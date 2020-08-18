#!/usr/bin/env python

import hasy

data = hasy.load_data()
print(f"n_classes={hasy.n_classes}")
print(f"labels={hasy.labels}")
print("## complete")
print("x.shape={:>20},\tx.dtype={}".format(data['x'].shape, data['x'].dtype))
print("x.shape={:>20},\tx.dtype={}".format(data['y'].shape, data['y'].dtype))
print("## fold-2")
data = hasy.load_data(mode='fold-2')
print("x_train.shape={:>20},\tx_test.shape={}".format(data['x_train'].shape,
                                                      data['x_test'].shape))
print("y_train.shape={:>20},\ty_test.shape={}".format(data['y_train'].shape,
                                                      data['y_test'].shape))
