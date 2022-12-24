# Core Library modules
import math
import random
from typing import List, Tuple

# Third party modules
import cv2
import numpy as np
import progressbar

# First party modules
from mpu.geometry import LineSegment, Point, do_lines_intersect


def create(
    width: int = 1400,
    height: int = 1200,
    nb_points: int = 100,
    max_length: int = None,
    iterations: int = 10,
):
    if max_length is None:
        max_length = int((width ** 2 + height ** 2) ** 0.5)
    lines: List[Tuple[int, int, int, int]] = []
    points = [
        (
            random.randint(0, width),
            random.randint(0, height),
            math.radians(random.randint(0, 360)),
        )
        for _ in range(nb_points)
    ]
    for _ in progressbar.progressbar(range(iterations)):
        new_points: List[Tuple[int, int, float]] = []
        for point in points:
            x, y, angle = point

            # Find end
            dx, dy = math.cos(angle), math.sin(angle)
            xe, ye = x + dx * max_length, y + dy * max_length
            xe, ye = crop_at_box((x, y, xe, ye), width, height)

            # Get all intersections
            intersections = get_intersections((x, y, xe, ye), lines) + [Point(xe, ye)]

            # And use the first intersection
            xe, ye = get_shortest_endpoint(x, y, intersections)

            xe, ye = int(xe), int(ye)

            lines.append((x, y, xe, ye))
            new_points.append((xe, ye, math.radians((math.degrees(angle) + 90) % 360)))

    # draw
    img_size = (height, width)
    img = np.ones(img_size) * 255
    lineThickness = 2
    for x1, y1, x2, y2 in lines:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), lineThickness)
    cv2.imwrite("houghlines3.jpg", img)


def get_shortest_endpoint(x, y, intersections: List[Point]) -> Tuple[float, float]:
    shortest_x, shortest_y = intersections[0].x, intersections[0].y
    min_length = LineSegment(Point(x, y), Point(shortest_x, shortest_y)).length()
    for p in intersections:
        xe, ye = p.x, p.y
        tmp = LineSegment(Point(x, y), Point(xe, ye))
        if tmp.length() < min_length:
            shortest_x = xe
            shortest_y = ye
    return (shortest_x, shortest_y)


def crop_at_box(
    line: Tuple[float, float, float, float], width: int, height: int
) -> Tuple[float, float]:
    """Crop the endpoint of a line with the box borders."""
    x, y, xe, ye = line

    # line: f(x) = m * x + t
    m = (ye - y) / (xe - x)
    t = y - m * x
    if xe < 0:
        xe, ye = 0, t
    if xe > width:
        xe, ye = width, m * width + t
    if ye < 0:
        ye, xe = 0, -t / m
    if ye > height:
        ye, xe = height, (height - t) / m

    return xe, ye


def get_intersections(
    line: Tuple[int, int, float, float], lines: List[Tuple[int, int, int, int]]
) -> List[Tuple[float, float]]:
    (x, y, xe, ye) = line

    line_segment = LineSegment(Point(x, y), Point(xe, ye))

    intersections = []
    for line_tmp in lines:
        x1, y1, x2, y2 = line_tmp
        line_segment_tmp = LineSegment(Point(x1, y1), Point(x2, y2))
        intersection = line_segment.get_intersection(line_segment_tmp)
        if intersection is not None:
            intersections.append(intersection)
    return intersections


if __name__ == "__main__":
    create()
