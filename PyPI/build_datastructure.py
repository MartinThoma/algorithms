#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Get information about all projects on PyPI."""

import urllib
from urllib.request import urlopen
from xml.etree import ElementTree
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import json
import pymysql.cursors
import threading
import time


def in_parallel(target, job_list, mysql):
    for package_name_link, package_name in job_list:
        if threading.active_count() > 32:
            time.sleep(1)  # delays for 1 second
        threading.Thread(target=target,
                         args=(package_name_link, package_name, mysql)).start()


def get_package_names(simple_index='https://pypi.python.org/simple/'):
    """
    Returns
    -------
    list
        Names of all packages.
    """
    f = urlopen(simple_index)
    tree = ElementTree.parse(f)
    f.close()
    return [(a.attrib['href'], a.text) for a in tree.iter('a')]


def get_package_info(package_name='numpy'):
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
        f = urlopen("https://pypi.python.org/pypi/%s/json" % package_name)
    except urllib.error.HTTPError as e:
        logging.error("'%s' gave %s", package_name, str(e))
        return None
    content = f.read()
    f.close()
    return json.loads(content.decode("utf-8"))


def insert_package_info(package_name, package_info, mysql):
    """
    Insert the package information into a MySQL database.

    Parameters
    ----------
    package_info : dict
    mysql : dict
        MySQL database connection information
    """
    releases = package_info['releases']
    url_entries = package_info['urls']
    package_info = package_info['info']
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    for key in package_info:
        package_info[key] = str(package_info[key])
        package_info[key] = connection.escape_string(package_info[key])
        if key in ['cheesecake_installability_id',
                   'cheesecake_documentation_id',
                   'cheesecake_code_kwalitee_id']:
            package_info[key] = package_info[key].replace('None', 'NULL')
        if key == '_pypi_hidden':
            package_info[key] = package_info[key].replace('True', '1')
            package_info[key] = package_info[key].replace('False', '0')

    if 'stable_version' not in package_info:
        package_info['stable_version'] = "UNKNOWN"

    cursor = connection.cursor()
    sql = ("INSERT INTO `packages` (`maintainer`, "
           "`docs_url`, `requires_python`, `maintainer_email`, "
           "`cheesecake_code_kwalitee_id`, `keywords`, `package_url`, "
           "`author`, `author_email`, `download_url`, `platform`, `version`, "
           "`cheesecake_documentation_id`, `_pypi_hidden`, `description`, "
           "`release_url`, `_pypi_ordering`, `name`, `bugtrack_url`, "
           "`license`, `summary`, `home_page`, `stable_version`, "
           "`cheesecake_installability_id`) VALUES "
           "('{maintainer}', '{docs_url}', '{requires_python}', "
           "'{maintainer_email}', {cheesecake_code_kwalitee_id}, "
           "'{keywords}', '{package_url}', '{author}', '{author_email}', "
           "'{download_url}', '{platform}', '{version}', "
           "{cheesecake_documentation_id}, '{_pypi_hidden}', "
           "'{description}', '{release_url}', '{_pypi_ordering}', '{name}', "
           "'{bugtrack_url}', '{license}', '{summary}', '{home_page}', "
           "'{stable_version}', {cheesecake_installability_id});").format(
        **package_info)
    try:
        cursor.execute(sql)
        connection.commit()
        was_successful = True
    except pymysql.err.IntegrityError as e:
        logging.warning(("Package '%s' is probably already in the database "
                         "as '%s'"),
                        package_name, package_info['name'])
        if 'Duplicate entry' not in str(e):
            logging.warning(e)
        was_successful = False

    if was_successful:
        # Get id
        db_package_id = is_package_in_database(package_info['name'], mysql)

        # Enter releases
        for release_number, release_all in releases.items():
            for release in release_all:
                # e.g.
                # https://pypi.python.org/pypi/agoraplex.themes.sphinx/json
                # has one release number, but multiple releases for that
                # number ... strange
                for key in release:
                    release[key] = str(release[key])
                    release[key] = connection.escape_string(release[key])
                    if key == 'has_sig':
                        release[key] = release[key].replace('True', '1')
                        release[key] = release[key].replace('False', '0')
                release['package_id'] = db_package_id
                release['release_number'] = release_number
                sql = ("INSERT INTO `releases` (`package_id`, "
                       "`release_number`, "
                       "`has_sig`, `upload_time`, `comment_text`, "
                       "`python_version`, `url`, `md5_digest`, `downloads`, "
                       "`filename`, `packagetype`, `size`) VALUES "
                       "('{package_id}', '{release_number}', {has_sig}, "
                       "'{upload_time}', '{comment_text}', "
                       "'{python_version}', "
                       "'{url}', '{md5_digest}', '{downloads}', '{filename}', "
                       "'{packagetype}', '{size}');").format(**release)
                cursor.execute(sql)
        connection.commit()

        # Enter URLs
        for url_entry in url_entries:
            for key in url_entry:
                url_entry[key] = str(url_entry[key])
                url_entry[key] = connection.escape_string(url_entry[key])
                if key == 'has_sig':
                    url_entry[key] = url_entry[key].replace('True', '1')
                    url_entry[key] = url_entry[key].replace('False', '0')
            url_entry['package_id'] = db_package_id
            sql = ("INSERT INTO `urls` (`package_id`, `has_sig`, "
                   "`upload_time`, `comment_text`, `python_version`, `url`, "
                   "`md5_digest`, `downloads`, `filename`, `packagetype`, "
                   "`size`) VALUES "
                   "('{package_id}', {has_sig}, '{upload_time}', "
                   "'{comment_text}', '{python_version}', '{url}', "
                   "'{md5_digest}', '{downloads}', '{filename}', "
                   "'{packagetype}', '{size}');").format(**url_entry)
            cursor.execute(sql)
        connection.commit()

        # Enter classifiers:
        try:
            package_info['classifiers'] = \
                package_info['classifiers'].replace("\\'", '"')
            package_info['classifiers'] = json.loads(
                package_info['classifiers'])
        except ValueError:
            logging.error("Could not parse classifier of package '%s'",
                          package_name)
            logging.error("Classifier: %s", package_info['classifiers'])
        for classifier in package_info['classifiers']:
            classifier = connection.escape_string(classifier)
            sql = ("INSERT INTO `package_classifiers` (`package_id`, "
                   "`classifier`) VALUES ('{package_id}', "
                   "'{classifier}');").format(package_id=db_package_id,
                                              classifier=classifier)
            cursor.execute(sql)
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
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    cursor = connection.cursor()
    escaped_name = connection.escape_string(name)
    sql = "SELECT id FROM `packages` WHERE `name` = '%s'" % escaped_name
    cursor.execute(sql)
    id_number = cursor.fetchone()
    connection.close()
    if id_number is not None and 'id' in id_number:
        id_number = id_number['id']
    return id_number


def handle_package(package_name_link, package_name, mysql):
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
        logging.info("Package '%s' already in database. Continue.",
                     package_name)
        return
    logging.info("Load '%s'..." % package_name_link)
    package_info = get_package_info(package_name_link)
    if package_info is None:
        return
    insert_package_info(package_name, package_info, mysql)


def main():
    logging.info("Get package names. This takes about 50 seconds...")
    package_names = get_package_names()
    logging.info("%i packages found.", len(package_names))

    with open("secret.json") as f:
        mysql = json.load(f)

    in_parallel(handle_package, package_names, mysql)
    # for package_name_link, package_name in package_names:
    #     handle_package(package_name_link, package_name, mysql)

if __name__ == '__main__':
    main()
