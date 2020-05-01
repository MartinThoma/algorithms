# Core Library modules
import random

# First party modules
from line_intersection import (
    EPSILON,
    LineSegment,
    Point,
    crossproduct,
    do_bounding_boxes_intersect,
    do_lines_intersect,
    get_all_intersecting_lines_by_brute_force,
    is_point_right_of_line,
    line_segment_touches_or_crosses_line,
)


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


def test_point_left_of_line():
    line = LineSegment(Point(0, 0), Point(0, 7))
    a = Point(-5, 5)
    assert not is_point_right_of_line(line, a)


def testPoint_on_line():
    line = LineSegment(Point(0, 0), Point(4, 4))
    a = Point(3, 3)
    assert not is_point_right_of_line(line, a)

    line = LineSegment(Point(4, 4), Point(0, 0))
    assert not is_point_right_of_line(line, a)


def testBoundingBoxesIntersectT1():
    a = [Point(0, 0), Point(5, 5)]
    b = [Point(1, 1), Point(2, 2)]
    assert do_bounding_boxes_intersect(a, b)


def testBoundingBoxesIntersectT2():
    a = [Point(0, 0), Point(3, 3)]
    b = [Point(1, -1), Point(2, 7)]
    assert do_bounding_boxes_intersect(a, b)


def testBoundingBoxesIntersectT3():
    a = [Point(0, 0), Point(3, 3)]
    b = [Point(1, -1), Point(2, 2)]
    assert do_bounding_boxes_intersect(a, b)


def testBoundingBoxesIntersectT4():
    a = [Point(0, 0), Point(3, 3)]
    b = [Point(3, 3), Point(5, 5)]
    assert do_bounding_boxes_intersect(a, b)


def testBoundingBoxesIntersectF1():
    a = [Point(0, 0), Point(3, 3)]
    b = [Point(4, 4), Point(5, 5)]
    assert not do_bounding_boxes_intersect(a, b)


def testLineSegmentCorssesLine():
    """Tests for lineSegmentCrossesLine"""
    lineSegment = LineSegment(Point(5, 5), Point(17, 17))
    line = LineSegment(Point(0, 0), Point(1, 1))
    assert line_segment_touches_or_crosses_line(lineSegment, line)

    lineSegment = LineSegment(Point(17, 17), Point(5, 5))
    line = LineSegment(Point(0, 0), Point(1, 1))
    assert line_segment_touches_or_crosses_line(lineSegment, line)


def test_lines_dont_intesect_F1():
    """Tests for do_lines_intersect"""
    a = LineSegment(Point(0, 0), Point(7, 7))
    b = LineSegment(Point(3, 4), Point(4, 5))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intesect_F2():
    a = LineSegment(Point(-4, 4), Point(-2, 1))
    b = LineSegment(Point(-2, 3), Point(0, 0))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intesect_F3():
    a = LineSegment(Point(0, 0), Point(0, 1))
    b = LineSegment(Point(2, 2), Point(2, 3))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intesect_F4():
    a = LineSegment(Point(0, 0), Point(0, 1))
    b = LineSegment(Point(2, 2), Point(3, 2))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intesect_F5():
    a = LineSegment(Point(-1, -1), Point(2, 2))
    b = LineSegment(Point(3, 3), Point(5, 5))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intesect_F6():
    a = LineSegment(Point(0, 0), Point(1, 1))
    b = LineSegment(Point(2, 0), Point(0.5, 2))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intesect_F7():
    a = LineSegment(Point(1, 1), Point(4, 1))
    b = LineSegment(Point(2, 2), Point(3, 2))
    assert not do_lines_intersect(a, b)


def test_lines_dont_intesect_F8():
    a = LineSegment(Point(0, 5), Point(6, 0))
    b = LineSegment(Point(2, 1), Point(2, 2))
    assert not do_lines_intersect(a, b)


def test_lines_do_intesect_T1():
    a = LineSegment(Point(0, -2), Point(0, 2))
    b = LineSegment(Point(-2, 0), Point(2, 0))
    assert do_lines_intersect(a, b)


def test_lines_do_intesect_T2():
    a = LineSegment(Point(5, 5), Point(0, 0))
    b = LineSegment(Point(1, 1), Point(8, 2))
    assert do_lines_intersect(a, b)


