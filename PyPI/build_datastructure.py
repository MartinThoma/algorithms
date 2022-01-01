#!/usr/bin/env python3

"""Get information about all projects on PyPI."""

import json
import logging
import sys
import threading
import time
import requests
import urllib
from urllib import request
from urllib.request import urlopen
from typing import List, Tuple, Any, Dict, Optional
import uuid
from pydantic import BaseModel
import datetime

import sqlite3

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
)


class PypiPackageInfo(BaseModel):
    author: str
    author_email: str
    bugtrack_url: Optional[str]
    classifiers: List[str]
    description: str
    description_content_type: str
    docs_url: str
    download_url: str
    downloads: Dict[str, Any]
    home_page: str
    keywords: str
    license: str
    maintainer: str
    maintainer_email: str
    name: str
    package_url: str
    platform: str
    project_url: str
    project_urls: Dict[str, Any]
    release_url: str
    requires_dist: List[str]
    requires_python: str
    summary: str
    version: str
    yanked: bool
    yanked_reason: Optional[Any]
    # stable_version: str = "UNKNOWN"
    # _pypi_hidden: int = -1


class PypiUrl(BaseModel):
    comment_text: str
    digests: Dict[str, Any]
    downloads: int
    filename: str
    has_sig: bool  # int?
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: str
    size: int
    upload_time: datetime.datetime
    upload_time_iso_8601: datetime.datetime
    url: str
    yanked: bool
    yanked_reason: Any


class PypiPackageInfoMain(BaseModel):
    info: PypiPackageInfo
    last_serial: int
    releases: Dict[str, Any]
    urls: List[PypiUrl]
    vulnerabilities: List[Any]


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def in_parallel(target, job_list: List[Tuple[str, str]], mysql):
    chunk_size = 5
    for package_name_link, package_name in job_list:
        if threading.active_count() > chunk_size:
            time.sleep(1)  # delays for 1 second
        threading.Thread(
            target=target, args=(package_name_link, package_name, mysql)
        ).start()


def get_package_names(
    simple_index: str = "https://pypi.python.org/simple/",
) -> List[Tuple[str, str]]:
    """
    Returns
    -------
    list
        Names of all packages.
    """

    def extract_package_name(line: str) -> Tuple[str, str]:
        line = line.strip()
        line = line[len('<a href="') : -len("</a>")]
        path = line.split('">')[0]
        name = line.split('">')[1]
        path = path.replace("simple/", "", 1)[1:-1]
        return (path, name)

    content = requests.get(simple_index).text
    lines = []
    for line in content.split("\n"):
        if "<a href=" in line:
            lines.append(extract_package_name(line))
    return lines


def get_package_info(package_name: str = "numpy") -> Optional[PypiPackageInfoMain]:
    """
    Parameters
    ----------
    package_name : str
        Name of a Python package

    Returns
    -------
    dict
        Package meta information
    """
    try:
        f = urlopen(f"https://pypi.org/pypi/{package_name}/json")
    except urllib.error.HTTPError as e:
        logging.error(f"'{package_name}' gave {str(e)}")
        return None
    content = f.read()
    f.close()
    return PypiPackageInfoMain.parse_raw(content.decode("utf-8"))


