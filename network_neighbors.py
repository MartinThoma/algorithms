#!/usr/bin/env python

"""List all hosts with their IP adress of the current network."""

import os

out = os.popen('ip neigh').read().splitlines()
for i, line in enumerate(out, start=1):
    ip = line.split(' ')[0]
    h = os.popen('host {}'.format(ip)).read()
    hostname = h.split(' ')[-1]
    print("{:>3}: {} ({})".format(i, hostname.strip(), ip))
