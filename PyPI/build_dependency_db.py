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

    sql = ("""SELECT
    `o`.`id`,
    `packages`.`name`,
    `o`.`url`,
    `o`.`upload_time`,
    `o`.`release_number`,
    `o`.`downloaded_bytes`
FROM
    `releases` o
LEFT JOIN
    `releases` b  ON `o`.`package_id` = `b`.`package_id`
    AND `o`.`upload_time` < `b`.`upload_time`
Left JOIN
    `packages` ON `packages`.`id` = `o`.`package_id`
WHERE
    `b`.`upload_time` is NULL
    AND `o`.`downloaded_bytes` = 0
ORDER BY
    `packages`.`name`
""")
    cursor.execute(sql)
    packages = cursor.fetchall()
    logging.info("Fetched %i packages.", len(packages))
    for pkg in packages:
        package_analysis.main(pkg['name'], pkg['url'], pkg['id'])
        logging.info("Package '%s' done.", pkg['name'])


if __name__ == '__main__':
    main()
