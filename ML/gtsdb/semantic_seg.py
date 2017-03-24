#!/usr/bin/env python

"""Semantic Segmentation experiment."""

from keras.models import load_model
from keras.models import Model
from keras.layers import UpSampling2D
import scipy.misc
import numpy as np
from PIL import Image
import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def scale_array(x, new_size):
    """
    Scale a numpy array.

    Parameters
    ----------
    x : numpy array
    new_size : tuple

    Returns
    -------
    scaled array
    """
    min_el = np.min(x)
    max_el = np.max(x)
    y = scipy.misc.imresize(x, new_size, mode='L', interp='nearest')
    y = y / 255.0 * (max_el - min_el) + min_el
    return y


def get_overlay_name(segmentation_name):
    splitted = segmentation_name.split('.')
    splitted[-2] = splitted[-2] + '-overlay'
    output_path = '.'.join(splitted)
    return output_path


def overlay_images(original_image,
                   segmentation_image,
                   hard_classification=True):
    """
    Overlay original_image with segmentation_image.

    store the result with the same name as segmentation_image, but with
        `-overlay`.

    Parameters
    ----------
    original_image : string
        Path to an image file
    segmentation_image : string
        Path to the an image file of the same size as original_image
    hard_classification : bool
        If True, the image will only show either street or no street.
        If False, the image will show probabilities.
    """
    background = Image.open(original_image)
    overlay = Image.open(segmentation_image)
    overlay = overlay.convert('RGB')

    # Replace colors of segmentation to make it easier to see
    street_color = (255, 255, 255)
    width, height = overlay.size
    pix = overlay.load()
    pixels_debug = list(overlay.getdata())
    logging.info('%i colors in classification (min=%s, max=%s)',
                 len(list(set(pixels_debug))),
                 min(pixels_debug),
                 max(pixels_debug))
    for x in range(0, width):
        for y in range(0, height):
            if not hard_classification:
                overlay.putpixel((x, y), (0, pix[x, y][0], 0))
            else:
                if pix[x, y] == street_color:
                    overlay.putpixel((x, y), (0, 255, 0))
                else:
                    overlay.putpixel((x, y), (0, 0, 0))

    background = background.convert('RGBA')
    overlay = overlay.convert('RGBA')

    new_img = Image.blend(background, overlay, 0.5)

    # get new name
    output_path = get_overlay_name(segmentation_image)

    new_img.save(output_path, 'PNG')


model = load_model("gtsdb-fully.h5")
# model.layers.pop()  # Get rid of the classification layer softmax
# model.layers.pop()  # Get rid of the classification layer softmax
# model.outputs = [model.layers[-1].output]
# model.output_layers = [model.layers[-1]]  # added this line in addition to zo7 solution
# model.layers[-1].outbound_nodes = []
# model.summary()

# Get input
# new_input = model.input
# new_input.input_shape = (1, None, None, 3)
# # Find the layer to connect
# # hidden_layer = model.layers[-1].output
# # # Connect a new layer on it
# # new_output = Dense(2)(hidden_layer)
# # Build a new model
# model2 = Model(new_input, hidden_layer)
model.add(UpSampling2D((2, 2)))  # Deconvolution2D
model.add(UpSampling2D((2, 2)))  # Deconvolution2D - (333, 193)
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=["accuracy"])
model.summary()

original_image = "00072.ppm"
img = scipy.misc.imread(original_image)
img = np.array(img, dtype=np.float32)
img /= 255.0
# scipy.misc.imshow(img)
img_shape = img.shape[:2]
img = img.reshape([1] + list(img.shape))
pred = model.predict(img)
pred = pred[0].transpose((2, 1, 0))

for i, layer in enumerate(pred):
    print(layer.shape)
    layer = scale_array(layer, img_shape)
    segmentation_fname = 'segmentations/{}.png'.format(i)
    scipy.misc.imsave(segmentation_fname, layer)
    overlay_images(original_image, segmentation_fname)
