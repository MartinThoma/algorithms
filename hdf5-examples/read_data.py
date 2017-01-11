#!/usr/bin/env python
import h5py
filename = 'file.hdf5'
f = h5py.File(filename, 'r')

# List all groups
print("Keys: %s" % f.keys())
a_group_key = f.keys()[0]

# Get the data
data = list(f[a_group_key])
print(data)
