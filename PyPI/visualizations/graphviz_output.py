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


def main(filename, n):
    """
    Fetch data from server and create the graphviz data.

    Parameters
    ----------
    filename : str
        The path where the doftile gets written to.
    n : int
        The number of nodes it may have. None for all nodes.
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
    logging.info("Start writing graphviz file...")
    create_graphviz(filename, packages, dependencies, n)


def create_graphviz(filename, packages, dependencies, n):
    """
    Parameters
    ----------
    filename : str
        Path to the file where the GraphViz data will be stored.
    packages: list of dicts
        Each dict represents a package. It has the keys 'id' and 'name'
    dependencies : list of dicts
        Each dict has the keys 'package', 'needs_package' and 'times'
    n : int
        The number of nodes it may have. None for all nodes.
    """
    with open(filename, "w") as f:
        # digraph is for "directed graph"
        f.write("digraph python_package_dependencies {\n")
        # f.write("rankdir=LR;\n")
        # f.write('size="8,5"\n')

        pkg_ids = []
        for pkg in packages[:n]:
            f.write('\tnode [shape = point, label="%s"]; %i\n' % (pkg['name'],
                                                                  pkg['id']))
            pkg_ids.append(pkg['id'])
        f.write("\n")
        for dep in dependencies:
            if dep['needs_package'] in pkg_ids and dep['package'] in pkg_ids:
                f.write('\t%i -> %i;\n' %
                        (dep['needs_package'], dep['package']))
        f.write("}")


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        help="write doftile to FILE",
                        default="graphviz.dot",
                        metavar="FILE")
    parser.add_argument("-n",
                        dest="n",
                        type=int,
                        help="how many nodes the graph will have")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.filename, args.n)
