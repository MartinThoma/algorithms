If you want to force Keras to use CPU


## Way 1

    import os
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

before Keras / Tensorflow is imported.

## Way 2

Run your script as

    $ CUDA_VISIBLE_DEVICES="" ./your_keras_code.py

See also

1. https://github.com/keras-team/keras/issues/152
2. https://github.com/fchollet/keras/issues/4613
