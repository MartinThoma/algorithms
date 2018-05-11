#!/usr/bin/env python

import seaborn as sns

for palette in ['deep', 'muted', 'pastel', 'bright', 'dark', 'colorblind']:
    current_palette = sns.color_palette(palette)
    sns.palplot(current_palette)
    sns.plt.savefig('{}.png'.format(palette))
