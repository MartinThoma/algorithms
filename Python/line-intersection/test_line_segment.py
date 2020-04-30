from line_intersection import (
    Point,
    crossproduct,
    EPSILON,
    LineSegment,
    is_point_right_of_line,
)
import random


def test_antisymmetry_of_cross_product():
    l = [Point(0, 0), Point(1, 1)]
    for i in range(50):
        l.append(Point(random.random(), random.random()))

    for p1 in l:
        for p2 in l:
            r1 = crossproduct(p1, p2)
            r2 = crossproduct(p2, p1)
            assert abs(r1 + r2) < EPSILON, f"[{p1}, {p2}]"


def test_point_right_of_line():
    line = LineSegment(Point(0, 0), Point(0, 7))
    a = Point(5, 5)
    assert is_point_right_of_line(line, a)
