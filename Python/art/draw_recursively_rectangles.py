from dataclasses import dataclass
from typing import List, Tuple

# Just store https://stackoverflow.com/a/5709655/562769
# as anti_aliased_line.py in the same directory
from anti_aliased_line import draw_line_antialiased
from PIL import Image, ImageDraw


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Line:
    p1: Point
    p2: Point

    def position(self, p: float) -> Point:
        return Point(
            self.p1.x + (self.p2.x - self.p1.x) * p,
            self.p1.y + (self.p2.y - self.p1.y) * p,
        )


@dataclass
class Rectangle:
    p1: Point
    p2: Point
    p3: Point
    p4: Point

    def __getitem__(self, key: int) -> Point:
        if key == 0:
            return self.p1
        elif key == 1:
            return self.p2
        elif key == 2:
            return self.p3
        elif key == 3:
            return self.p4
        raise ValueError(f"key = {key} is invalid")

    def __setitem__(self, key: int, value: Point) -> None:
        if key == 0:
            self.p1 = value
        elif key == 1:
            self.p2 = value
        elif key == 2:
            self.p3 = value
        elif key == 3:
            self.p4 = value
        else:
            raise ValueError(f"key = {key} is invalid")


def new_point(rect: Rectangle, i: int, pct: float = 0.1) -> Point:
    if i == 0:
        return Line(rect.p1, rect.p2).position(pct)
    elif i == 1:  # top
        return Line(rect.p2, rect.p3).position(pct)
    elif i == 2:
        return Line(rect.p3, rect.p4).position(pct)
    elif i == 3:
        return Line(rect.p4, rect.p1).position(pct)
    raise ValueError(f"i = {i} is invalid")


def get_color(i: int, variant:int=1) -> Tuple[int, int, int, int]:
    if variant == 1:
        r = 0 # i % 256
        g = 0  # i * 2 % 256
        b = i % (256)
        return (r, g, b, 255)
    else:
        r = i % 256
        g = 0  # i * 2 % 256
        b = 0 # i % (256 * 2)
        return (r, g, b, 255)


def main():
    width = 1000
    height = 1000
    im = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    rectangle = Rectangle(
        Point(0, 0), Point(width, 0), Point(width, height), Point(0, height)
    )

    rect_width = 300
    rect_height = 300
    w_offset = (width - rect_width) / 2
    h_offset = (height - rect_height) / 2
    rectangle2 = Rectangle(
        Point(w_offset, h_offset),
        Point(width - w_offset, h_offset),
        Point(width - w_offset, height - h_offset),
        Point(w_offset, height - h_offset),
    )

    for i in range(1000):
        p1 = rectangle[i % 4]
        p2 = rectangle[(i + 1) % 4]
        draw_line_antialiased(draw, im, p1.x, p1.y, p2.x, p2.y, get_color(i, variant=1))

        p1 = rectangle2[i % 4]
        p2 = rectangle2[(i + 1) % 4]
        draw_line_antialiased(draw, im, p1.x, p1.y, p2.x, p2.y, get_color(i, variant=2))

        # draw.line((p1.x, p1.y, p2.x, p2.y), fill=get_color(i))
        rectangle[i % 4] = new_point(rectangle, i % 4, pct=0.01)
        rectangle2[i % 4] = new_point(rectangle2, i % 4, pct=0.01)

    # write to stdout
    im.save("rectangles.png", "PNG")


if __name__ == "__main__":
    main()
