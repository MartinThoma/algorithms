## General

A perceptron is a linear, binary classifier. Hence the target labels are `0`
and `1`. This perceptron can be executed on the MNIST dataset and recognize if
an input image (28 pixel x 28 pixel) is a "3" or not:

```
./perceptron.py
2016-11-18 16:01:09,551 INFO Epoch: 1 (Validation acc: 10.3333%)
2016-11-18 16:01:10,163 INFO Epoch: 2 (Validation acc: 97.0635%)
2016-11-18 16:01:10,772 INFO Epoch: 3 (Validation acc: 97.2063%)
2016-11-18 16:01:11,375 INFO Epoch: 4 (Validation acc: 97.0794%)
2016-11-18 16:01:11,985 INFO Epoch: 5 (Validation acc: 96.9048%)
2016-11-18 16:01:12,584 INFO Epoch: 6 (Validation acc: 97.0952%)
2016-11-18 16:01:13,188 INFO Epoch: 7 (Validation acc: 96.8095%)
2016-11-18 16:01:13,795 INFO Epoch: 8 (Validation acc: 96.6825%)
2016-11-18 16:01:14,402 INFO Epoch: 9 (Validation acc: 97.0476%)
2016-11-18 16:01:15,006 INFO Epoch: 10 (Validation acc: 96.4921%)
```

## Requirements

You have to install two 3rd-party packages: `numpy` and `scikit-learn`.

### Numpy

You might have to install numpy manually. Please follow the
[official guide](http://docs.scipy.org/doc/numpy/user/install.html) to do so.

### Scikit-learn

Scikit-learn is also called sklearn. Don't be confused by that, it is the same
package. Please follow the
[official guide](http://scikit-learn.org/stable/install.html) to
install it.