def test_lines_do_intesect_T3():
    a = LineSegment(Point(-1, 0), Point(0, 0))
    b = LineSegment(Point(-1, -1), Point(-1, 1))
    assert do_lines_intersect(a, b)


def test_lines_do_intesect_T4():
    a = LineSegment(Point(0, 2), Point(2, 2))
    b = LineSegment(Point(2, 0), Point(2, 4))
    assert do_lines_intersect(a, b)


def test_lines_do_intesect_T5():
    a = LineSegment(Point(0, 0), Point(5, 5))
    b = LineSegment(Point(1, 1), Point(3, 3))
    assert do_lines_intersect(a, b)


def test_lines_do_intesect_T6():
    for i in range(50):
        ax = random.random()
        ay = random.random()
        bx = random.random()
        by = random.random()
        a = LineSegment(Point(ax, ay), Point(bx, by))
        b = LineSegment(Point(ax, ay), Point(bx, by))
        assert do_lines_intersect(a, b)


def test_BlogExample():
    """check getAllIntersectingLines()"""
    lines: List[LineSegment] = [
        LineSegment(Point(1, 4), Point(6, 1), "a"),
        LineSegment(Point(2, 1), Point(5, 4), "b"),
        LineSegment(Point(3, 1), Point(6, 4), "c"),
        LineSegment(Point(4, 1), Point(8, 5), "d"),
        LineSegment(Point(3, 4), Point(9, 3), "e"),
        LineSegment(Point(7, 2), Point(9, 3), "f"),
        LineSegment(Point(6, 7), Point(9, 1), "g"),
        LineSegment(Point(11, 1), Point(16, 5), "h"),
        LineSegment(Point(13, 3), Point(13, 4), "i"),
        LineSegment(Point(15, 3), Point(15, 4), "j"),
        LineSegment(Point(13, 2), Point(14, 2), "k"),
        LineSegment(Point(14, 1), Point(14, 2), "l"),
        LineSegment(Point(17, 3), Point(21, 3), "m"),
        LineSegment(Point(19, 5), Point(19, 1), "n"),
        LineSegment(Point(11, 1), Point(16, 5), "o"),
    ]

    intersections: Set[LineSegment] = set()
    add = frozenset({lines[0], lines[1]})
    intersections.add(add)
    add = frozenset({lines[0], lines[2]})
    intersections.add(add)
    add = frozenset({lines[0], lines[3]})
    intersections.add(add)
    add = frozenset({lines[3], lines[6]})
    intersections.add(add)
    add = frozenset({lines[4], lines[1]})
    intersections.add(add)
    add = frozenset({lines[4], lines[2]})
    intersections.add(add)
    add = frozenset({lines[4], lines[3]})
    intersections.add(add)
    add = frozenset({lines[4], lines[5]})
    intersections.add(add)
    add = frozenset({lines[4], lines[6]})
    intersections.add(add)
    add = frozenset({lines[5], lines[6]})
    intersections.add(add)
    add = frozenset({lines[10], lines[11]})
    intersections.add(add)
    add = frozenset({lines[12], lines[13]})
    intersections.add(add)
    add = frozenset({lines[7], lines[14]})
    intersections.add(add)

    intersectionsBrute: Set[LineSegment] = get_all_intersecting_lines_by_brute_force(
        lines
    )
    # intersectionsSweep: Set[LineSegment] = getAllIntersectingLines(lines)

    assert intersectionsBrute == intersections

    # twice [e,g], but not [[d, g], [e, c], [e, d], [e, f]]
    # assert intersectionsSweep == intersections


def test_compare_to_brute_force():
    n = 30
    max_intersections = (n * n - n) / 2

    lines: List[LineSegment] = []
    for i in range(n):
        a = Point(random.random(), random.random())
        b = Point(random.random(), random.random())
        lines.append(LineSegment(a, b))

    intersectionsBrute: Set[LineSegment] = get_all_intersecting_lines_by_brute_force(
        lines
    )
    # intersectionsSweep: Set[LineSegment] = getAllIntersectingLines(lines)
    assert len(intersectionsBrute) <= max_intersections
    # assert intersectionsBrute == intersectionsSweep
