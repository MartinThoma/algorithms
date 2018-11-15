## Purpose

This is copied from `02-keras-validation-curve` where I noticed by looking at
the validation curve that training for 150 epochs did not overfit and not
saturate for the given model.

This time, I train for 1000 epochs instead of 150 epochs.

This change also introduces checkpoints.

## Results

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
dense_1 (Dense)              (None, 256)               692480    
_________________________________________________________________
dropout_1 (Dropout)          (None, 256)               0         
_________________________________________________________________
dense_2 (Dense)              (None, 256)               65792     
_________________________________________________________________
dense_3 (Dense)              (None, 369)               94833     
=================================================================
Total params: 855,585
Trainable params: 855,585
Non-trainable params: 0
_________________________________________________________________
None
16992/16992 [==============================] - 3s 181us/step

acc: 75.71%
```
