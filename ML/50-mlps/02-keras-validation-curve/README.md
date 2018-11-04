## Purpose

This is copied from `01-keras-basic`. You can notice that there was quite a bit
of overfitting: The final test accuracy is 69.49%, but after epoch 4 it was
already at 70.61% training accuracy and in epoch 150 it was at 91.37% training
accuracy.

This time, I add dropout and I log the training accuracy, the validation
accuracy and the test accuracy in a CSV. I want to create a validation curve
(see https://arxiv.org/pdf/1707.09725.pdf, Subsection 2.5.3: Validation Curves: Accuracy, loss and other metrics)


## Results

The test accuracy improved from 69.49% to 74.18% just by adding dropout!

```
time python3 main.py
Using TensorFlow backend.
Train on 151241 samples, validate on 151241 samples
Epoch 1/150
2018-11-03 10:13:44.807688: I tensorflow/core/platform/cpu_feature_guard.cc:140] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2018-11-03 10:13:44.916352: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:898] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2018-11-03 10:13:44.917270: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1356] Found device 0 with properties: 
name: GeForce 940MX major: 5 minor: 0 memoryClockRate(GHz): 1.2415
pciBusID: 0000:02:00.0
totalMemory: 1.96GiB freeMemory: 1.50GiB
2018-11-03 10:13:44.917290: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1435] Adding visible gpu devices: 0
2018-11-03 10:13:46.593804: I tensorflow/core/common_runtime/gpu/gpu_device.cc:923] Device interconnect StreamExecutor with strength 1 edge matrix:
2018-11-03 10:13:46.595811: I tensorflow/core/common_runtime/gpu/gpu_device.cc:929]      0 
2018-11-03 10:13:46.595853: I tensorflow/core/common_runtime/gpu/gpu_device.cc:942] 0:   N 
2018-11-03 10:13:46.596847: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1053] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 1270 MB memory) -> physical GPU (device: 0, name: GeForce 940MX, pci bus id: 0000:02:00.0, compute capability: 5.0)
151241/151241 [==============================] - 16s 108us/step - loss: 2.7992 - acc: 0.4067 - val_loss: 1.7318 - val_acc: 0.5830
Epoch 2/150
151241/151241 [==============================] - 15s 100us/step - loss: 1.7489 - acc: 0.5786 - val_loss: 1.4055 - val_acc: 0.6476
Epoch 3/150
151241/151241 [==============================] - 15s 102us/step - loss: 1.5349 - acc: 0.6188 - val_loss: 1.2551 - val_acc: 0.6788
Epoch 4/150
151241/151241 [==============================] - 16s 106us/step - loss: 1.4177 - acc: 0.6394 - val_loss: 1.1461 - val_acc: 0.6985
Epoch 5/150
151241/151241 [==============================] - 13s 87us/step - loss: 1.3406 - acc: 0.6528 - val_loss: 1.0898 - val_acc: 0.7080
Epoch 6/150
151241/151241 [==============================] - 13s 87us/step - loss: 1.2829 - acc: 0.6645 - val_loss: 1.0262 - val_acc: 0.7219
Epoch 7/150
151241/151241 [==============================] - 14s 92us/step - loss: 1.2423 - acc: 0.6720 - val_loss: 1.0264 - val_acc: 0.7206
Epoch 8/150
151241/151241 [==============================] - 15s 101us/step - loss: 1.2078 - acc: 0.6784 - val_loss: 0.9767 - val_acc: 0.7307
Epoch 9/150
151241/151241 [==============================] - 15s 100us/step - loss: 1.1777 - acc: 0.6835 - val_loss: 0.9274 - val_acc: 0.7444
Epoch 10/150
151241/151241 [==============================] - 12s 83us/step - loss: 1.1549 - acc: 0.6890 - val_loss: 0.9206 - val_acc: 0.7423
Epoch 11/150
151241/151241 [==============================] - 13s 83us/step - loss: 1.1370 - acc: 0.6918 - val_loss: 0.8850 - val_acc: 0.7526
Epoch 12/150
151241/151241 [==============================] - 15s 102us/step - loss: 1.1223 - acc: 0.6938 - val_loss: 0.8908 - val_acc: 0.7488
Epoch 13/150
151241/151241 [==============================] - 16s 103us/step - loss: 1.1052 - acc: 0.6968 - val_loss: 0.8507 - val_acc: 0.7584
Epoch 14/150
151241/151241 [==============================] - 13s 88us/step - loss: 1.0884 - acc: 0.7006 - val_loss: 0.8416 - val_acc: 0.7593
Epoch 15/150
151241/151241 [==============================] - 14s 94us/step - loss: 1.0757 - acc: 0.7028 - val_loss: 0.8402 - val_acc: 0.7581
Epoch 16/150
151241/151241 [==============================] - 14s 91us/step - loss: 1.0641 - acc: 0.7052 - val_loss: 0.8035 - val_acc: 0.7704
Epoch 17/150
151241/151241 [==============================] - 13s 85us/step - loss: 1.0542 - acc: 0.7069 - val_loss: 0.8172 - val_acc: 0.7630
Epoch 18/150
151241/151241 [==============================] - 13s 87us/step - loss: 1.0510 - acc: 0.7068 - val_loss: 0.8132 - val_acc: 0.7653
Epoch 19/150
151241/151241 [==============================] - 14s 93us/step - loss: 1.0404 - acc: 0.7092 - val_loss: 0.7860 - val_acc: 0.7713
Epoch 20/150
151241/151241 [==============================] - 13s 86us/step - loss: 1.0330 - acc: 0.7101 - val_loss: 0.7867 - val_acc: 0.7674
Epoch 21/150
151241/151241 [==============================] - 14s 94us/step - loss: 1.0260 - acc: 0.7116 - val_loss: 0.7670 - val_acc: 0.7765
Epoch 22/150
151241/151241 [==============================] - 14s 90us/step - loss: 1.0171 - acc: 0.7138 - val_loss: 0.7963 - val_acc: 0.7686
Epoch 23/150
151241/151241 [==============================] - 12s 80us/step - loss: 1.0110 - acc: 0.7146 - val_loss: 0.7589 - val_acc: 0.7759
Epoch 24/150
151241/151241 [==============================] - 12s 81us/step - loss: 1.0039 - acc: 0.7147 - val_loss: 0.7650 - val_acc: 0.7756
Epoch 25/150
151241/151241 [==============================] - 13s 84us/step - loss: 1.0047 - acc: 0.7159 - val_loss: 0.7495 - val_acc: 0.7786
Epoch 26/150
151241/151241 [==============================] - 12s 82us/step - loss: 0.9969 - acc: 0.7167 - val_loss: 0.7533 - val_acc: 0.7764
Epoch 27/150
151241/151241 [==============================] - 12s 82us/step - loss: 0.9915 - acc: 0.7180 - val_loss: 0.7527 - val_acc: 0.7766
Epoch 28/150
151241/151241 [==============================] - 12s 82us/step - loss: 0.9853 - acc: 0.7196 - val_loss: 0.7490 - val_acc: 0.7781
Epoch 29/150
151241/151241 [==============================] - 12s 83us/step - loss: 0.9830 - acc: 0.7198 - val_loss: 0.7767 - val_acc: 0.7657
Epoch 30/150
151241/151241 [==============================] - 12s 82us/step - loss: 0.9828 - acc: 0.7189 - val_loss: 0.7568 - val_acc: 0.7747
Epoch 31/150
151241/151241 [==============================] - 12s 82us/step - loss: 0.9739 - acc: 0.7209 - val_loss: 0.7344 - val_acc: 0.7796
Epoch 32/150
151241/151241 [==============================] - 12s 82us/step - loss: 0.9713 - acc: 0.7223 - val_loss: 0.7477 - val_acc: 0.7778
Epoch 33/150
151241/151241 [==============================] - 12s 80us/step - loss: 0.9677 - acc: 0.7231 - val_loss: 0.7203 - val_acc: 0.7850
Epoch 34/150
151241/151241 [==============================] - 13s 83us/step - loss: 0.9675 - acc: 0.7227 - val_loss: 0.7249 - val_acc: 0.7839
Epoch 35/150
151241/151241 [==============================] - 12s 81us/step - loss: 0.9618 - acc: 0.7241 - val_loss: 0.7011 - val_acc: 0.7859
Epoch 36/150
151241/151241 [==============================] - 13s 83us/step - loss: 0.9585 - acc: 0.7231 - val_loss: 0.7235 - val_acc: 0.7817
Epoch 37/150
151241/151241 [==============================] - 13s 85us/step - loss: 0.9583 - acc: 0.7241 - val_loss: 0.6974 - val_acc: 0.7858
Epoch 38/150
151241/151241 [==============================] - 12s 81us/step - loss: 0.9582 - acc: 0.7240 - val_loss: 0.6984 - val_acc: 0.7904
Epoch 39/150
151241/151241 [==============================] - 12s 81us/step - loss: 0.9509 - acc: 0.7261 - val_loss: 0.6976 - val_acc: 0.7884
Epoch 40/150
151241/151241 [==============================] - 12s 81us/step - loss: 0.9508 - acc: 0.7251 - val_loss: 0.7124 - val_acc: 0.7846
Epoch 41/150
151241/151241 [==============================] - 14s 93us/step - loss: 0.9468 - acc: 0.7275 - val_loss: 0.7130 - val_acc: 0.7863
Epoch 42/150
151241/151241 [==============================] - 14s 91us/step - loss: 0.9387 - acc: 0.7294 - val_loss: 0.7218 - val_acc: 0.7810
Epoch 43/150
151241/151241 [==============================] - 13s 85us/step - loss: 0.9388 - acc: 0.7268 - val_loss: 0.6709 - val_acc: 0.7952
Epoch 44/150
151241/151241 [==============================] - 13s 83us/step - loss: 0.9441 - acc: 0.7271 - val_loss: 0.6746 - val_acc: 0.7949
Epoch 45/150
151241/151241 [==============================] - 13s 84us/step - loss: 0.9421 - acc: 0.7264 - val_loss: 0.6884 - val_acc: 0.7907
Epoch 46/150
151241/151241 [==============================] - 12s 82us/step - loss: 0.9363 - acc: 0.7270 - val_loss: 0.6839 - val_acc: 0.7912
Epoch 47/150
151241/151241 [==============================] - 15s 100us/step - loss: 0.9272 - acc: 0.7302 - val_loss: 0.6681 - val_acc: 0.7944
Epoch 48/150
151241/151241 [==============================] - 19s 127us/step - loss: 0.9311 - acc: 0.7282 - val_loss: 0.6751 - val_acc: 0.7956
Epoch 49/150
151241/151241 [==============================] - 15s 98us/step - loss: 0.9262 - acc: 0.7288 - val_loss: 0.6821 - val_acc: 0.7914
Epoch 50/150
151241/151241 [==============================] - 18s 118us/step - loss: 0.9211 - acc: 0.7305 - val_loss: 0.6706 - val_acc: 0.7941
Epoch 51/150
151241/151241 [==============================] - 14s 89us/step - loss: 0.9256 - acc: 0.7297 - val_loss: 0.6897 - val_acc: 0.7875
Epoch 52/150
151241/151241 [==============================] - 13s 86us/step - loss: 0.9245 - acc: 0.7303 - val_loss: 0.6856 - val_acc: 0.7901
Epoch 53/150
151241/151241 [==============================] - 13s 86us/step - loss: 0.9208 - acc: 0.7316 - val_loss: 0.6756 - val_acc: 0.7925
Epoch 54/150
151241/151241 [==============================] - 12s 82us/step - loss: 0.9173 - acc: 0.7312 - val_loss: 0.6756 - val_acc: 0.7934
Epoch 55/150
151241/151241 [==============================] - 13s 85us/step - loss: 0.9171 - acc: 0.7315 - val_loss: 0.6565 - val_acc: 0.7962
Epoch 56/150
151241/151241 [==============================] - 14s 91us/step - loss: 0.9161 - acc: 0.7327 - val_loss: 0.6530 - val_acc: 0.7989
Epoch 57/150
151241/151241 [==============================] - 17s 109us/step - loss: 0.9124 - acc: 0.7316 - val_loss: 0.6713 - val_acc: 0.7945
Epoch 58/150
151241/151241 [==============================] - 17s 112us/step - loss: 0.9141 - acc: 0.7309 - val_loss: 0.6713 - val_acc: 0.7926
Epoch 59/150
151241/151241 [==============================] - 13s 86us/step - loss: 0.9178 - acc: 0.7304 - val_loss: 0.6862 - val_acc: 0.7888
Epoch 60/150
151241/151241 [==============================] - 14s 90us/step - loss: 0.9045 - acc: 0.7340 - val_loss: 0.6892 - val_acc: 0.7891
Epoch 61/150
151241/151241 [==============================] - 13s 86us/step - loss: 0.9065 - acc: 0.7332 - val_loss: 0.6638 - val_acc: 0.7945
Epoch 62/150
151241/151241 [==============================] - 15s 96us/step - loss: 0.9056 - acc: 0.7343 - val_loss: 0.6413 - val_acc: 0.7987
Epoch 63/150
151241/151241 [==============================] - 14s 94us/step - loss: 0.9052 - acc: 0.7349 - val_loss: 0.6541 - val_acc: 0.7983
Epoch 64/150
151241/151241 [==============================] - 15s 97us/step - loss: 0.9035 - acc: 0.7349 - val_loss: 0.6559 - val_acc: 0.7968
Epoch 65/150
151241/151241 [==============================] - 17s 110us/step - loss: 0.9018 - acc: 0.7326 - val_loss: 0.6507 - val_acc: 0.7982
Epoch 66/150
151241/151241 [==============================] - 18s 116us/step - loss: 0.8985 - acc: 0.7362 - val_loss: 0.6356 - val_acc: 0.8010
Epoch 67/150
151241/151241 [==============================] - 14s 93us/step - loss: 0.8979 - acc: 0.7344 - val_loss: 0.6495 - val_acc: 0.7980
Epoch 68/150
151241/151241 [==============================] - 13s 87us/step - loss: 0.8959 - acc: 0.7352 - val_loss: 0.6307 - val_acc: 0.8033
Epoch 69/150
151241/151241 [==============================] - 15s 96us/step - loss: 0.8979 - acc: 0.7351 - val_loss: 0.6417 - val_acc: 0.7994
Epoch 70/150
151241/151241 [==============================] - 16s 108us/step - loss: 0.8930 - acc: 0.7363 - val_loss: 0.6332 - val_acc: 0.8029
Epoch 71/150
151241/151241 [==============================] - 13s 87us/step - loss: 0.8905 - acc: 0.7365 - val_loss: 0.6601 - val_acc: 0.7957
Epoch 72/150
151241/151241 [==============================] - 13s 87us/step - loss: 0.8973 - acc: 0.7354 - val_loss: 0.6550 - val_acc: 0.7940
Epoch 73/150
151241/151241 [==============================] - 12s 82us/step - loss: 0.8940 - acc: 0.7351 - val_loss: 0.6365 - val_acc: 0.8017
Epoch 74/150
151241/151241 [==============================] - 13s 85us/step - loss: 0.8887 - acc: 0.7354 - val_loss: 0.6174 - val_acc: 0.8078
Epoch 75/150
151241/151241 [==============================] - 12s 81us/step - loss: 0.8926 - acc: 0.7355 - val_loss: 0.6529 - val_acc: 0.7966
Epoch 76/150
151241/151241 [==============================] - 20s 130us/step - loss: 0.8880 - acc: 0.7374 - val_loss: 0.6278 - val_acc: 0.8045
Epoch 77/150
151241/151241 [==============================] - 20s 130us/step - loss: 0.8904 - acc: 0.7367 - val_loss: 0.6186 - val_acc: 0.8062
Epoch 78/150
151241/151241 [==============================] - 19s 124us/step - loss: 0.8845 - acc: 0.7387 - val_loss: 0.6137 - val_acc: 0.8062
Epoch 79/150
151241/151241 [==============================] - 21s 136us/step - loss: 0.8783 - acc: 0.7401 - val_loss: 0.6240 - val_acc: 0.8045
Epoch 80/150
151241/151241 [==============================] - 23s 149us/step - loss: 0.8811 - acc: 0.7391 - val_loss: 0.6281 - val_acc: 0.8033
Epoch 81/150
151241/151241 [==============================] - 27s 181us/step - loss: 0.8788 - acc: 0.7401 - val_loss: 0.6413 - val_acc: 0.8000
Epoch 82/150
151241/151241 [==============================] - 29s 190us/step - loss: 0.8766 - acc: 0.7388 - val_loss: 0.6266 - val_acc: 0.8048
Epoch 83/150
151241/151241 [==============================] - 29s 194us/step - loss: 0.8821 - acc: 0.7393 - val_loss: 0.6209 - val_acc: 0.8053
Epoch 84/150
151241/151241 [==============================] - 13s 86us/step - loss: 0.8802 - acc: 0.7382 - val_loss: 0.6386 - val_acc: 0.7994
Epoch 85/150
151241/151241 [==============================] - 13s 85us/step - loss: 0.8809 - acc: 0.7380 - val_loss: 0.6306 - val_acc: 0.8046
Epoch 86/150
151241/151241 [==============================] - 13s 87us/step - loss: 0.8850 - acc: 0.7394 - val_loss: 0.6384 - val_acc: 0.8000
Epoch 87/150
151241/151241 [==============================] - 14s 92us/step - loss: 0.8791 - acc: 0.7378 - val_loss: 0.6400 - val_acc: 0.7976
Epoch 88/150
151241/151241 [==============================] - 14s 95us/step - loss: 0.8757 - acc: 0.7395 - val_loss: 0.6065 - val_acc: 0.8102
Epoch 89/150
151241/151241 [==============================] - 14s 92us/step - loss: 0.8718 - acc: 0.7397 - val_loss: 0.6111 - val_acc: 0.8081
Epoch 90/150
151241/151241 [==============================] - 14s 93us/step - loss: 0.8768 - acc: 0.7393 - val_loss: 0.6294 - val_acc: 0.8016
Epoch 91/150
151241/151241 [==============================] - 14s 95us/step - loss: 0.8652 - acc: 0.7409 - val_loss: 0.5973 - val_acc: 0.8123
Epoch 92/150
151241/151241 [==============================] - 14s 92us/step - loss: 0.8708 - acc: 0.7416 - val_loss: 0.6124 - val_acc: 0.8084
Epoch 93/150
151241/151241 [==============================] - 15s 98us/step - loss: 0.8703 - acc: 0.7409 - val_loss: 0.6056 - val_acc: 0.8088
Epoch 94/150
151241/151241 [==============================] - 14s 94us/step - loss: 0.8671 - acc: 0.7411 - val_loss: 0.6108 - val_acc: 0.8085
Epoch 95/150
151241/151241 [==============================] - 14s 95us/step - loss: 0.8706 - acc: 0.7404 - val_loss: 0.6236 - val_acc: 0.8026
Epoch 96/150
151241/151241 [==============================] - 22s 146us/step - loss: 0.8729 - acc: 0.7411 - val_loss: 0.6089 - val_acc: 0.8076
Epoch 97/150
151241/151241 [==============================] - 16s 108us/step - loss: 0.8632 - acc: 0.7415 - val_loss: 0.6138 - val_acc: 0.8053
Epoch 98/150
151241/151241 [==============================] - 15s 98us/step - loss: 0.8667 - acc: 0.7403 - val_loss: 0.6324 - val_acc: 0.8016
Epoch 99/150
151241/151241 [==============================] - 15s 97us/step - loss: 0.8639 - acc: 0.7419 - val_loss: 0.6208 - val_acc: 0.8032
Epoch 100/150
151241/151241 [==============================] - 14s 90us/step - loss: 0.8603 - acc: 0.7422 - val_loss: 0.5782 - val_acc: 0.8179
Epoch 101/150
151241/151241 [==============================] - 14s 94us/step - loss: 0.8650 - acc: 0.7414 - val_loss: 0.6176 - val_acc: 0.8049
Epoch 102/150
151241/151241 [==============================] - 16s 103us/step - loss: 0.8619 - acc: 0.7431 - val_loss: 0.6112 - val_acc: 0.8064
Epoch 103/150
151241/151241 [==============================] - 15s 96us/step - loss: 0.8607 - acc: 0.7428 - val_loss: 0.6026 - val_acc: 0.8099
Epoch 104/150
151241/151241 [==============================] - 14s 90us/step - loss: 0.8655 - acc: 0.7418 - val_loss: 0.6014 - val_acc: 0.8085
Epoch 105/150
151241/151241 [==============================] - 14s 94us/step - loss: 0.8622 - acc: 0.7429 - val_loss: 0.6030 - val_acc: 0.8103
Epoch 106/150
151241/151241 [==============================] - 15s 98us/step - loss: 0.8622 - acc: 0.7419 - val_loss: 0.6131 - val_acc: 0.8078
Epoch 107/150
151241/151241 [==============================] - 13s 88us/step - loss: 0.8576 - acc: 0.7435 - val_loss: 0.6167 - val_acc: 0.8046
Epoch 108/150
151241/151241 [==============================] - 15s 99us/step - loss: 0.8593 - acc: 0.7430 - val_loss: 0.6212 - val_acc: 0.8042
Epoch 109/150
151241/151241 [==============================] - 14s 96us/step - loss: 0.8571 - acc: 0.7430 - val_loss: 0.6020 - val_acc: 0.8094
Epoch 110/150
151241/151241 [==============================] - 17s 112us/step - loss: 0.8625 - acc: 0.7426 - val_loss: 0.5983 - val_acc: 0.8114
Epoch 111/150
151241/151241 [==============================] - 16s 104us/step - loss: 0.8578 - acc: 0.7431 - val_loss: 0.6007 - val_acc: 0.8102
Epoch 112/150
151241/151241 [==============================] - 14s 91us/step - loss: 0.8569 - acc: 0.7436 - val_loss: 0.5991 - val_acc: 0.8093
Epoch 113/150
151241/151241 [==============================] - 14s 94us/step - loss: 0.8518 - acc: 0.7444 - val_loss: 0.5973 - val_acc: 0.8105
Epoch 114/150
151241/151241 [==============================] - 14s 92us/step - loss: 0.8525 - acc: 0.7439 - val_loss: 0.6077 - val_acc: 0.8055
Epoch 115/150
151241/151241 [==============================] - 13s 89us/step - loss: 0.8474 - acc: 0.7456 - val_loss: 0.5986 - val_acc: 0.8108
Epoch 116/150
151241/151241 [==============================] - 14s 92us/step - loss: 0.8503 - acc: 0.7440 - val_loss: 0.5976 - val_acc: 0.8092
Epoch 117/150
151241/151241 [==============================] - 14s 95us/step - loss: 0.8503 - acc: 0.7442 - val_loss: 0.6232 - val_acc: 0.8039
Epoch 118/150
151241/151241 [==============================] - 14s 93us/step - loss: 0.8545 - acc: 0.7438 - val_loss: 0.6174 - val_acc: 0.8038
Epoch 119/150
151241/151241 [==============================] - 14s 94us/step - loss: 0.8576 - acc: 0.7428 - val_loss: 0.5864 - val_acc: 0.8126
Epoch 120/150
151241/151241 [==============================] - 15s 97us/step - loss: 0.8509 - acc: 0.7443 - val_loss: 0.5895 - val_acc: 0.8128
Epoch 121/150
151241/151241 [==============================] - 14s 95us/step - loss: 0.8462 - acc: 0.7451 - val_loss: 0.5872 - val_acc: 0.8122
Epoch 122/150
151241/151241 [==============================] - 14s 93us/step - loss: 0.8481 - acc: 0.7462 - val_loss: 0.5875 - val_acc: 0.8127
Epoch 123/150
151241/151241 [==============================] - 15s 97us/step - loss: 0.8518 - acc: 0.7439 - val_loss: 0.5861 - val_acc: 0.8140
Epoch 124/150
151241/151241 [==============================] - 14s 96us/step - loss: 0.8518 - acc: 0.7446 - val_loss: 0.5904 - val_acc: 0.8135
Epoch 125/150
151241/151241 [==============================] - 15s 98us/step - loss: 0.8434 - acc: 0.7471 - val_loss: 0.5888 - val_acc: 0.8126
Epoch 126/150
151241/151241 [==============================] - 14s 92us/step - loss: 0.8470 - acc: 0.7446 - val_loss: 0.5971 - val_acc: 0.8109
Epoch 127/150
151241/151241 [==============================] - 14s 93us/step - loss: 0.8436 - acc: 0.7461 - val_loss: 0.6139 - val_acc: 0.8056
Epoch 128/150
151241/151241 [==============================] - 15s 99us/step - loss: 0.8440 - acc: 0.7462 - val_loss: 0.5634 - val_acc: 0.8180
Epoch 129/150
151241/151241 [==============================] - 15s 102us/step - loss: 0.8468 - acc: 0.7470 - val_loss: 0.5990 - val_acc: 0.8110
Epoch 130/150
151241/151241 [==============================] - 15s 100us/step - loss: 0.8468 - acc: 0.7462 - val_loss: 0.5828 - val_acc: 0.8142
Epoch 131/150
151241/151241 [==============================] - 14s 93us/step - loss: 0.8462 - acc: 0.7458 - val_loss: 0.5983 - val_acc: 0.8105
Epoch 132/150
151241/151241 [==============================] - 15s 100us/step - loss: 0.8426 - acc: 0.7473 - val_loss: 0.5795 - val_acc: 0.8149
Epoch 133/150
151241/151241 [==============================] - 14s 95us/step - loss: 0.8421 - acc: 0.7463 - val_loss: 0.5708 - val_acc: 0.8184
Epoch 134/150
151241/151241 [==============================] - 15s 96us/step - loss: 0.8412 - acc: 0.7466 - val_loss: 0.5948 - val_acc: 0.8086
Epoch 135/150
151241/151241 [==============================] - 14s 94us/step - loss: 0.8439 - acc: 0.7459 - val_loss: 0.6058 - val_acc: 0.8080
Epoch 136/150
151241/151241 [==============================] - 15s 96us/step - loss: 0.8379 - acc: 0.7483 - val_loss: 0.5753 - val_acc: 0.8145
Epoch 137/150
151241/151241 [==============================] - 14s 93us/step - loss: 0.8433 - acc: 0.7468 - val_loss: 0.5939 - val_acc: 0.8108
Epoch 138/150
151241/151241 [==============================] - 14s 94us/step - loss: 0.8345 - acc: 0.7488 - val_loss: 0.5828 - val_acc: 0.8135
Epoch 139/150
151241/151241 [==============================] - 16s 105us/step - loss: 0.8409 - acc: 0.7470 - val_loss: 0.5729 - val_acc: 0.8167
Epoch 140/150
151241/151241 [==============================] - 13s 86us/step - loss: 0.8397 - acc: 0.7462 - val_loss: 0.5702 - val_acc: 0.8173
Epoch 141/150
151241/151241 [==============================] - 15s 99us/step - loss: 0.8370 - acc: 0.7482 - val_loss: 0.5791 - val_acc: 0.8171
Epoch 142/150
151241/151241 [==============================] - 15s 96us/step - loss: 0.8355 - acc: 0.7487 - val_loss: 0.5860 - val_acc: 0.8124
Epoch 143/150
151241/151241 [==============================] - 14s 95us/step - loss: 0.8348 - acc: 0.7481 - val_loss: 0.5596 - val_acc: 0.8192
Epoch 144/150
151241/151241 [==============================] - 14s 95us/step - loss: 0.8338 - acc: 0.7480 - val_loss: 0.5628 - val_acc: 0.8163
Epoch 145/150
151241/151241 [==============================] - 14s 96us/step - loss: 0.8382 - acc: 0.7484 - val_loss: 0.5702 - val_acc: 0.8177
Epoch 146/150
151241/151241 [==============================] - 12s 82us/step - loss: 0.8319 - acc: 0.7489 - val_loss: 0.5734 - val_acc: 0.8153
Epoch 147/150
151241/151241 [==============================] - 13s 88us/step - loss: 0.8383 - acc: 0.7473 - val_loss: 0.5813 - val_acc: 0.8147
Epoch 148/150
151241/151241 [==============================] - 15s 100us/step - loss: 0.8280 - acc: 0.7499 - val_loss: 0.5875 - val_acc: 0.8131
Epoch 149/150
151241/151241 [==============================] - 14s 95us/step - loss: 0.8320 - acc: 0.7487 - val_loss: 0.5550 - val_acc: 0.8206
Epoch 150/150
151241/151241 [==============================] - 14s 91us/step - loss: 0.8309 - acc: 0.7488 - val_loss: 0.5683 - val_acc: 0.8175
16992/16992 [==============================] - 1s 40us/step

acc: 74.18%

real    2193,24s
user    2353,14s
sys    457,63s
```
