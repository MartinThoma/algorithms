#!/usr/bin/env python

import json
import logging
import pymysql


def main():
    """
    Add system modules. Please run 'build_datastructure.py' before.
    """
    with open("secret.json") as f:
        mysql = json.load(f)
    sys_modules = get_system_modules()
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    cursor = connection.cursor()
    for package_name in sys_modules:
        sql = ("INSERT INTO `packages` (`name`, `on_pypi`) VALUES "
               "('{name}', 0);").format(name=package_name)
        try:
            cursor.execute(sql)
            connection.commit()
        except pymysql.err.IntegrityError as e:
            logging.warning(("Package '%s' is probably already in the "
                             "database"),
                            package_name)
            if 'Duplicate entry' not in str(e):
                logging.warning(e)


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
    for dist in __import__('pkg_resources').working_set:
        if dist.project_name not in system_modules:
            pkg_resources_pkgs.append(dist.project_name)

    pkg_resources_pkgs = sorted(pkg_resources_pkgs)

    # for p in pkg_resources_pkgs:
    #     print(p)

    # print("## " + "pkgutil " + "#"*60)
    import pkgutil
    pkg_utils = []
    for m in pkgutil.iter_modules():
        if m[1] not in (system_modules+pkg_resources_pkgs):
            pkg_utils.append(m[1])
    pkg_utils = sorted(pkg_utils)
    # for m in pkg_utils:
    #     print(m)
    return sorted(system_modules + pkg_resources_pkgs + pkg_utils)


if __name__ == '__main__':
    main()
