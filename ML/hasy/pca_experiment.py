#!/usr/bin/env python

import hasy_tools as ht
from sklearn.decomposition import PCA
import itertools as it

dataset_path = './HASYv2'
symbol_id2index = ht.generate_index(dataset_path)
data, y = ht.load_images(dataset_path,
                         'hasy-train-labels.csv',
                         symbol_id2index,
                         one_hot=False)
data = data.reshape(data.shape[0], data.shape[1] * data.shape[2])
X = data
print(data.shape)

# Do PCA
pca = PCA()
pca.fit(data)
sum_ = 0.0
done_values = [None, None, None]
done_points = [False, False, False]
chck_points = [0.9, 0.95, 0.99]
print(pca.explained_variance_ratio_)
print(sum(pca.explained_variance_ratio_))
for counter, el in enumerate(pca.explained_variance_ratio_):
    sum_ += el
    for check_point, done, i in zip(chck_points, done_points, it.count()):
        if not done and sum_ >= check_point:
            done_points[i] = counter
            done_values[i] = sum_
print(chck_points)
print(done_points)
print(done_values)
