#!/usr/bin/env python

"""Visualize with tsne as in https://indico.io/blog/visualizing-with-t-sne/."""

import numpy as np
import hasy_tools as ht
from matplotlib import pyplot as plt
from tsne import bh_sne

# load up data
dataset_path = './HASYv2'
ht._get_data(dataset_path)
data_complete = []

symbol_id2index = ht.generate_index("%s/symbols.csv" % dataset_path)
x_data, y_data, _ = ht.load_images('HASYv2/hasy-data-labels.csv',
                                   symbol_id2index,
                                   one_hot=False)

# convert image data to float64 matrix. float64 is need for bh_sne
x_data = np.asarray(x_data).astype('float64')
x_data = x_data.reshape((x_data.shape[0], -1))

# For speed of computation, only run on a subset
n = 20000
x_data = x_data[:n]
y_data = y_data[:n]

# perform t-SNE embedding
vis_data = bh_sne(x_data)

# plot the result
vis_x = vis_data[:, 0]
vis_y = vis_data[:, 1]

plt.scatter(vis_x, vis_y, c=y_data, cmap=plt.cm.get_cmap("viridis", 369))
plt.colorbar(ticks=range(369))
# plt.clim(-0.5, 9.5)
filename = '{}.pdf'.format('tsne')
plt.savefig(filename)
