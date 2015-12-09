#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Graph for small Collatz sequences"""

# Based on: http://en.wikipedia.org/wiki/File:Collatz-graph-all-30-no27.svg


def f(n):
    """
    Calculate the next step in the Collatz sequence.

    Parameters
    ----------
    n : int

    Returns
    -------
    int
    """
    if n % 2 == 0:
        return n / 2
    else:
        return 3*n + 1


def write_dotfile(filename, limit, explored):
    """
    Write a dotfile.

    Parameters
    ----------
    filename : str
    limit : int
        Number to which all numbers below will be tested
    explored : container
    """
    dotfile = file(filename, 'w')

    dotfile.write('digraph {\n')
    dotfile.write('node[style=filled,color=".7 .3 1.0"];\n')
    dotfile.write('1\n')
    dotfile.write('node[style=filled,color=".95 .1 1"];\n')
    # dotfile.write('size="15,8";\n')

    for n in range(2, limit):
        while n not in explored:
            dotfile.write(str(n) + ' -> ')
            explored.add(n)
            n = f(n)
        dotfile.write(str(n) + ';\n')
    dotfile.write('}\n')


def create_png(dotfile, base, program):
    """
    Parameters
    ----------
    dotfile : str
        Name of the dotfile
    base : str
        Name of the resulting svg file without extension
    program : str
        Program to generate the svg
    """
    import os
    command = program + " -Tsvg " + dotfile + " -o " + base + ".svg"
    print("Execute command: %s" % command)
    os.system(command)

    command = "inkscape "+base+".svg"+" -w 512 --export-png="+base+".png"
    print("Execute command: %s" % command)
    os.system(command)


def get_parser():
    """Get parser object."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file", dest="filename",
                        default="collatz-graph.gv",
                        help="write dot-FILE", metavar="FILE")
    parser.add_argument("-p", "--program", dest="program",
                        help="dot, neato, twopi, circo, fdp, sfdp, osage",
                        metavar="PROGRAM", default="dot")
    parser.add_argument("-n",
                        dest="limit", default=20, type=int,
                        help="limit")
    return parser


if __name__ == "__main__":
    args = get_parser()
    write_dotfile(args.filename, args.limit, set([1]))
    import os
    create_png(args.filename, os.path.splitext(args.filename)[0], args.program)
