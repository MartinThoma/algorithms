#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Analysis of Python packages."""

import json
import os
from os import walk
import pymysql.cursors
import re
import shutil
import tarfile
import logging
import sys

if sys.version_info[0] == 2:
    from urllib import urlretrieve
else:
    from urllib.request import urlretrieve

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main(package_name, package_url, release_id=None):
    """
    Parameters
    ----------
    package_name : str
    package_url : str
        Path to a Python package.
    package_id : int, optional
    """
    pkg_name = package_name
    if release_id is None:
        raise NotImplementedError("Look up the release id.")
    filepaths, download_dir = download(package_url)
    if download_dir is None:
        return
    with open("secret.json") as f:
        mysql = json.load(f)
    package_id = get_pkg_id_by_name(pkg_name, mysql)
    if package_id is None:
        logging.info("Package id of '%s' could not be determined", pkg_name)
        sys.exit(1)
    required_packages = get_requirements(filepaths, pkg_name)
    imported_packages = get_imports(filepaths, pkg_name)
    setup_packages = get_setup_packages(filepaths, pkg_name)
    store_dependencies(mysql,
                       package_id,
                       required_packages,
                       imported_packages,
                       setup_packages,
                       package_url,
                       release_id)
    remove_unpacked(download_dir)


def store_dependencies(mysql,
                       package_id,
                       required_packages,
                       imported_packages,
                       setup_packages,
                       package_url,
                       release_id):
    """
    Parameters
    ----------
    mysql : dict
        MySQL database connection information
    package_id : int
    required_packages : list
    imported_packages : list
    setup_packages : list
    package_url : str
    release_id : int
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')

    insert_dependency_db(imported_packages,
                         'imported',
                         package_id,
                         mysql,
                         connection)
    insert_dependency_db(required_packages,
                         'requirements.txt',
                         package_id,
                         mysql,
                         connection)
    insert_dependency_db(setup_packages,
                         'setup.py',
                         package_id,
                         mysql,
                         connection)
    # Store that the package was downloaded
    # and analyzed
    cursor = connection.cursor()
    sql = "UPDATE `releases` SET `downloaded_bytes` = %s WHERE `id` = %s;"
    pkg_name = os.path.basename(package_url)
    target_dir = "pypipackages"
    target = os.path.join(target_dir, pkg_name)
    downloaded_bytes = os.path.getsize(target)
    cursor.execute(sql, (downloaded_bytes, release_id))
    connection.commit()
    cursor.close()
    connection.close()


def insert_dependency_db(imported_packages,
                         req_type,
                         package_id,
                         mysql,
                         connection):
    """
    Parameters
    ----------
    imported_packages : list
    req_type : str
        'setup.py', 'requirements.txt' or 'imported'
    package_id : int
    mysql : dict
        credentials for the connection
    connection : pymysql connection object
    """
    cursor = connection.cursor()
    for pkg, times in imported_packages.items():
        package_info = {'package': package_id,
                        'needs_package': get_pkg_id_by_name(pkg, mysql),
                        'times': times,
                        'req_type': req_type}
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
            # Packages which were imported, but not found on PyPI
            # TODO: This still needs work. 21737 imports were not found on PyPI
            # amongst them:
            # mysqlDB
            # mySQLdb
            # MySQLdb
            with open("not-found.csv", "a") as f:
                f.write("%s\n" % pkg)


def get_pkg_id_by_name(pkg_name, mysql):
    """
    Parameters
    ----------
    pkg_name : str
    mysql : dict
        MySQL database connection information

    Returns
    -------
    int or None
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    cursor = connection.cursor()
    sql = "SELECT id FROM `packages` WHERE `name` = %s"
    cursor.execute(sql, (pkg_name, ))
    id_number = cursor.fetchone()
    if id_number is not None and 'id' in id_number:
        return id_number['id']
    else:
        return None


