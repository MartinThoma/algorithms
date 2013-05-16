#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on: http://en.wikipedia.org/wiki/File:Collatz-graph-all-30-no27.svg

def f(n):
    if n % 2 == 0:
        return n / 2
    else:
        return 3*n + 1

def writeDotfile(filename, limit, explored):
    dotfile = file(filename, 'w')

    dotfile.write('digraph {\n')
    dotfile.write('node[style=filled,color=".7 .3 1.0"];\n')
    dotfile.write('1\n')
    dotfile.write('node[style=filled,color=".95 .1 1"];\n')
    #dotfile.write('size="15,8";\n')

    for n in range(2, limit):
        while n not in explored:
            dotfile.write(str(n) + ' -> ')
            explored.add(n)
            n = f(n)
        dotfile.write(str(n) + ';\n')
    dotfile.write('}\n')

def createPng(dotfile, base, program):
    import os
    command = program + " -Tsvg " + dotfile + " -o " + base + ".svg"
    print("Execute command: %s" % command)
    os.system(command)

    command = "inkscape "+base+".svg"+" -w 512 --export-png="+base+".png"
    print("Execute command: %s" % command)
    os.system(command)

if __name__ == "__main__":
    import argparse
 
    parser = argparse.ArgumentParser(
        description="Graph for small Collatz sequences"
    )
    parser.add_argument("-f", "--file", dest="filename",
                        default="collatz-graph.gv",
                        help="write dot-FILE", metavar="FILE")
    parser.add_argument("-p", "--program", dest="program",
                  help="dot, neato, twopi, circo, fdp, sfdp, osage", 
                  metavar="PROGRAM", default="dot")
    parser.add_argument("-n", 
                      dest="limit", default=20, type=int, 
                      help="limit")
    args = parser.parse_args()
    
    writeDotfile(args.filename, args.limit, set([1]))
    import os
    createPng(args.filename, os.path.splitext(args.filename)[0], args.program)
