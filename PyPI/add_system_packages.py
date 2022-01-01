#!/usr/bin/env python

import json
import logging
import sqlite3
import uuid


def main():
    """
    Add system modules. Please run 'build_datastructure.py' before.
    """
    sys_modules = get_system_modules()
    connection = sqlite3.connect("pypi.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    for package_name in sys_modules:
        sql = (
            "INSERT INTO `packages` "
            "(`id`, `name`, `on_pypi`, "
            "`author`, `author_email`, `maintainer`, `maintainer_email`, "
            "`requires_python`, `platform`, `version`, `license`, `keywords`, "
            "`description`, `summary`, `stable_version`, `home_page`, "
            "`release_url`, `bugtrack_url`, `download_url`, `docs_url`, "
            "`package_url`, `_pypi_hidden`) "
            "VALUES "
            "(?, ?, 0, 'python::system::module', 'python::system::module'"
            ", 'python::system::module', 'python::system::module', true, "
            "'all', 'n/a', 'NULL', '', '', '', '', '', '', '', '', '', '', '');"
        )
        try:
            cursor.execute(
                sql,
                (
                    str(uuid.uuid4()),
                    package_name,
                ),
            )
            connection.commit()
        except ValueError as e:
            logging.warning(
                ("Package '%s' is probably already in the database"), package_name
            )
            if "Duplicate entry" not in str(e):
                logging.warning(e)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_system_modules():
    """
    Get a list of system modules.

    Returns
    -------
    list :
        System modules
    """
    # print("## " + "System modules " + "#"*60)
    import sys

    system_modules = sorted(sys.modules.keys())
    # for m in system_modules:
    #     print(m)

    # print("## " + "pkg_resources " + "#"*60)
    pkg_resources_pkgs = []
    for dist in __import__("pkg_resources").working_set:
        if dist.project_name not in system_modules:
            pkg_resources_pkgs.append(dist.project_name)

    pkg_resources_pkgs = sorted(pkg_resources_pkgs)

    # for p in pkg_resources_pkgs:
    #     print(p)

    # print("## " + "pkgutil " + "#"*60)
    import pkgutil

    pkg_utils = []
    for m in pkgutil.iter_modules():
        if m[1] not in (system_modules + pkg_resources_pkgs):
            pkg_utils.append(m[1])
    pkg_utils = sorted(pkg_utils)
    # for m in pkg_utils:
    #     print(m)
    return sorted(system_modules + pkg_resources_pkgs + pkg_utils)


if __name__ == "__main__":
    main()
