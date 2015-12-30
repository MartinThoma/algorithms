#!/usr/bin/env python

"""
Generate a dotfile for Python module dependencies.
"""

import json
import pymysql
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def main(filename):
    """
    Fetch data from server and create the graphviz data.

    Parameters
    ----------
    filename : str
        The path where the doftile gets written to.
    """
    with open("../secret.json") as f:
        mysql = json.load(f)
    connection = pymysql.connect(host=mysql['host'],
                                 user=mysql['user'],
                                 passwd=mysql['passwd'],
                                 db=mysql['db'],
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8')
    cursor = connection.cursor()
    logging.info("Start fetching data from server...")
    sql = ("SELECT `id`, `name` FROM `packages`")
    cursor.execute(sql)
    packages = cursor.fetchall()
    sql = ("SELECT `package`, `needs_package`, `times` FROM `dependencies`")
    cursor.execute(sql)
    dependencies = cursor.fetchall()
    logging.info("Start writing json file...")
    store_json(filename,
               packages,
               dependencies)


def store_json(filename,
               packages,
               dependencies):
    """
    Parameters
    ----------
    filename : str
        Path to the file where the GraphViz data will be stored.
    packages: list of dicts
        Each dict represents a package. It has the keys 'id' and 'name'
    dependencies : list of dicts
        Each dict has the keys 'package', 'needs_package' and 'times'
    """
    meta = {'pypi_data_date': '2015-12-06',
            'data_src': 'https://github.com/MartinThoma/pypi-dependencies',
            'about': 'http://martin-thoma.com/analyzing-pypi-metadata/'}

    for dep_dict in dependencies:
        dep_dict['needs_pkg'] = dep_dict.pop('needs_package')
        dep_dict['pkg'] = dep_dict.pop('package')
        dep_dict['type'] = 'import'

    with open(filename, "w") as f:
        data = {'packages': packages,
                'dependencies': dependencies,
                'meta': meta,
                'software_repository':
                    'git@github.com:MartinThoma/algorithms.git',
                'software_version': '426f07db7a2cb392fbd25417b4889a636c30a313',
                'software_readme': 'The software is in the folder "PyPI".'}
        json.dump(data, f, indent=2)


def get_parser():
    """Get the parser object for the store_json script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        help="write data to this JSONFILE",
                        default="pypi_dependency_pkg_data.json",
                        metavar="FILE")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.filename)
