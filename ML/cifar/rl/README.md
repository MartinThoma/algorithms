## About

This model was found by reinforcment learning (see [Neural Archtecture Search With Reinforcment Learning](https://arxiv.org/abs/1611.01578), [reddit discussion](https://www.reddit.com/r/MachineLearning/comments/5b5022)). It gives state of
the art results of CIFAR.

This model gives 28.3% accuracy after one epoch. I'm still running it; lets see
how well it gets.

It has 4,380,022 parameters (4,374,742 trainable parameters).


## Notes

* After 25 epochs with Adam(lr=1E-4) the test accuracy was at 36.6%, but the
  test accuracy jumped a lot. After epoch 22, it was at 38.1%.


## Implementation questions

I have a couple of questions about the architecture / training setup which I
didn't find in the paper (I might just have missed it):

1. Does the CIFAR10 model reported in Figure 7 use Batch Normalization? If so, where exactly?
2. Which training algorithm was used for the CIFAR10 model? Adam with LR=1E-4?
3. Which batch size did you use for training the CIFAR10 model? 32?
4. Which initialization scheme did you use for the CIFAR10 model? He uniform?
5. Which border mode did you use for the CIFAR10 model? Same?
6. Did you use a bias for the Convolutional layer in the CIFAR10 model?
7. Did you use a regularizer (e.g. l2 with 1E-4) for the CIFAR10 model?
8. Did you use data augmentation for the CIFAR10 model? If yes, which kind?