def insert_package_info(package_name: str, package_info: PypiPackageInfoMain, mysql):
    """
    Insert the package information into a MySQL database.

    Parameters
    ----------
    package_info : dict
    mysql : dict
        MySQL database connection information
    """
    releases = package_info.releases
    url_entries = package_info.urls
    package_info_info = package_info.info
    connection = sqlite3.connect("pypi.db")
    connection.row_factory = dict_factory

    cursor = connection.cursor()
    sql = (
        "INSERT INTO `packages` (`id`, `maintainer`, "
        "`docs_url`, `requires_python`, `maintainer_email`, "
        "`keywords`, `package_url`, "
        "`author`, `author_email`, `download_url`, `platform`, `version`, "
        "`description`, "
        "`release_url`, `name`, `bugtrack_url`, "
        "`license`, `summary`, `home_page`, `stable_version`, `_pypi_hidden` "
        ") VALUES "
        "(?, ?, ?, ?, "
        "?, "
        "?, ?, ?, ?, "
        "?, ?, ?, "
        "?, ?, ?, "
        "?, ?, ?, ?, "
        "?, ?);"
    )
    try:
        cursor.execute(
            sql,
            (
                str(uuid.uuid4()),
                package_info_info.maintainer,
                package_info_info.docs_url,
                package_info_info.requires_python,
                package_info_info.maintainer_email,
                package_info_info.keywords,
                package_info_info.package_url,
                package_info_info.author,
                package_info_info.author_email,
                package_info_info.download_url,
                package_info_info.platform,
                package_info_info.version,
                package_info_info.description,
                package_info_info.release_url,
                package_info_info.name,
                package_info_info.bugtrack_url,
                package_info_info.license,
                package_info_info.summary,
                package_info_info.home_page,
                None,  # package_info_info.stable_version
                -1,  # package_info_info._pypi_hidden
            ),
        )
        connection.commit()
        was_successful = True
    # except pymysql.err.IntegrityError as e:
    except sqlite3.IntegrityError as e:
        logging.error(f"{package_name} gave sqlite3.IntegrityError: {str(e)}")
        was_successful = False
    except ValueError as e:
        print(e)
        # logging.warning(
        #     ("Package '%s' is probably already in the database " "as '%s'"),
        #     package_name,
        #     package_info["name"],
        # )
        # if "Duplicate entry" not in str(e):
        #     logging.warning(e)
        was_successful = False

    if was_successful:
        # Get id
        db_package_id = is_package_in_database(package_info_info.name, mysql)

        # Enter releases
        for release_number, release_all in releases.items():
            for release in release_all:
                # e.g.
                # https://pypi.python.org/pypi/agoraplex.themes.sphinx/json
                # has one release number, but multiple releases for that
                # number ... strange
                for key in release:
                    release[key] = str(release[key])
                    if key == "has_sig":
                        release[key] = release[key].replace("True", "1")
                        release[key] = release[key].replace("False", "0")
                release["package_id"] = db_package_id
                release["release_number"] = release_number
                sql = (
                    "INSERT INTO `releases` (`id`, `package_id`, "
                    "`release_number`, "
                    "`has_sig`, `upload_time`, `comment_text`, "
                    "`python_version`, `url`, `md5_digest`, `downloads`, "
                    "`filename`, `packagetype`, `size`) VALUES "
                    "(?, ?, ?, ?, "
                    "?, ?, "
                    "?, "
                    "?, ?, ?, ?, "
                    "?, ?);"
                )
                cursor.execute(
                    sql,
                    (
                        str(uuid.uuid4()),
                        release["package_id"],
                        release["release_number"],
                        release["has_sig"],
                        release["upload_time"],
                        release["comment_text"],
                        release["python_version"],
                        release["url"],
                        release["md5_digest"],
                        release["downloads"],
                        release["filename"],
                        release["packagetype"],
                        release["size"],
                    ),
                )
        connection.commit()

        # Enter URLs
        for url_entry in url_entries:
            sql = (
                "INSERT INTO `urls` (`id`, `package_id`, `has_sig`, "
                "`upload_time`, `comment_text`, `python_version`, `url`, "
                "`md5_digest`, `downloads`, `filename`, `packagetype`, "
                "`size`) VALUES "
                "(?, ?, ?, ?, "
                "?, ?, ?, "
                "?, ?, ?, "
                "?, ?);"
            )
            cursor.execute(
                sql,
                (
                    str(uuid.uuid4()),
                    db_package_id,
                    url_entry.has_sig,
                    url_entry.upload_time,
                    url_entry.comment_text,
                    url_entry.python_version,
                    url_entry.url,
                    url_entry.md5_digest,
                    url_entry.downloads,
                    url_entry.filename,
                    url_entry.packagetype,
                    url_entry.size,
                ),
            )
        connection.commit()

        # Enter classifiers:
        for classifier in package_info_info.classifiers:
            sql = (
                "INSERT INTO `package_classifiers` (`id`, `package_id`, "
                "`classifier`) VALUES (?, ?, ?);"
            )
            cursor.execute(sql, (str(uuid.uuid4()), db_package_id, classifier))
        connection.commit()
    connection.close()


def is_package_in_database(name, mysql):
    """
    Check if a package is in the database.

    Parameters
    ----------
    package_name : str
    mysql : dict
        MySQL database connection information

    Returns
    -------
    Either ``None`` or an integer (the ID in the database)
    """
    connection = sqlite3.connect("pypi.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    sql = "SELECT id FROM `packages` WHERE `name` = ?"
    cursor.execute(sql, (name,))
    id_number = cursor.fetchone()
    connection.close()
    if id_number is not None and "id" in id_number:
        id_number = id_number["id"]
    return id_number


def handle_package(
    package_name_link: str, package_name: str, mysql: Dict[str, Any]
) -> None:
    """
    Load package information and store it in the database.

    Parameters
    ----------
    package_name_link : str
    package_name : str
    mysql : dict
        MySQL database connection information
    """
    package_id = is_package_in_database(package_name, mysql)
    if package_id is not None:
        logging.info(f"Package '{package_name}' already in database. Continue.")
        return
    logging.info(f"Load '{package_name_link}'...")
    package_info = get_package_info(package_name_link)
    if package_info is None:
        return
    insert_package_info(package_name, package_info, mysql)


def main():
    logging.info("Get package names. This takes about 50 seconds...")
    package_names = get_package_names()
    logging.info(f"{len(package_names)} packages found.")
    with open("secret.json") as f:
        mysql = json.load(f)

    in_parallel(handle_package, package_names, mysql)
    # for package_name_link, package_name in package_names:
    #     handle_package(package_name_link, package_name, mysql)


if __name__ == "__main__":
    main()
