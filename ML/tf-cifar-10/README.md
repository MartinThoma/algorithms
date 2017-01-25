Read [the tutorial](https://www.tensorflow.org/tutorials/deep_cnn/) for more
information.

* cifar10.py: Builds the CIFAR-10 model.
* cifar10_input.py: Reads the native CIFAR-10 binary file format.
* cifar10_train.py: Trains a CIFAR-10 model on a CPU or GPU.
* cifar10_eval.py: Evaluates the predictive performance of a CIFAR-10 model.


## Requirements

Install (in this order):

* CUDA 8: [instructions](http://askubuntu.com/a/799185/10425)
* CuDNN 5.1: [instructions](http://stackoverflow.com/a/36978616/562769)
* Tensorflow: [instructions](https://www.tensorflow.org/get_started/os_setup)


## Usage examples

```
$ python cifar10_train.py --help
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcublas.so locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcudnn.so locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcufft.so locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcuda.so.1 locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcurand.so locally
usage: cifar10_train.py [-h] [--batch_size BATCH_SIZE] [--data_dir DATA_DIR]
                        [--use_fp16 [USE_FP16]] [--nouse_fp16]
                        [--train_dir TRAIN_DIR] [--max_steps MAX_STEPS]
                        [--log_device_placement [LOG_DEVICE_PLACEMENT]]
                        [--nolog_device_placement]

optional arguments:
  -h, --help            show this help message and exit
  --batch_size BATCH_SIZE
                        Number of images to process in a batch.
  --data_dir DATA_DIR   Path to the CIFAR-10 data directory.
  --use_fp16 [USE_FP16]
                        Train the model using fp16.
  --nouse_fp16
  --train_dir TRAIN_DIR
                        Directory where to write event logs and checkpoint.
  --max_steps MAX_STEPS
                        Number of batches to run.
  --log_device_placement [LOG_DEVICE_PLACEMENT]
                        Whether to log device placement.
  --nolog_device_placement

```

Now run it:

```
$ mkdir checkpoints
$ mkdir data
$ python cifar10_train.py --max_steps 200 --train_dir checkpoints --data_dir data
```

If you want to know how good your model is:

```
$ python cifar10_eval.py --eval_data test --data_dir data --checkpoint_dir checkpoints
```


## How it looks like when it works

```
$ python cifar10_train.py
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcublas.so locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcudnn.so locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcufft.so locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcuda.so.1 locally
I tensorflow/stream_executor/dso_loader.cc:128] successfully opened CUDA library libcurand.so locally
Filling queue with 20000 CIFAR images before starting to train. This will take a few minutes.
I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:937] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
I tensorflow/core/common_runtime/gpu/gpu_device.cc:885] Found device 0 with properties: 
name: GeForce 940MX
major: 5 minor: 0 memoryClockRate (GHz) 1.2415
pciBusID 0000:02:00.0
Total memory: 1.96GiB
Free memory: 1.62GiB
I tensorflow/core/common_runtime/gpu/gpu_device.cc:906] DMA: 0 
I tensorflow/core/common_runtime/gpu/gpu_device.cc:916] 0:   Y 
I tensorflow/core/common_runtime/gpu/gpu_device.cc:975] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce 940MX, pci bus id: 0000:02:00.0)
2017-01-02 14:48:39.431956: step 0, loss = 4.67 (11.7 examples/sec; 10.899 sec/batch)
2017-01-02 14:48:41.670052: step 10, loss = 4.62 (712.7 examples/sec; 0.180 sec/batch)
2017-01-02 14:48:43.460929: step 20, loss = 4.44 (745.9 examples/sec; 0.172 sec/batch)
2017-01-02 14:48:45.253523: step 30, loss = 4.45 (726.7 examples/sec; 0.176 sec/batch)
2017-01-02 14:48:47.051605: step 40, loss = 4.29 (736.8 examples/sec; 0.174 sec/batch)
2017-01-02 14:48:48.860873: step 50, loss = 4.28 (732.6 examples/sec; 0.175 sec/batch)
2017-01-02 14:48:50.668181: step 60, loss = 4.34 (737.7 examples/sec; 0.174 sec/batch)
2017-01-02 14:48:52.589918: step 70, loss = 4.27 (722.0 examples/sec; 0.177 sec/batch)
2017-01-02 14:48:54.495558: step 80, loss = 4.24 (676.8 examples/sec; 0.189 sec/batch)
2017-01-02 14:48:56.395373: step 90, loss = 3.98 (726.1 examples/sec; 0.176 sec/batch)
2017-01-02 14:48:58.305380: step 100, loss = 4.10 (549.3 examples/sec; 0.233 sec/batch)
```

You can see that 100 steps need about 19 seconds on my Laptop. It will make
100K steps => 19000 seconds = 5 hours and 15 seconds needed to train.
