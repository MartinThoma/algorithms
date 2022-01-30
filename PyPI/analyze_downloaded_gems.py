"""
With this script, I want to figure out which packages are worth to be used.
"""
from typing import List, Optional, Dict, Any, Tuple
import requests
from pathlib import Path
import sqlite3
import re
import logging
from packaging import version
from tqdm import tqdm
import csv
import json

# Only show warnings
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Disable all child loggers of urllib3, e.g. urllib3.connectionpool
logging.getLogger("urllib3").propagate = False

from package_analysis import download


def main(
    pkg_data_dir="/media/moose/1d41967e-6a0c-4c0e-af8c-68d4fae7fa64/moose/pypipackages",
):
    downloaded_files = get_downloaded(Path(pkg_data_dir))
    names = [get_pkg_name_from_path(i) for i in downloaded_files]
    disk_names = set([standardize_name(name) for name in names])
    print(f"Downloaded: {len(names):,}")

    non_crap = get_non_crap()
    print(f"Non-crap packages: {len(non_crap):,}")
    pkg2max_version = {}
    too_small = []

    conn = sqlite3.connect("pypi.db")
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(
        f"SELECT id, name, summary, keywords, author, home_page, package_url FROM packages"
    )
    rows = c.fetchall()
    pkg_id2pkg = {row["id"]: row for row in rows}
    pgk2id = {
        standardize_name(pkg["name"]): pkg_id for pkg_id, pkg in pkg_id2pkg.items()
    }

    print("Building releases dict")
    c.execute(f"SELECT * FROM releases")
    rows = c.fetchall()
    pkg_id2release = {}
    for row in rows:
        if row["package_id"] not in pkg_id2release or version.parse(
            pkg_id2release[row["package_id"]]["release_number"]
        ) < version.parse(row["release_number"]):
            pkg_id2release[row["package_id"]] = row
    print("Finished building releases dict")
    non_crap = set([standardize_name(pkg) for pkg in non_crap])
    too_old = []
    for pkg in tqdm(non_crap):
        pkg2max_version[pkg] = pkg_id2release.get(pgk2id[pkg])
        if (
            # no code
            pkg2max_version[pkg] is None
            or pkg2max_version[pkg]["size"] < 2000
            # author don't thinks it's beta
            or version.parse(pkg2max_version[pkg]["release_number"])
            < version.parse("0.1.0")
            # no activity in over a year
            # or pkg2max_version[pkg]["upload_time"] < "2021-01-01"
        ):
            too_small.append(standardize_name(pkg))
        elif pkg2max_version[pkg]["upload_time"] < "2021-01-01":
            too_old.append(pkg)
            too_small.append(standardize_name(pkg))
    print(f"Too small/null version: {len(too_small):,}")
    print(f"Too old: {len(too_old):,}")

    non_crap = set([standardize_name(pkg) for pkg in non_crap])
    non_crap = non_crap - set(too_small)
    print(f"Non-crap packages with reasonable size: {len(non_crap):,}")

    print(
        f"Interesction: {len(non_crap.intersection(disk_names)):,} <------ those might be good!"
    )
    print(f"Downloaded, but not in non-crap DB: {len(disk_names - non_crap):,}:")
    for el in list(disk_names - non_crap)[:10]:
        print(f"* {el}")
    # print([n for n in non_crap if "openpyxl" in n])
    # print([n for n in disk_names if "openpyxl" in n])
    print(f"non-crap DB, but not in downloaded: {len(non_crap - disk_names):,}")
    download_missing = False
    if download_missing:
        with open("no-content-files.csv", "w") as fp:
            for el in list(non_crap - disk_names):
                pkg_url = get_pkg_url(el)
                if pkg_url is None:
                    fp.write(el)
                    fp.write("\n")
                    continue
                _, target = download(pkg_url)
                # print(f"Downloaded to {target}...")
                # print(f"* {el}")
    print("-" * 80)

    with open("secret.json") as fp:
        secrets = json.load(fp)

    with open(f"{secrets['meta_folder']}/pypi-packages.csv", "wt") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(
            [
                "package_name",
                "summary",
                "keywords",
                "release_number",
                "size",
                "author",
                "home_page",
                "package_url",
            ]
        )
        non_crap = non_crap.intersection(disk_names)
        for pkg_name in sorted(non_crap):
            pkg_id = pgk2id[pkg_name]
            release = pkg_id2release[pkg_id]
            pkg = pkg_id2pkg[pkg_id]
            writer.writerow(
                [
                    pkg_name,
                    pkg["summary"].replace("\n", " ").replace("\r", " ")[:160],
                    pkg["keywords"].replace("\n", " ").replace("\r", " ")[:160],
                    release["release_number"],
                    release["size"],
                    pkg["author"].replace("\n", " ").replace("\r", " "),
                    pkg["home_page"].replace("\n", " ").replace("\r", " "),
                    pkg["package_url"].replace("\n", " ").replace("\r", " "),
                ]
            )
            c.execute(
                "REPLACE INTO computed_values (package_id, latest_release_id, unusable) VALUES (?, ?, ?)",
                (pkg_id, release["id"], 0),
            )
        for pkg_name, pkg_id in pgk2id.items():
            if pkg_name in non_crap:
                continue
            c.execute(
                "REPLACE INTO computed_values (package_id, unusable) VALUES (?, ?)",
                (pgk2id[pkg_name], 1),
            )
        conn.commit()


