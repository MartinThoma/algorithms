## Purpose

AutoKeras is a framework which automatically creates a neural network topology,
given only the dataset.


## Results MNIST

```
time python3 mnist_example.py
Using TensorFlow backend.

Initializing search.
Initialization finished.


+----------------------------------------------+
|               Training model 0               |
+----------------------------------------------+
Using TensorFlow backend.

No loss decrease after 5 epochs.


Saving model.
+--------------------------------------------------------------------------+
|        Model ID        |          Loss          |      Metric Value      |
+--------------------------------------------------------------------------+
|           0            |   1.4756227307021619   |         0.9904         |
+--------------------------------------------------------------------------+
/usr/lib/python3.6/multiprocessing/semaphore_tracker.py:143: UserWarning: semaphore_tracker: There appear to be 1 leaked semaphores to clean up at shutdown
  len(cache))


+----------------------------------------------+
|               Training model 1               |
+----------------------------------------------+
/home/moose/.local/lib/python3.6/site-packages/autokeras/bayesian.py:151: UserWarning: Predicted variances smaller than 0. Setting those variances to 0.
  warnings.warn("Predicted variances smaller than 0. "
Using TensorFlow backend.

No loss decrease after 5 epochs.


+--------------------------------------------------------------------------+
|    Father Model ID     |                 Added Operation                 |
+--------------------------------------------------------------------------+
|           0            |           ('to_add_skip_model', 1, 5)           |
+--------------------------------------------------------------------------+

Saving model.
+--------------------------------------------------------------------------+
|        Model ID        |          Loss          |      Metric Value      |
+--------------------------------------------------------------------------+
|           1            |   1.5098872095346452   |        0.99192         |
+--------------------------------------------------------------------------+
/usr/lib/python3.6/multiprocessing/semaphore_tracker.py:143: UserWarning: semaphore_tracker: There appear to be 1 leaked semaphores to clean up at shutdown
  len(cache))

Loading and training the best model recorded from the search.

No loss decrease after 30 epochs.

99.39

real    11255,74s
user    7872,08s
sys    3510,83s
```
