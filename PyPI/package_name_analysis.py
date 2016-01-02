#!/usr/bin/env python3

"""Analyze the package names of PyPI."""

import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import json
import pymysql.cursors


def get_package_names(mysql):
    """
    Parameters
    ----------
    mysql: str
        connection string

    Returns
    -------
    list
        dicts {id, package name}
    """
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    cursor = connection.cursor()
    sql = "SELECT id, name FROM `packages`"
    cursor.execute(sql)
    packages = cursor.fetchall()
    return packages


def prefix_analysis(pkg_names):
    """
    Parameters
    ----------
    pkg_names : list
        dicts {'id', 'name'}
    """
    prefix_tree = {}
    for pkg in pkg_names:
        current_node = prefix_tree
        for char in pkg['name']:
            if char in current_node:
                current_node = current_node[char]
            else:
                current_node[char] = {}
                current_node = current_node[char]
        current_node['package'] = True

    # Now traverse tree - if a 'package' node is not a leaf, then this is a
    # prefix
    i = 1
    short_packages = set()
    is_prefix_of = {}
    prefixed_by = {}
    for pkg in pkg_names:
        current_node = prefix_tree
        current_str = ""
        prefix_msgs = []
        for char in pkg['name']:
            current_str += char
            current_node = current_node[char]
            if 'package' in current_node and current_str != pkg['name']:
                if len(current_str) <= 2:
                    short_packages.add(current_str)
                else:
                    msg = {'prefix': current_str, 'long': pkg['name']}
                    if current_str in is_prefix_of:
                        is_prefix_of[current_str].append(pkg['name'])
                    else:
                        is_prefix_of[current_str] = [pkg['name']]
                    if pkg['name'] in prefixed_by:
                        prefixed_by[pkg['name']].append(current_str)
                    else:
                        prefixed_by[pkg['name']] = [current_str]
                    prefix_msgs.append(msg)
        # if len(prefix_msgs) > 0 and len(current_node) == 1:
        #     for msg in prefix_msgs:
        #         msg = ("'%s' is prefix of '%s'." %
        #                (msg['prefix'], msg['long']))
        #         print("%i. %s" % (i, msg))
        #         i += 1

    is_prefix_top = [(pkg, len(pkg_list))
                     for pkg, pkg_list in is_prefix_of.items()]
    is_prefix_top = sorted(is_prefix_top,
                           reverse=True,
                           key=lambda n: n[1])
    print("## Packages which are prefixes of many packages:")
    for i, isptop in enumerate(is_prefix_top[:10], start=1):
        print("%i. %s: %i" % (i, isptop[0], isptop[1]))

    prefixed_by_top = [(pkg, len(pkg_list))
                       for pkg, pkg_list in prefixed_by.items()]
    prefixed_by_top = sorted(prefixed_by_top,
                             reverse=True,
                             key=lambda n: n[1])
    print("## Packages which prefixed by packages:")
    for i, isptop in enumerate(prefixed_by_top[:10], start=1):
        print("%i. %s: %i" % (i, isptop[0], isptop[1]))

    print("## Short package names: %i" % len(short_packages))


def main():
    """Orchestrate the package name analysis."""
    logging.info("Get package names...")
    with open("secret.json") as f:
        mysql = json.load(f)

    pkg_names = get_package_names(mysql)
    prefix_analysis(pkg_names)
    # for package_name_link, package_name in package_names:
    #     handle_package(package_name_link, package_name, mysql)

if __name__ == '__main__':
    main()
