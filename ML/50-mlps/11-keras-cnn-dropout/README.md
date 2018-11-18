## Purpose

This is copied from `08-keras-cnn`. Now I double the second last layers nodes
and train for 200 epochs.


## Results

```
16992/16992 [==============================] - 1s 42us/step

acc: 75.80%

real    7090,96s
user    8736,06s
sys    689,04s
```

Evaluation:

```
2018-11-18 16:58:55.309466: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:964] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2018-11-18 16:58:55.309922: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1432] Found device 0 with properties:
name: GeForce GTX TITAN Black major: 3 minor: 5 memoryClockRate(GHz): 0.98
pciBusID: 0000:01:00.0
totalMemory: 5.94GiB freeMemory: 5.79GiB
2018-11-18 16:58:55.309945: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1511] Adding visible gpu devices: 0
2018-11-18 16:58:55.537453: I tensorflow/core/common_runtime/gpu/gpu_device.cc:982] Device interconnect StreamExecutor with strength 1 edge matrix:
2018-11-18 16:58:55.537500: I tensorflow/core/common_runtime/gpu/gpu_device.cc:988]      0
2018-11-18 16:58:55.537508: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1001] 0:   N
2018-11-18 16:58:55.537701: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 5579 MB memory) -> physical GPU (device: 0, name: GeForce GTX TITAN Black, pci bus id: 0000:01:00.0, compute capability: 3.5)
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
conv2d_1 (Conv2D)            (None, 30, 30, 16)        160
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 15, 15, 16)        0
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 13, 13, 16)        2320
_________________________________________________________________
flatten_1 (Flatten)          (None, 2704)              0
_________________________________________________________________
dense_1 (Dense)              (None, 512)               1384960
_________________________________________________________________
dropout_1 (Dropout)          (None, 512)               0
_________________________________________________________________
dense_2 (Dense)              (None, 256)               131328
_________________________________________________________________
dense_3 (Dense)              (None, 369)               94833
=================================================================
Total params: 1,613,601
Trainable params: 1,613,601
Non-trainable params: 0
_________________________________________________________________
None
16992/16992 [==============================] - 1s 83us/step

acc: 76.67%
```
