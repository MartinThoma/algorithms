#!/usr/bin/env python

"""Create report."""

from typing import Any
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Template
import sqlite3
from math import ceil
import json

template_parameters = {}


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_barh(names, values, title, ylabel, filename):
    plt.figure(figsize=(8, 8))
    y_pos = np.arange(len(names))
    plt.barh(y_pos, values, align="center")
    plt.yticks(y_pos, names)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename, bbox_inches="tight")


def get_packages_by_x(cursor, x: str = "author") -> dict[str, int]:
    pkg_by_author: dict[str, int] = {}
    sql = f"""SELECT {x} FROM `packages` JOIN computed_values ON packages.id = package_id WHERE unusable=0"""
    cursor.execute(sql)  ## todo
    rows = cursor.fetchall()
    for row in rows:
        author = row[x].lower()
        if "Odoo Community Association".lower() in author:
            author = "Odoo Community Association".lower()
        if author not in pkg_by_author:
            pkg_by_author[author] = 0
        pkg_by_author[author] += 1
    return pkg_by_author


def get_licenses(cursor, min_count: int = 1) -> list[dict[str, Any]]:
    sql = f"""SELECT license, COUNT(id) as count FROM `packages` JOIN computed_values ON packages.id = package_id WHERE unusable=0 GROUP BY license ORDER BY count DESC"""
    cursor.execute(sql)
    results = cursor.fetchall()
    results_dict = {}
    for result in results:
        name = result["license"].upper()
        if name in ["", "UNKNOWN"]:
            name = "Unknown"
        elif name in ["NO LICENSE", "NOPE"]:
            name = "NO LICENSE"
        elif name in [
            "MIT",
            "MIT LICENSE",
            "MIT LICENCE",
            "LICENSE :: OSI APPROVED :: MIT LICENSE",
            "THE MIT LICENSE (MIT)",
            "THE MIT LICENSE",
            "HTTP://OPENSOURCE.ORG/LICENSES/MIT",
            "HTTP://WWW.OPENSOURCE.ORG/LICENSES/MIT-LICENSE.PHP",
            '"MIT"',
            "['MIT']",
        ]:
            name = "MIT"
        elif name in [
            "APACHE LICENSE 2.0",
            "APACHE 2.0",
            "APACHE-2.0",
            "APACHE LICENSE, VERSION 2.0",
            "APACHE SOFTWARE LICENSE 2.0",
            "HTTP://WWW.APACHE.ORG/LICENSES/LICENSE-2.0",
            "APACHE SOFTWARE LICENSE (APACHE 2.0)",
            "APACHE V2.0 LICENSE",
            "APACHE SOFTWARE LICENSE V2.0",
            "APACHE LICENSE VERSION 2.0, JANUARY 2004 HTTP://WWW.APACHE.ORG/LICENSES/",
            "APACHE 2",
            "APACHE2",
            "APACHE LICENSE VERSION 2.0",
            "APACHE-2.0 LICENSE",
            "APACHE-2",
            "APACHE LICENSE (2.0)",
            "APACHE V2",
            "APACHE 2.0 LICENSE",
            "APACHE2.0",
            "APACHE V2.0",
            "APACHE LICENSE V2.0",
            "APACHE LICENSE V2",
            "APACHE LICENSE 2",
            "APACHE LICENCE 2.0",
            "HTTPS://WWW.APACHE.ORG/LICENSES/LICENSE-2.0",
        ]:
            name = "APACHE LICENSE 2.0"
        elif name in [
            "APACHE",
            "APACHE SOFTWARE LICENSE",
            "APACHE LICENSE",
            "LICENSE :: OSI APPROVED :: APACHE SOFTWARE LICENSE",
        ]:
            name = "APACHE"
        elif name in [
            "GPLV3",
            "GPL-3.0",
            "GPL-3",
            "GPL3",
            "GNU GPLV3",
            "GNU GENERAL PUBLIC LICENSE V3.0",
            "GNU GENERAL PUBLIC LICENSE V3 (GPLV3)",
            "LICENSE :: OSI APPROVED :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)",
        ]:
            name = "GPLv3"
        elif name in [
            "BSD",
            "BSD LICENCE, SEE LICENSE FILE",
            "BSD LICENSE",
            "LICENSE :: OSI APPROVED :: BSD LICENSE",
            "BSD LICENCE, SEE LICENCE.TXT",
        ]:
            name = "BSD"
        elif name in ["BSD-3-CLAUSE", "BSD 3-CLAUSE", "BSD 3-CLAUSE LICENSE", "BSD-3"]:
            name = "BSD-3-CLAUSE"
        elif name in ["LICENSE", "LICENSE.TXT", "SEE LICENSE.TXT", "LICENCE.TXT"]:
            name = "name of a file"

        if name not in results_dict:
            results_dict[name] = 0
        results_dict[name] += result["count"]
    results = [
        {"name": name, "count": count}
        for name, count in results_dict.items()
        if count >= min_count
    ]
    return sorted(results, key=lambda n: n["count"], reverse=True)


