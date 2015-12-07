#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pymysql
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

# mine
import package_analysis


def main():
    """
    Load the edges of the dependency graph by downloading PyPI.

    Yep. All of it. Make sure you have at least 50GB disk space.
    """
    with open("secret.json") as f:
        mysql = json.load(f)

    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    cursor = connection.cursor()
    sql = "SELECT `packages`.`id`, `name` FROM `packages` ORDER BY `id` ASC"
    cursor.execute(sql)
    packages = cursor.fetchall()
    for pkg in packages:
        sql = ("SELECT `url` FROM `releases` "
               "WHERE `package_id` = %s "
               "ORDER BY `upload_time` DESC LIMIT 1")
        cursor.execute(sql, (pkg['id'], ))
        url = cursor.fetchone()
        if url is not None and 'url' in url:
            package_url = url['url']
            package_analysis.main(pkg['name'], package_url)
            logging.info("Package '%s' done.", pkg['name'])


if __name__ == '__main__':
    main()
