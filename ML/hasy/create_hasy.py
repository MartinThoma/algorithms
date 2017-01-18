#!/usr/bin/env python

"""Create hwrt-offline dataset."""

from PIL import Image, ImageDraw
import csv
import json
import os
import sys


def load_csv(filepath):
    """Read a CSV file."""
    data = []
    with open(filepath, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            data.append(row)
    return data


def load_dataset(filepath):
    """Load a HWRT dataset."""
    data = load_csv(filepath)
    dicts = []
    for i, row in enumerate(data):
        row['i'] = i
        row['data'] = normalize_data(json.loads(row['data']), 32, 32)
        dicts.append(row)
    return dicts


def normalize_data(lines, width, height):
    """Normalize the data to be centered within a bounding box."""
    min_x, max_x = float('inf'), 0
    min_y, max_y = float('inf'), 0
    for line in lines:
        for p in line:
            min_x = min(min_x, p['x'])
            max_x = max(max_x, p['x'])
            min_y = min(min_y, p['y'])
            max_y = max(max_y, p['y'])
    dimensions = max(max_x - min_x, max_y - min_y)
    dimensions = max(32.0, float(dimensions))
    x_translation = (dimensions - (max_x - min_x)) / 2
    y_translation = (dimensions - (max_y - min_y)) / 2
    for i, line in enumerate(lines):
        for j, p in enumerate(line):
            lines[i][j]['x'] = ((p['x'] - min_x + x_translation) /
                                dimensions * width)
            lines[i][j]['y'] = ((p['y'] - min_y + y_translation) /
                                dimensions * height)
    # print(lines)
    return lines


def draw(target_path, lines):
    """Create an image for online data."""
    width, height = 32, 32
    im = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for line in lines:
        had_difference = False
        p = line[0]
        for p1, p2 in zip(line, line[1:]):
            if int(abs(p1['x'] - p2['x'])) + int(abs(p1['y'] - p2['y'])) > 0:
                had_difference = True
            draw.line((p1['x'], p1['y'], p2['x'], p2['y']),
                      fill=0,
                      width=2)
        if not had_difference:
            r = 2
            x, y = p['x'], p['y']
            draw.ellipse((x - r, y - r, x + r, y + r), fill=0)
    im.save(target_path)


def generate_dataset(data, symbols_dict, directory):
    """Generate a dataset."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print("Directory '%s' already exists. Please remove it.")
        sys.exit(-1)
    print("Start generating 32x32 images for %i instances of %i symbols" %
          (len(data), len(symbols_dict)))
    labels = [('path', 'symbol_id', 'latex')]
    for i in range(len(data)):
        if i % 1000 == 0:
            print("\t%i done" % i)
        target_path = "%s/%s.png" % (directory, data[i]['i'])
        draw(target_path, lines=data[i]['data'])
        labels.append((target_path,
                       data[i]['symbol_id'],
                       symbols_dict[data[i]['symbol_id']]))
    with open('%s-labels.csv' % directory, 'w') as f:
        a = csv.writer(f, delimiter=',')
        a.writerows(labels)

symbols_df = load_csv('symbols.csv')
symbols = {}
for row in symbols_df:
    symbols[row['symbol_id']] = row['latex']

generate_dataset(load_dataset('test-data.csv'),
                 symbols,
                 directory='hasy-test')
print("Start loading train data...")
generate_dataset(load_dataset('train-data.csv'),
                 symbols,
                 directory='hasy-train')
