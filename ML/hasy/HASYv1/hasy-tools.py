#!/usr/bin/env python

"""Tools for the HASY dataset."""

import logging
import csv
import random
from PIL import Image, ImageDraw
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)


def load_csv(filepath):
    """Load a CSV file."""
    data = []
    with open(filepath, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar="'")
        for row in reader:
            data.append(row)
    return data


def is_valid_png(filepath):
    """Check if the PNG image is valid."""
    try:
        test = Image.open(filepath)
        test.close()
        return True
    except:
        return False


def verify_all():
    """Verify all PNG files."""
    for csv_data_path in ['hasy-test-labels.csv', 'hasy-train-labels.csv']:
        train_data = load_csv(csv_data_path)
        for data_item in train_data:
            if not is_valid_png(data_item['path']):
                logging.info("%s is invalid." % data_item['path'])
        logging.info("Checked %i items of %s." %
                     (len(train_data), csv_data_path))


def create_random_overview(img_src, x_images, y_images):
    """Create a random overview of images."""
    # Create canvas
    background = Image.new('RGB',
                           (35 * x_images, 35 * y_images),
                           (255, 255, 255))
    bg_w, bg_h = background.size
    # Paste image on canvas
    for x in range(x_images):
        for y in range(y_images):
            path = random.choice(img_src)['path']
            img = Image.open(path, 'r')
            img_w, img_h = img.size
            offset = (35 * x, 35 * y)
            background.paste(img, offset)
    # Draw lines
    draw = ImageDraw.Draw(background)
    for y in range(y_images):  # horizontal lines
        draw.line((0, 35 * y - 2, 35 * x_images, 35 * y - 2), fill=0)
    for x in range(x_images):  # vertical lines
        draw.line((35 * x - 2, 0, 35 * x - 2, 35 * y_images), fill=0)
    # Store
    background.save('out.png')


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--verify",
                        dest="verify",
                        action="store_true",
                        default=False,
                        help="verify PNG files")
    parser.add_argument("--overview",
                        dest="overview",
                        action="store_true",
                        default=False,
                        help="Get overview of data")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    if args.verify:
        verify_all()
    if args.overview:
        img_src = load_csv('hasy-train-labels.csv')
        create_random_overview(img_src, x_images=10, y_images=10)
