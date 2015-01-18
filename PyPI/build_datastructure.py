#!/usr/bin/env python3

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
import pymysql
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
    f = urlopen(simple_index)
    tree = ElementTree.parse(f)
    f.close()
    return [(a.attrib['href'], a.text) for a in tree.iter('a')]


def get_package_info(package_name='numpy'):
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
    :param package_info: dictionary
    :param mysql: dictionary with mysql database connection information
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    for key in package_info:
        package_info[key] = str(package_info[key])
        package_info[key] = connection.escape_string(package_info[key])
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
           "'{maintainer_email}', '{cheesecake_code_kwalitee_id}', "
           "'{keywords}', '{package_url}', '{author}', '{author_email}', "
           "'{download_url}', '{platform}', '{version}', "
           "'{cheesecake_documentation_id}', '{_pypi_hidden}', "
           "'{description}', '{release_url}', '{_pypi_ordering}', '{name}', "
           "'{bugtrack_url}', '{license}', '{summary}', '{home_page}', "
           "'{stable_version}', '{cheesecake_installability_id}');").format(
        **package_info)
    try:
        cursor.execute(sql)
        connection.commit()
    except pymysql.err.IntegrityError as e:
        logging.warning(("Package '%s' is probably already in the database "
                         "as '%s'"),
                        package_name, package_info['name'])
        if 'Duplicate entry' not in str(e):
            logging.warning(e)
    connection.close()


def is_package_in_database(name, mysql):
    """
    :param package_name: string
    :param mysql: dictionary with mysql database connection information
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
    ids = cursor.fetchall()
    connection.close()
    return ids


def handle_package(package_name_link, package_name, mysql):
    answer = is_package_in_database(package_name, mysql)
    if len(answer) == 1:
        logging.info("Package '%s' already in database. Continue.",
                     package_name)
        return
    logging.info("Load '%s'..." % package_name_link)
    package_info = get_package_info(package_name_link)
    if package_info is None:
        return
    insert_package_info(package_name, package_info['info'], mysql)


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
