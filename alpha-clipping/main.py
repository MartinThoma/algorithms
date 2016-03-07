#!/usr/bin/env python

"""Example of the alpha clipping algorithm."""


def main():
    """Test some simple examples."""
    pl = Point(0.0, 0.0)
    pr = Point(10.0, 6.0)
    p0 = Point(-3.0, 4.0)
    p1 = Point(6.0, -2.0)
    p3 = Point(-1.0, -1.0)
    p4 = Point(4.0, 4.0)
    p5 = Point(1.0, 100.0)
    rectangle = Rectangle(pl, pr)
    print(alpha_clipping(rectangle, Line(p1, pr)))
    print(alpha_clipping(rectangle, Line(p3, pr)))
    print(alpha_clipping(rectangle, Line(p3, p4)))
    print(alpha_clipping(rectangle, Line(p1, p3)))
    print(alpha_clipping(rectangle, Line(p3, p5)))
    print(alpha_clipping(rectangle, Line(p0, p1)))


class Point(object):
    """A point identified by (x,y) coordinates."""

    def __init__(self, x=0.0, y=0.0):
        """
        Constructor for a point.

        Parameters
        ----------
        x : float
        y : float
        """
        assert isinstance(x, float), "x=%r is not a float" % x
        assert isinstance(y, float), "y=%r is not a float" % y
        self.x = x
        self.y = y

    def __str__(self):
        return "P(%0.2f, %0.2f)" % (self.x, self.y)

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __rmul__(self, other):  # :-/
        assert isinstance(other, float), "other=%r is not a float" % other
        return Point(other * self.x, other * self.y)


class Rectangle(object):
    """A rectangle identified by two points."""

    def __init__(self, p1, p2):
        """
        Constructor for a rectangle.

        Parameters
        ----------
        p1 : Point
        p2 : Point
        """
        assert isinstance(p1, Point), "p1=%r is not a point" % p1
        assert isinstance(p2, Point), "p2=%r is not a point" % p2
        self.p1 = p1
        self.p2 = p2
        self.x_min = min(p1.x, p2.x)
        self.y_min = min(p1.y, p2.x)
        self.x_max = max(p1.x, p2.x)
        self.y_max = max(p1.y, p2.x)

    def get_outcode(self, p):
        """
        Get the outcode for a point p.

        The values are (left, right, bottom, top).

        Parameters
        ----------
        p : Point

        Returns
        -------
        list of 4 bools
        """
        assert isinstance(p, Point), "p=%r is not a point" % p
        outcode = [p.x < self.x_min,
                   p.x > self.x_max,
                   p.y < self.y_min,
                   p.y > self.y_max]
        return outcode

    def get_wec(self, e, p):
        """
        Get the window edge coordiantes (WEC) of a point p according to edge e.

        Parameters
        ----------
        e : 0, 1, 2, 3
        p : Point

        Returns
        -------
        float
        """
        assert e in [0, 1, 2, 3], "e=%s is not in [0, 1, 2, 3]" % str(e)
        assert isinstance(p, Point), "p=%r is not a point" % p
        if e == 0:  # left
            return p.x - self.x_min
        elif e == 1:  # right
            return self.x_max - p.x
        elif e == 2:  # bottom
            return p.y - self.y_min
        elif e == 3:  # top
            return self.y_max - p.y


class Line(object):
    """A line identified by two points."""

    def __init__(self, p1, p2):
        """
        Constructor for a line.

        Parameters
        ----------
        p1 : Point
        p2 : Point
        """
        assert isinstance(p1, Point), "p1=%r is not a point" % p1
        assert isinstance(p2, Point), "p2=%r is not a point" % p2
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return "[%s, %s]" % (str(self.p1), str(self.p2))

    def __repr__(self):
        return str(self)


def alpha_clipping(rectangle, line):
    """
    Apply alpha-clipping of `line` according to `rectangle`.

    Parameters
    ----------
    rectangle : Rectangle
    line : Line

    Returns
    -------
    `None` or Line within rectangle
    """
    a_min = 0.0
    a_max = 1.0
    outcode_p1 = rectangle.get_outcode(line.p1)
    outcode_p2 = rectangle.get_outcode(line.p2)
    for e in range(4):
        if outcode_p1[e] and outcode_p2[e]:
            return None  # trivial reject
        if outcode_p1[e] or outcode_p2[e]:
            # line intersects line
            wec_p1 = rectangle.get_wec(e, line.p1)
            wec_p2 = rectangle.get_wec(e, line.p2)
            a_s = wec_p1 / (wec_p1 - wec_p2)
            if outcode_p1[e]:  # P1 is outside of the rectangle
                a_min = max(a_min, a_s)
            else:
                a_max = min(a_max, a_s)
    if a_min > a_max:
        return None  # non-trivial reject
    else:
        # Now we have a line which is parametrized like this:
        # P1 + a * (P2 - P1) with a in [a_min, a_max]
        # We want a line which is parametrized like this:
        # P1' + a * (P2' - P1') with a in [0, 1]
        print("a_min=%0.2f" % a_min)
        print("a_max=%0.2f" % a_max)
        p1s = line.p1 + a_min * (line.p2 - line.p1)
        p2s = line.p1 + a_max * (line.p2 - line.p1)
        return Line(p1s, p2s)


if __name__ == '__main__':
    main()