def get_pkg_extension(package_url):
    """
    Parameters
    ----------
    package_url : str

    Returns
    -------
    str
        File extension of the package given by url
    """
    not_implemented_fileending = [".msi", ".rpm", ".deb", ".tgz", ".dmg"]
    if package_url.endswith(".tar.gz"):
        return ".tar.gz"
    elif package_url.endswith(".tar.bz"):
        return ".tar.bz"
    elif package_url.endswith(".tar.bz2"):
        return ".tar.bz2"
    elif package_url.endswith(".whl"):
        return ".whl"
    elif package_url.endswith(".zip"):
        return ".zip"
    elif package_url.endswith(".egg"):
        return ".egg"
    elif package_url.endswith(".exe"):
        logging.info("Skip '%s' for safty reasons.", package_url)
        return None
    elif any(package_url.endswith(x) for x in not_implemented_fileending):
        pass  # TODO: Implement
    else:
        with open("todo-unknown-pkg-extension.csv", "a") as f:
            f.write("%s\n" % package_url)
        return None


def download(package_url):
    """
    Parameters
    ----------
    package_url : str
        URL of a Python package

    Returns
    -------
    tuple
        (List of paths to all unpackaged files, folder where it got extracted)
    """
    extension = get_pkg_extension(package_url)
    if extension is None:
        return ([], None)
    file_ending_len = len(extension)

    target_dir = "pypipackages"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    pkg_name = os.path.basename(package_url)
    target = os.path.join(target_dir, pkg_name)

    if not os.path.exists(target):
        try:
            urlretrieve(package_url, target)
            logging.info("Package '%s' downloaded.", pkg_name)
        except:
            return ([], None)
    else:
        pass
        # logging.info("Package '%s' was already downloaded.", pkg_name)

    # Unpack it
    if not os.path.exists(target[:-file_ending_len]):
        is_tarfile = (package_url.endswith(".tar.gz")
                      or package_url.endswith(".tar.bz")
                      or package_url.endswith(".tar.bz2"))
        if is_tarfile:
            try:
                with tarfile.open(target) as tar:
                    tar.extractall(target[:-file_ending_len])
            except:
                # Something is wrong with the tar file
                return ([], None)
        elif (package_url.endswith(".whl") or package_url.endswith(".zip") or
              package_url.endswith(".egg")):
            import zipfile
            try:
                with zipfile.ZipFile(target) as tar:
                    tar.extractall(target[:-file_ending_len])
            except:
                # Something is wrong with the zip file
                return ([], None)
        else:
            raise NotImplementedError

    filepaths = []
    for (dirpath, dirnames, filenames) in walk(target[:-file_ending_len]):
        filepaths.extend([os.path.join(dirpath, f) for f in filenames])
    return (filepaths, target[:-file_ending_len])


def remove_unpacked(download_dir):
    """
    Clean up the folders to prevent HDD of getting full.
    """
    shutil.rmtree(download_dir)


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
    requirements_file = [f for f in filepaths
                         if f.endswith("requirements.txt")]

    if len(requirements_file) > 0:
        requirements_file = requirements_file[0]
        # TODO: parse requirements.txt
    else:
        # logging.debug("Package '%s' has no requirements.txt.",
        #               pkg_name)
        pass
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
        try:
            with open(filep) as f:
                content = f.read()
        except:
            # there is something wrong with a file encoding. Or the file cannot
            # be opened
            # Ignore it.
            return imports

        imported = (simple_pattern.findall(content) +
                    from_pattern.findall(content))
        for import_pkg_name in imported:
            if import_pkg_name in imports:
                imports[import_pkg_name] += 1
            else:
                imports[import_pkg_name] = 1
    return imports


def get_setup_packages(filepaths, pkg_name):
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
    setup_py_file = [f for f in filepaths if f.endswith("setup.py")]
    imports = {}
    if len(setup_py_file) > 0:
        setup_py_file = setup_py_file[0]
        # logging.info(setup_py_file)
        # TODO: parse setup.py
        # can be dangerous
        # look for 'install_requires' and 'dependency_links'
        # ... may the force be with you

        # RegEx is complicated:
        # setup\(.*?(install_requires\s*=\s*\[.*?").*?\)  <--- doesn't work,
        # as you can have variables
    else:
        # logging.debug("Package '%s' has no setup.py.",
        #               pkg_name)
        pass
    logging.debug
    return imports


def get_parser():
    """The parser object for this script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--name",
                        dest="name",
                        help="name of the package",
                        required=True)
    parser.add_argument("-p", "--package_url",
                        dest="package_url",
                        help="url where the package is",
                        required=True)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.name, args.package_url)