def get_latest_release(pkg_id: str, pkg_name: str) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect("pypi.db")
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(f"SELECT * FROM releases WHERE package_id='{pkg_id}'")
    rows = c.fetchall()
    latest_release = None
    max_release_number = version.parse("0-dev")
    for row in rows:
        release_number = version.parse(row["release_number"])
        if release_number > max_release_number:
            max_release_number = release_number
            latest_release = row
    return latest_release


def version_str_to_semver(version_str: str) -> Tuple[int, int, int, str]:
    version_str_orig = version_str
    if "-" in version_str:
        version_str_p = version_str.split("-")
        version_str = version_str_p[0]
        rest = "-".join(version_str_p[1:])
    else:
        rest = ""
    parts = version_str.split(".")
    if len(parts) == 0:
        raise ValueError(f"Invalid version string: {version_str_orig}")

    if len(parts) == 1:
        return (int(parts[0]), 0, 0, rest)
    if len(parts) == 2:
        return (int(parts[0]), int(parts[1]), 0, rest)
    if len(parts) == 3:
        return (int(parts[0]), int(parts[1]), int(parts[2]), rest)
    raise ValueError(f"Invalid version string: {version_str_orig}")


def get_downloaded(pkg_data_dir: Path) -> List[Path]:
    return [p for p in pkg_data_dir.iterdir() if p.is_file()]


def get_pkg_url(pkg_name: str) -> Optional[str]:
    meta_url = f"https://pypi.org/simple/{pkg_name}/"
    response = requests.get(meta_url)
    for line in response.text.split("\n"):
        if "<a href=" in line:
            url = line.split('"')[1]
            url = url.split("#")[0]
            if url.endswith(".exe"):
                continue
            return url
    return None


def standardize_name(name: str) -> str:
    return name.lower().replace("-", "_").replace(" ", "_").replace("%20", "_")


def get_pkg_name_from_path(path: Path) -> str:
    filename = path.stem

    # Remove extension
    if filename.endswith(".tar"):
        filename = filename[:-4]

    semantic_version = re.compile(r"-[0-9]+\.[0-9]+(\.[0-9]+)*")
    filename = semantic_version.split(filename)[0]

    # for ext in [
    #     "-py3-none-any",
    #     "-py27-none-any",
    #     "-py34-none-any",
    #     "-py35-none-any",
    #     "-py36-none-any",
    #     "-py37-none-any",
    #     "-py38-none-any",
    #     "-py39-none-any",
    #     "-py2-none-any",
    #     ".py2-none-any",
    #     ".py3-none-any",
    #     "-py3-none-any.whl",
    #     "-py27-none-any.whl",
    #     "-py34-none-any.whl",
    #     "-py35-none-any.whl",
    #     "-py36-none-any.whl",
    #     "-py37-none-any.whl",
    #     "-py38-none-any.whl",
    #     "-py39-none-any.whl",
    # ]:
    #     if filename.endswith(ext):
    #         filename = filename[: -len(ext)]

    return filename


def get_non_crap() -> List[str]:
    connection = sqlite3.connect("pypi.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()

    crap = (
        "on_pypi = 0 "
        "OR author = 'Example Author' "
        "OR packages.id IN (SELECT DISTINCT package_id FROM package_classifiers WHERE classifier = 'Development Status :: 1 - Planning' or classifier = 'Development Status :: 2 - Pre-Alpha' or classifier = 'Development Status :: 3 - Alpha' or classifier = 'Development Status :: 7 - Inactive') "
        "OR author = 'Your Name' "
        "OR name LIKE('%example%') "
        # Remove packages created by beginners who read a 'head first' book
        r"OR LOWER(summary) LIKE('%a simple printer of nested lists%') "
        r"OR LOWER(summary) LIKE('%a small example package%') "
        r"OR LOWER(summary) LIKE('%example package%') "
        r"OR LOWER(summary) LIKE('%an example for%') "
        r"OR LOWER(summary) LIKE('%template project%') "
        r"OR LOWER(summary) LIKE('%reserved for%') "
        r"OR LOWER(summary) LIKE('%for learning purposes%') "
        r"OR LOWER(summary) LIKE('%reserved package name%') "
        r"OR LOWER(summary) LIKE('%package placeholder%') "
        r"OR LOWER(summary) LIKE('%a harmless package to prevent exploitation%') "
        r"OR LOWER(summary) LIKE('%first python%') "
        r"OR LOWER(summary) LIKE('%demo package%') "
        r"OR LOWER(summary) LIKE('%sample package%') "
        r"OR LOWER(summary) LIKE('%hello world%') "
        r"OR LOWER(summary) LIKE('%first package%') "
        r"OR LOWER(summary) LIKE('%python runer lib support shell, ssh ...%') "
        r"OR LOWER(keywords) LIKE('%hello world%') "
        "OR LOWER(author) = 'hfpython' "
        "OR home_page = 'https://example.org' "
        "OR home_page = 'https://example.com/' "
        "OR home_page = 'https://github.com/pypa/example-project'"
        "OR home_page LIKE ('%http://www.headfirstlabs.com%') "
    )
    sql = f"SELECT name FROM `packages` WHERE NOT ({crap})"
    cursor.execute(sql)
    non_craps = cursor.fetchall()
    return [non_crap["name"] for non_crap in non_craps]


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


if __name__ == "__main__":
    main()