def get_release_sizes(cursor) -> list[dict[str, Any]]:
    sql = f"""
    SELECT
        `name`, `release_number`, `size`
    FROM
        `releases`
    JOIN
        `packages` ON `releases`.`package_id` = `packages`.`id`
    JOIN computed_values ON packages.id = computed_values.package_id
    WHERE releases.id IN (SELECT MAX(id) FROM releases GROUP BY releases.package_id) AND  unusable=0
    ORDER BY
        `releases`.`size` DESC
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


with open("secret.json") as fp:
    secrets = json.load(fp)

connection = sqlite3.connect("pypi.db")
connection.row_factory = dict_factory
cursor = connection.cursor()

queries = []
sql = """
SELECT
    `packages`.`name`,
    COUNT(`needs_package`) as count
FROM
    `dependencies`
JOIN
    `packages` ON `needs_package` = `packages`.`id`
GROUP BY
    `needs_package`
ORDER BY
    COUNT(`needs_package`) DESC
LIMIT 20
    """
queries.append(
    (
        sql,
        "Module imports of Python packages",
        "Name of the imported package",
        f"{secrets['meta_folder']}/pypi-imported-packages-count.png",
    )
)
###
sql = """
SELECT
    `packages`.`name`,
    COUNT(`needs_package`) as count
FROM
    `dependencies`
JOIN
    `packages` ON `needs_package` = `packages`.`id`
WHERE
    `on_pypi` = 1
GROUP BY
    `needs_package`
ORDER BY
    COUNT(`needs_package`) DESC
LIMIT 20
"""
queries.append(
    (
        sql,
        "Module imports of Python modules excluding system modules",
        "Name of the imported package",
        f"{secrets['meta_folder']}/pypi-imported-packages-excluding-system-count.png",
    )
)
###
sql = """
SELECT
    `packages`.`name`,
    SUM(`times`) as count
FROM
    `dependencies`
JOIN
    `packages` ON `needs_package` = `packages`.`id`
GROUP BY
    `needs_package`
ORDER BY
    SUM(`times`) DESC
LIMIT 20
"""
queries.append(
    (
        sql,
        "Weighted module imports by Python packages",
        "Name of the imported module",
        f"{secrets['meta_folder']}/pypi-imported-packages.png",
    )
)
###
sql = """
SELECT
    `packages`.`name`,
    SUM(`times`) as count
FROM
    `dependencies`
JOIN
    `packages` ON `needs_package` = `packages`.`id`
WHERE
    `on_pypi` = 1
GROUP BY
    `needs_package`
ORDER BY
    SUM(`times`) DESC
