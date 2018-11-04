#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Visualize validation curve."""

import pandas as pd
import matplotlib.pyplot as plt

Y_SCALE_FACTOR = 100

# Prepare dataframe
df = pd.read_csv('log.csv', sep=';')
df = df[['epoch', 'acc', 'val_acc']]
df[['acc', 'val_acc']] = df[['acc', 'val_acc']] * Y_SCALE_FACTOR
df = df.set_index('epoch').rename(columns={'acc': 'Training Accuracy',
                                           'val_acc': 'Validation Accuracy'})
print(df)

# Plot
fig, ax = plt.subplots()
df.plot.line(ylim=(0.65 * Y_SCALE_FACTOR, 0.85 * Y_SCALE_FACTOR),
             title='Validation Curve',
             ax=ax)
ax.minorticks_on()  # required for minor grid
ax.grid()
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
plt.savefig('validation-curve.png', dpi=300)
