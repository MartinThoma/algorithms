#!/usr/bin/env python

"""List all hosts with their IP adress of the current network."""

import os

out = os.popen('ip neigh').read().splitlines()
for i, line in enumerate(out, start=1):
    ip = line.split(' ')[0]
    h = os.popen(f'host {ip}').read()
    hostname = h.split(' ')[-1]
    print(f"{i:>3}: {hostname.strip()} ({ip})")
