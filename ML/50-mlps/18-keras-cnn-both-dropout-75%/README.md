## Purpose

This is copied from `16-keras-cnn-higher-dropout-l2`. Now the two last layer
have 50% dropout instead of 25%.


## Results

Before, 77.42% accuracy.

```
151040/151241 [============================>.] - ETA: 0s - loss: 1.5913 - acc: 0.6019^CTraceback (most recent call last):
  File "main.py", line 60, in <module>
    callbacks=[csv_logger, checkpointer])
  File "/home/moose/.local/lib/python3.6/site-packages/keras/engine/training.py", line 1037, in fit
    validation_steps=validation_steps)
  File "/home/moose/.local/lib/python3.6/site-packages/keras/engine/training_arrays.py", line 212, in fit_loop
    verbose=0)
  File "/home/moose/.local/lib/python3.6/site-packages/keras/engine/training_arrays.py", line 392, in test_loop
    batch_outs = f(ins_batch)
  File "/home/moose/.local/lib/python3.6/site-packages/keras/backend/tensorflow_backend.py", line 2666, in __call__
    return self._call(inputs)
  File "/home/moose/.local/lib/python3.6/site-packages/keras/backend/tensorflow_backend.py", line 2636, in _call
    fetched = self._callable_fn(*array_vals)
  File "/home/moose/.local/lib/python3.6/site-packages/tensorflow/python/client/session.py", line 1399, in __call__
    run_metadata_ptr)
KeyboardInterrupt

real    38733,98s
user    188674,06s
sys    36739,54s

```

and

```
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
dense_1 (Dense)              (None, 128)               346240    
_________________________________________________________________
dropout_1 (Dropout)          (None, 128)               0         
_________________________________________________________________
dense_2 (Dense)              (None, 256)               33024     
_________________________________________________________________
dropout_2 (Dropout)          (None, 256)               0         
_________________________________________________________________
dense_3 (Dense)              (None, 369)               94833     
=================================================================
Total params: 476,577
Trainable params: 476,577
Non-trainable params: 0
_________________________________________________________________
None
16992/16992 [==============================] - 3s 159us/step

acc: 74.41%
```
