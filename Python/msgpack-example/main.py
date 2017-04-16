#!/usr/bin/env python
# -*- coding: utf-8 -*-
import msgpack

# Define data
data = {'a list': [1, 42, 3.141, 1337, 'help'],
        'a string': 'bla',
        'another dict': {'foo': 'bar',
                         'key': 'value',
                         'the answer': 42}}

# Write msgpack file
with open('data.msgpack', 'w') as outfile:
    msgpack.pack(data, outfile)

# Read msgpack file
with open('data.msgpack') as data_file:
    # data_loaded = json.load(data_file)
    data_loaded = msgpack.unpack(data_file)

print(data == data_loaded)
