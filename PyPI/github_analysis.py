#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find Python package on GitHub.
"""

import json
import pymysql
import requests
import logging
import sys
import re

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
logging.getLogger("requests").setLevel(logging.WARNING)


def main():
    """Orchestrate finding packages on GitHub."""
    with open("secret.json") as f:
        credentials = json.load(f)

    connection = pymysql.connect(host=credentials['host'],
                                 user=credentials['user'],
                                 passwd=credentials['passwd'],
                                 db=credentials['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    cursor = connection.cursor()

    sql = ("""SELECT
    `packages`.`id`,
    `name`,
    `home_page`,
    `stargazers_count`,
    `watchers_count`,
    `forks_count`
FROM
    `packages`
LEFT JOIN
    github ON `packages`.`id` = `github`.`id`
WHERE
    `license` LIKE '%MIT%'
    AND `summary` != ''
    AND `home_page` LIKE 'https://github.com/%'
    AND `github`.`stargazers_count` IS NULL
ORDER BY
    `name` ASC
""")
    cursor.execute(sql)
    logging.info("Get packages...")
    packages = cursor.fetchall()

    logging.info("Get stargazers...")
    get_stargazers(credentials, packages)


def get_stargazers(credentials, packages):
    """
    Parameters
    ----------
    credentials : dict
        connection string
    packages : list
    """

    pattern = re.compile("https://github.com/(.*?)/(.*)")
    highest = -1

    # gh = Github(login=credentials['github_username'],
    #             password=credentials['github_password'])

    for pkg in packages:
        matches = pattern.findall(pkg['home_page'])
        if len(matches) == 0:
            logging.info("No matches found for '%s'.", pkg['home_page'])
            continue
        matches = matches[0]
        r = requests.get("https://api.github.com/repos/%s/%s" % matches,
                         auth=(credentials['github_username'],
                               credentials['github_password']))
        github_repo_meta = json.loads(r.content)  # .decode('utf-8')
        if 'message' in github_repo_meta:
            if github_repo_meta['message'] == 'Not Found':
                logging.info("Not found: '%s'", pkg['home_page'])
                continue
            elif github_repo_meta['message'] == 'Bad credentials':
                print("Your credentials in secret.json are wrong.")
                sys.exit(-1)
            else:
                logging.debug(github_repo_meta)
                continue
        if 'stargazers_count' not in github_repo_meta:
            logging.info("stargazers_count not in github_repo_meta: '%s'",
                         pkg['home_page'])
            continue
        update_stargazers(credentials, pkg['id'], github_repo_meta)
        if github_repo_meta['stargazers_count'] > highest:
            logging.info("%s has %i stargazers.",
                         pkg['home_page'],
                         github_repo_meta['stargazers_count'])
            highest = github_repo_meta['stargazers_count']


def update_stargazers(mysql, pypi_internal_mysql_id, github_repo_meta):
    """
    Parameters
    ----------
    mysql : dict
        connection string
    pypi_internal_mysql_id : int
    github_repo_meta : int
    """
    # Connect to the database
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8mb4')

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = ("INSERT INTO `github` "
                   "(`id`, "
                   "`stargazers_count`, `watchers_count`, `forks_count`) "
                   "VALUES (%s, %s, %s, %s);")
            cursor.execute(sql, (pypi_internal_mysql_id,
                                 github_repo_meta['stargazers_count'],
                                 github_repo_meta['watchers_count'],
                                 github_repo_meta['forks_count']))
        connection.commit()
    finally:
        connection.close()


if __name__ == '__main__':
    main()
