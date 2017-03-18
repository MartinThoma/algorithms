#!/usr/bin/env python

"""Calculate the IoU of axis-aligned bounding boxes."""

import csv


def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou


if __name__ == '__main__':
    with open('testcases.csv', 'r') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        next(reader, None)  # skip the headers
        examples = [row for row in reader]
    for i in range(len(examples)):
        ex = examples[i]
        bb1 = {'x1': int(ex[0]),
               'y1': int(ex[1]),
               'x2': int(ex[2]),
               'y2': int(ex[3])}
        bb2 = {'x1': int(ex[4]),
               'y1': int(ex[5]),
               'x2': int(ex[6]),
               'y2': int(ex[7])}
        iou = float(ex[8])
        comment = ex[9]
        pred_iou = get_iou(bb1, bb2)
        if abs(pred_iou - iou) > 1e-7:
            print("Test case {} failed ({})".format(i + 1, comment))
            print("\tExpected {:0.4f}, got {:0.4f}".format(iou, pred_iou))
