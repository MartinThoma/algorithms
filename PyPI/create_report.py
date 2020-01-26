#!/usr/bin/env python

"""Create report."""

import json

import matplotlib.pyplot as plt
import numpy as np
import pymysql
from jinja2 import Template

template_parameters = {}


def create_barh(names, values, title, ylabel, filename):
    plt.figure(figsize=(8, 8))
    y_pos = np.arange(len(names))
    plt.barh(y_pos, values, align="center")
    plt.yticks(y_pos, names)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename, bbox_inches="tight")


with open("secret.json") as f:
    mysql = json.load(f)

connection = pymysql.connect(
    host=mysql["host"],
    user=mysql["user"],
    passwd=mysql["passwd"],
    db=mysql["db"],
    cursorclass=pymysql.cursors.DictCursor,
    charset="utf8",
)
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
        "images/pypi-imported-packages-count.png",
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
        "images/pypi-imported-packages-excluding-system-count.png",
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
        "images/pypi-imported-packages.png",
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
        "images/pypi-imported-packages-excluding-system.png",
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

sql = """SELECT COUNT(DISTINCT `author`) AS `total_authors` FROM `packages`"""
cursor.execute(sql)
total_authors = cursor.fetchone()["total_authors"]

template_parameters["total_authors"] = total_authors

sql = """
SELECT
    `author`, COUNT(`id`) as `created_packages`
FROM
    `packages`
GROUP BY
    `author`
ORDER BY
    COUNT(`id`) DESC, `author` ASC
LIMIT
    10
"""
cursor.execute(sql)
results = cursor.fetchall()
template_parameters["author_dicts"] = results


def get_max_attribute(attribute_name):
    sql = f"""SELECT `{attribute_name}`, LENGTH(`{attribute_name}`) as count FROM `packages` ORDER BY LENGTH(`{attribute_name}`) DESC LIMIT 1"""
    cursor.execute(sql)
    results = cursor.fetchone()
    return results[attribute_name]


def get_null_attribute(attribute_name):
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
template_parameters["null"] = {}
for attribute_name in attribute_names:
    template_parameters["max"][attribute_name] = get_max_attribute(attribute_name)
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

sql = """SELECT min(`license`) as name, COUNT(`id`) as count FROM `packages` GROUP BY lower(`license`) ORDER BY COUNT(`id`) DESC LIMIT 10"""
cursor.execute(sql)
results = cursor.fetchall()
template_parameters["licenses"] = results

sql = """
SELECT `name`, `url`, `downloads`
FROM `urls`
JOIN `packages` ON `urls`.`package_id` = `packages`.`id`
ORDER BY `urls`.`downloads`  DESC
LIMIT 10"""
cursor.execute(sql)
results = cursor.fetchall()
template_parameters["max_downloads"] = results


sql = """
SELECT
    `name`, `release_number`, `size`
FROM
    `releases`
JOIN
    `packages` ON `releases`.`package_id` = `packages`.`id`
WHERE releases.id IN (SELECT MAX(id) FROM releases GROUP BY package_id)
ORDER BY
    `releases`.`size` DESC
LIMIT 15"""
cursor.execute(sql)
results = cursor.fetchall()
template_parameters["max_pkg_sizes"] = results


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
with open("created_report.html", "w") as f:
    f.write(rendered)
