#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Analysis of Python packages."""

import json
import os
import pymysql.cursors
import re
import tarfile
import urllib
import logging
import sys
from os import walk

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main(package_url):
    pkg_name = "-".join(os.path.basename(package_url)[:-7].split("-")[:-1])
    filepaths = download(package_url)
    with open("secret.json") as f:
        mysql = json.load(f)
    package_id = get_pkg_id_by_name(pkg_name, mysql)
    required_packages = get_requirements(filepaths, pkg_name)
    imported_packages = get_imports(filepaths, pkg_name)
    store_dependencies(mysql, package_id, required_packages, imported_packages)


def store_dependencies(mysql,
                       package_id,
                       required_packages,
                       imported_packages):
    """
    Parameters
    ----------
    mysql : dict
        MySQL database connection information
    package_id : int
    required_packages : list
    imported_packages : list
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    cursor = connection.cursor()

    for pkg, times in imported_packages.items():
        cursor = connection.cursor()
        package_info = {'package': package_id,
                        'needs_package': get_pkg_id_by_name(pkg, mysql),
                        'times': times,
                        'req_type': 'imported'}
        if package_info['needs_package'] is not None:
            try:
                sql = ("INSERT INTO `dependencies` "
                       "(`package`, `needs_package`, `req_type`, `times`) "
                       " VALUES "
                       "('{package}', '{needs_package}', '{req_type}', "
                       "'{times}');").format(
                    **package_info)
                cursor.execute(sql)
                connection.commit()
            except pymysql.err.IntegrityError as e:
                if 'Duplicate entry' not in str(e):
                    logging.warning(e)
        else:
            logging.info("Package '%s' was not found. Skip.", pkg)


def get_pkg_id_by_name(pkg_name, mysql):
    """
    Parameters
    ----------
    pkg_name : str
    mysql : dict
        MySQL database connection information
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    cursor = connection.cursor()
    sql = "SELECT id FROM `packages` WHERE `name` = '%s'" % pkg_name
    cursor.execute(sql)
    id_number = cursor.fetchone()
    if id_number is not None and 'id' in id_number:
        return id_number['id']
    else:
        return None


def download(package_url):
    """
    Parameters
    ----------
    package_url : str
        Something ending with tar.gz

    Returns
    -------
    list
        Paths to all unpackaged files
    """
    assert package_url.endswith(".tar.gz")
    target_dir = "pypipackages"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    pkg_name = os.path.basename(package_url)
    target = os.path.join(target_dir, pkg_name)

    if not os.path.exists(target):
        urllib.urlretrieve(package_url, target)
        logging.info("Package '%s' downloaded.", pkg_name)
        with tarfile.open(target) as tar:
            tar.extractall(target[:-7])
    else:
        logging.info("Package '%s' was already downloaded.", pkg_name)

    filepaths = []
    for (dirpath, dirnames, filenames) in walk(target[:-7]):
        filepaths.extend([os.path.join(dirpath, f) for f in filenames])
    return filepaths


def get_requirements(filepaths, pkg_name):
    """
    Get a list of all "officially" set requirements.

    Parameters
    ----------
    filepaths : list
        Paths to files of a package
    pkg_name : str
        Name of the currently parsed package.

    Returns
    -------
    list
        "Officially" set requirements
    """
    imports = {}
    setup_py_file = [f for f in filepaths if f.endswith("setup.py")]
    if len(setup_py_file) > 0:
        print(setup_py_file)
        # TODO: parse setup.py
        # can be dangerous
        # look for 'install_requires'
        # ... may the force be with you
    else:
        logging.debug("Package '%s' has no setup.py. Strange.",
                      pkg_name)
    return imports


def get_imports(filepaths, pkg_name):
    """
    Get a list of all imported packages.

    Parameters
    ----------
    filepaths : list
        Paths to files of a package
    pkg_name : str
        Name of the currently parsed package.

    Returns
    -------
    dict
        Names of packages which got imported and how often
    """
    # TODO: Not all python files end with .py. We loose some.
    filepaths = [f for f in filepaths if f.endswith(".py")]
    simple_pattern = re.compile("^\s*import\s+([a-zA-Z][a-zA-Z0-9_]*)",
                                re.MULTILINE)
    from_pattern = re.compile("^\s*from\s+import\s+([a-zA-Z][a-zA-Z0-9_]*)",
                              re.MULTILINE)
    imports = {}
    for filep in filepaths:
        logging.info("Analyze '%s'...", filep)
        with open(filep) as f:
            content = f.read()

        imported = (simple_pattern.findall(content) +
                    from_pattern.findall(content))
        for import_pkg_name in imported:
            if import_pkg_name in imports:
                imports[import_pkg_name] += 1
            else:
                imports[import_pkg_name] = 1
    return imports


def get_parser():
    """The parser object for this script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--package_url",
                        dest="package_url",
                        help="write report to FILE",
                        required=True)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.package_url)
