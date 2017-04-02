#!/usr/bin/env python

"""
Run GAN training.

See:
https://oshearesearch.com/index.php/2016/07/01/mnist-generative-adversarial-model-in-keras/
"""

import random
import numpy as np
from keras.layers import Input
from keras.optimizers import Adam
import matplotlib as mpl
mpl.use('Agg')  # works even without X-Org
import matplotlib.pyplot as plt
from keras.models import Model
from tqdm import tqdm
import keras.backend as K


def make_trainable(net, val):
    """Freeze or unfreeze variables."""
    net.trainable = val
    for l in net.layers:
        l.trainable = val


def plot_loss(losses):
    """Plot the loss function."""
    fig = plt.figure(figsize=(10, 8))
    fig.suptitle('Losses')
    plt.plot(losses["d"], label='discriminitive loss')
    plt.plot(losses["g"], label='generative loss')
    plt.legend()
    plt.savefig('plot_loss.png')


def plot_gen(generator, n_ex=16, dim=(4, 4), figsize=(10, 10)):
    """Plot generated images."""
    noise = np.random.uniform(0, 1, size=[n_ex, 100])
    generated_images = generator.predict(noise)
    print(generated_images[0].shape)

    fig = plt.figure(figsize=figsize)
    fig.suptitle('plot_gen')
    for i in range(generated_images.shape[0]):
        plt.subplot(dim[0], dim[1], i + 1)
        img = generated_images[i, :, :, 0]
        plt.imshow(img)
        plt.axis('off')
    plt.tight_layout()
    plt.savefig('plot_gen.png')


def train_for_n(X_train, generator, discriminator, losses, GAN,
                epochs=5000, plt_frq=25, BATCH_SIZE=32):
    """Set up our main training loop."""
    for e in tqdm(range(epochs)):

        # Make generative images
        image_batch = X_train[np.random.randint(0, X_train.shape[0],
                                                size=BATCH_SIZE), :, :, :]
        noise_gen = np.random.uniform(0, 1, size=[BATCH_SIZE, 100])
        generated_images = generator.predict(noise_gen)

        # Train discriminator on generated images
        X = np.concatenate((image_batch, generated_images))
        y = np.zeros([2 * BATCH_SIZE, 2])
        y[0:BATCH_SIZE, 1] = 1
        y[BATCH_SIZE:, 0] = 1

        # make_trainable(discriminator,True)
        d_loss = discriminator.train_on_batch(X, y)
        losses["d"].append(d_loss)

        # train Generator-Discriminator stack on input noise to non-generated
        # output class
        noise_tr = np.random.uniform(0, 1, size=[BATCH_SIZE, 100])
        y2 = np.zeros([BATCH_SIZE, 2])
        y2[:, 1] = 1

        # make_trainable(discriminator,False)
        g_loss = GAN.train_on_batch(noise_tr, y2)
        losses["g"].append(g_loss)

        # Updates plots
        if e % plt_frq == plt_frq - 1:
            plot_loss(losses)
            plot_gen(generator)


def plot_real(X_train, n_ex=16, dim=(4, 4), figsize=(10, 10)):
    """Plot real data."""
    idx = np.random.randint(0, X_train.shape[0], n_ex)
    generated_images = X_train[idx, :, :, :]

    fig = plt.figure(figsize=figsize)
    fig.suptitle('plot_real')
    for i in range(generated_images.shape[0]):
        plt.subplot(dim[0], dim[1], i + 1)
        img = generated_images[i, :, :, 0]
        plt.imshow(img)
        plt.axis('off')
    plt.tight_layout()
    plt.savefig('plot_real.png')


def main(data_module, generator_module, discriminator_module):
    """Orchestrate."""
    data = data_module.load_data()
    X_train = data['x_train']
    X_test = data['x_test']
    X_train = data_module.preprocess(X_train)
    X_test = data_module.preprocess(X_test)

    shp = X_train.shape[1:]
    opt = Adam(lr=1e-4)
    dopt = Adam(lr=1e-3)

    # Build Generative model ...
    generator = generator_module.create_model()
    generator.compile(loss='binary_crossentropy', optimizer=opt)
    generator.summary()

    # Build Discriminative model ...
    discriminator = discriminator_module.create_model(shp, dropout_rate=0.25)
    discriminator.compile(loss='categorical_crossentropy', optimizer=dopt)

    # Freeze weights in the discriminator for stacked training
    make_trainable(discriminator, False)

    # Build stacked GAN model
    gan_input = Input(shape=[100])
    H = generator(gan_input)
    gan_V = discriminator(H)
    GAN = Model(gan_input, gan_V)
    GAN.compile(loss='categorical_crossentropy', optimizer=opt)
    GAN.summary()

    ntrain = 50000
    trainidx = random.sample(range(0, X_train.shape[0]), ntrain)
    XT = X_train[trainidx, :, :, :]

    # Pre-train the discriminator network ...
    noise_gen = np.random.uniform(0, 1, size=[XT.shape[0], 100])
    generated_images = generator.predict(noise_gen)
    X = np.concatenate((XT, generated_images))
    n = XT.shape[0]
    y = np.zeros([2 * n, 2])
    y[:n, 1] = 1
    y[n:, 0] = 1

    make_trainable(discriminator, True)

    print("fit discriminator")
    discriminator.fit(X, y, epochs=1, batch_size=128)
    y_hat = discriminator.predict(X)

    # Measure accuracy of pre-trained discriminator network
    y_hat_idx = np.argmax(y_hat, axis=1)
    y_idx = np.argmax(y, axis=1)
    diff = y_idx - y_hat_idx
    n_tot = y.shape[0]
    n_rig = (diff == 0).sum()
    acc = n_rig * 100.0 / n_tot
    print("Accuracy: {:0.02f}% ({} of {}) right".format(acc, n_rig, n_tot))

    # set up loss storage vector
    losses = {"d": [], "g": []}

    # Train for 6000 epochs at original learning rates
    print("Train for 6000 epochs")
    epochs = 6000
    train_for_n(X_train, generator, discriminator, losses, GAN,
                epochs=epochs, plt_frq=500, BATCH_SIZE=32)

    # Train for 2000 epochs at reduced learning rates
    K.set_value(opt.lr, 1e-5)
    K.set_value(dopt.lr, 1e-4)
    print("Train for 2000 epochs")
    epochs = 2000
    train_for_n(X_train, generator, discriminator, losses, GAN,
                epochs=epochs, plt_frq=500, BATCH_SIZE=32)

    # Train for 2000 epochs at reduced learning rates
    K.set_value(opt.lr, 1e-6)
    K.set_value(dopt.lr, 1e-5)
    print("Train for 2000 epochs")
    epochs = 2000
    train_for_n(X_train, generator, discriminator, losses, GAN,
                epochs=epochs, plt_frq=500, BATCH_SIZE=32)

    generator.save('generator.h5')
    discriminator.save('discriminator.h5')

    # Plot the final loss curves
    plot_loss(losses)

    # Plot some generated images from our GAN
    plot_gen(generator, 25, (5, 5), (12, 12))

    # Plot real MNIST images for comparison
    plot_real(X_train)

if __name__ == '__main__':
    import mnist as data_module
    import discriminator_module
    import generator_module
    main(data_module, generator_module, discriminator_module)
