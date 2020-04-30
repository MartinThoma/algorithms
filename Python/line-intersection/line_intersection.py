from typing import Tuple

EPSILON = 0.000001


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}|{self.y})"

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class LineSegment:
    def __init__(self, first: Point, second: Point, name: str = "LineSegment"):
        self.first = first
        self.second = second
        self.name = name

    def bounding_box(self) -> Tuple[Point, Point]:
        """
        Get the bounding box of this line represented by two points.

        The first point is in the lower left corner, the second one at the
        upper right corner.
        """
        result = (
            Point(min(self.first.x, self.second.x), min(self.first.y, self.second.y)),
            Point(max(self.first.x, self.second.x), max(self.first.y, self.second.y)),
        )
        return result

    def __str__(self) -> str:
        if self.name == "LineSegment":
            return f"LineSegment [{self.first} to {self.second}]"
        else:
            return self.name

    def __hash__(self):
        return hash((self.first, self.second, self.name))

    def __eq__(self, other):
        if not isinstance(other, LineSegment):
            return False
        return self.name == other.name and (
            (self.first == other.first and self.second == other.second)
            or (self.first == other.second and self.second == other.first)
        )


def do_bounding_boxes_intersect(a: Tuple[Point, Point], b: Tuple[Point, Point]) -> bool:
    """
    Check if bounding boxes do intersect.

    If one bounding box touches the other, they do intersect.
    """
    return (
        a[0].x <= b[1].x and a[1].x >= b[0].x and a[0].y <= b[1].y and a[1].y >= b[0].y
    )


def crossproduct(a: Point, b: Point) -> float:
    return a.x * b.y - b.x * a.y


def is_point_on_line(a: LineSegment, b: Point) -> bool:
    # Move the image, so that a.first is on (0|0)
    p2 = Point(a.second.x - a.first.x, a.second.y - a.first.y)
    a_tmp = LineSegment(Point(0, 0), p2)
    b_tmp = Point(b.x - a.first.x, b.y - a.first.y)
    r = crossproduct(a_tmp.second, b_tmp)
    return abs(r) < EPSILON


def is_point_right_of_line(a: LineSegment, b: Point) -> bool:
    # Move the image, so that a.first is on (0|0)
    a_tmp = LineSegment(
        Point(0, 0), Point(a.second.x - a.first.x, a.second.y - a.first.y)
    )
    b_tmp = Point(b.x - a.first.x, b.y - a.first.y)
    return crossproduct(a_tmp.second, b_tmp) < 0


def line_segment_touches_or_crosses_line(a: LineSegment, b: LineSegment) -> bool:
    return (
        is_point_on_line(a, b.first)
        or is_point_on_line(a, b.second)
        or (is_point_right_of_line(a, b.first) ^ is_point_right_of_line(a, b.second))
    )


def do_lines_intersect(a: LineSegment, b: LineSegment) -> bool:
    box1 = a.bounding_box()
    box2 = b.bounding_box()
    return (
        do_bounding_boxes_intersect(box1, box2)
        and line_segment_touches_or_crosses_line(a, b)
        and line_segment_touches_or_crosses_line(b, a)
    )


if __name__ == "__main__":
    pass
    # x = Point(x=123456789, y=987654321)
    # y = Point(x=123456789, y=987654321)

    # print({x, y})