LIMIT 20
"""
queries.append(
    (
        sql,
        "Module imports of Python packages, excluding system packages",
        "Number of imports",
        f"{secrets['meta_folder']}/pypi-imported-packages-excluding-system.png",
    )
)


for sql, title, ylabel, filename in queries:
    cursor.execute(sql)
    result = cursor.fetchall()
    names = [el["name"] for el in result][::-1]
    values = [el["count"] for el in result][::-1]
    create_barh(names, values, title, ylabel=ylabel, filename=filename)

###

sql = """
SELECT
    `packages`.`id`, `name`
FROM `packages`
WHERE
    `id` in (
        SELECT DISTINCT
            `dependencies`.`package`
        FROM
            dependencies)
OR `id` in (
        SELECT DISTINCT
            `dependencies`.`needs_package`
        FROM
            `dependencies`)"""
cursor.execute(sql)
used_packages = cursor.fetchall()


sql = """SELECT COUNT(id) as count FROM `packages`"""
cursor.execute(sql)
all_packages = cursor.fetchone()["count"]

template_parameters["all_packages"] = all_packages
template_parameters["nb_used_packages"] = len(used_packages)

sql = """SELECT COUNT(id) as count FROM `packages`"""
cursor.execute(sql)
total_packages = cursor.fetchone()["count"]
template_parameters["total_packages"] = total_packages

sql = """SELECT COUNT(id) as count FROM `packages` WHERE on_pypi = 0"""
cursor.execute(sql)
total_packages = cursor.fetchone()["count"]
template_parameters["draft_pkgs_not_on_pypi"] = total_packages


sql = """SELECT COUNT(id) as count FROM `packages` WHERE author = 'Example Author' or author = 'Your Name'"""
cursor.execute(sql)
total_packages = cursor.fetchone()["count"]
template_parameters["draft_pkgs_example_author"] = total_packages

sql = """SELECT COUNT(id) as count FROM `packages` WHERE name LIKE('%example%')"""
cursor.execute(sql)
total_packages = cursor.fetchone()["count"]
template_parameters["draft_pkgs_example_name"] = total_packages

sql = """SELECT COUNT(id) as count FROM `packages` WHERE id IN (SELECT DISTINCT package_id FROM package_classifiers WHERE classifier = 'Development Status :: 1 - Planning' or classifier = 'Development Status :: 2 - Pre-Alpha' or classifier = 'Development Status :: 3 - Alpha'
)"""
cursor.execute(sql)
total_packages = cursor.fetchone()["count"]
template_parameters["draft_pkgs_development_status"] = total_packages

sql = f"""SELECT COUNT(id) as count FROM `packages` JOIN computed_values ON packages.id = package_id WHERE unusable=0"""
cursor.execute(sql)
total_packages = cursor.fetchone()["count"]
template_parameters["nb_noncrap"] = total_packages


def gen_dev_stats(template_parameters, dev_type: str = "author"):
    pkg_by_author = get_packages_by_x(cursor, dev_type)
    template_parameters[f"total_{dev_type}s"] = len(pkg_by_author)
    max_authors = 100
    template_parameters[f"{dev_type}_dicts"] = [
        {dev_type: author, "created_packages": count}
        for author, count in sorted(
            pkg_by_author.items(), key=lambda x: x[1], reverse=True
        )[:max_authors]
    ]
    template_parameters[f"nb_{dev_type}s"] = len(pkg_by_author)
    template_parameters[f"pkg_by_{dev_type}_p75"] = int(
        ceil(np.percentile(list(pkg_by_author.values()), 75))
    )
    template_parameters[f"pkg_by_{dev_type}_p95"] = int(
        ceil(np.percentile(list(pkg_by_author.values()), 95))
    )
    template_parameters[f"pkg_by_{dev_type}_p99"] = int(
        ceil(np.percentile(list(pkg_by_author.values()), 99))
    )
    template_parameters[f"pkg_by_{dev_type}_50plus"] = len(
        [count for count in pkg_by_author.values() if count >= 50]
    )


gen_dev_stats(template_parameters, dev_type="author")
gen_dev_stats(template_parameters, dev_type="maintainer")
gen_dev_stats(template_parameters, dev_type="maintainer_email")


def get_max_attribute(attribute_name: str) -> int:
    sql = f"""SELECT `{attribute_name}`, LENGTH(`{attribute_name}`) as count FROM `packages` ORDER BY LENGTH(`{attribute_name}`) DESC LIMIT 1"""
    cursor.execute(sql)
    results = cursor.fetchone()
    return results[attribute_name]


def get_max_attribute_pkg(attribute_name: str) -> str:
    sql = f"""SELECT package_url FROM `packages` ORDER BY LENGTH(`{attribute_name}`) DESC LIMIT 1"""
    cursor.execute(sql)
    results = cursor.fetchone()
    return results["package_url"]


def get_null_attribute(attribute_name: str) -> int:
    sql = (
        f"""SELECT COUNT(id) as count FROM `packages` WHERE `{attribute_name}` = "";"""
    )
    cursor.execute(sql)
    results = cursor.fetchone()
    return results["count"]


attribute_names = [
    "name",
    "version",
    "stable_version",
    "release_url",
    "package_url",
    "bugtrack_url",
    "summary",
    "home_page",
    "author",
    "author_email",
    "license",
    "keywords",
    "requires_python",
    "maintainer",
    "maintainer_email",
    "platform",
    "download_url",
]
template_parameters["attribute_names"] = attribute_names
template_parameters["max"] = {}
template_parameters["max_pkg"] = {}
template_parameters["null"] = {}
for attribute_name in attribute_names:
    template_parameters["max"][attribute_name] = get_max_attribute(attribute_name)
    template_parameters["max_pkg"][attribute_name] = get_max_attribute_pkg(
        attribute_name
    )
    template_parameters["null"][attribute_name] = get_null_attribute(attribute_name)

sql = """SELECT `author`, LENGTH(`author`) as count FROM `packages` ORDER BY LENGTH(`author`) DESC LIMIT 1"""
cursor.execute(sql)
results = cursor.fetchone()
template_parameters["max_author"] = results["author"]

###

sql = """SELECT min(`platform`) as name, COUNT(`id`) as count FROM `packages` GROUP BY lower(`platform`) ORDER BY COUNT(`id`) DESC LIMIT 20"""
cursor.execute(sql)
results = cursor.fetchall()
template_parameters["platforms"] = results

template_parameters["licenses"] = get_licenses(cursor, min_count=1000)

sql = f"""
SELECT `name`, `url`, `downloads`
FROM `urls`
JOIN `packages` ON `urls`.`package_id` = `packages`.`id`
JOIN computed_values ON packages.id = computed_values.package_id 
WHERE unusable=0
ORDER BY `urls`.`downloads`  DESC
LIMIT 10"""
cursor.execute(sql)
results = cursor.fetchall()
template_parameters["max_downloads"] = results


template_parameters["max_pkg_sizes"] = get_release_sizes(cursor)
template_parameters["pkg_sizes_p75"] = np.percentile(
    [result["size"] for result in template_parameters["max_pkg_sizes"]], 75
)
template_parameters["pkg_sizes_p95"] = np.percentile(
    [result["size"] for result in template_parameters["max_pkg_sizes"]], 95
)
template_parameters["pkg_sizes_p99"] = np.percentile(
    [result["size"] for result in template_parameters["max_pkg_sizes"]], 99
)


sql = """
SELECT
    `packagetype` as name, COUNT(`id`) as count
FROM
    `urls`
GROUP BY
    packagetype
ORDER BY
    COUNT(`id`) DESC
"""
cursor.execute(sql)
results = cursor.fetchall()
template_parameters["max_packagetypes"] = results


### Template
with open("template.html") as f:
    query = f.read()
query = Template(query)
rendered = query.render(**template_parameters)
with open(f"{secrets['meta_folder']}/created_report.html", "w") as f:
    f.write(rendered)
