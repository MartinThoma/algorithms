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


def get_color(i: int, variant: int = 1) -> Tuple[int, int, int, int]:
    variant = variant % 9
    if variant == 0:
        r = i % (256)
        g = 0
        b = 0
        return (r, g, b, 255)
    if variant == 1:
        r = 0
        g = i % (256)
        b = 0
        return (r, g, b, 255)
    elif variant == 2:
        r = 0
        g = 0
        b = i % (256)
        return (r, g, b, 255)
    elif variant == 3:
        r = i % (256)
        g = i % (256)
        b = 0
        return (r, g, b, 255)
    elif variant == 4:
        r = i % (64)
        g = i % (64)
        b = i % (64)
        return (r, g, b, 255)
    elif variant == 5:
        r = 0
        g = i % (256)
        b = i % (256)
        return (r, g, b, 255)
    elif variant == 6:
        r = i % (256)
        g = i % (256)
        b = i % (256)
        return (r, g, b, 255)
    elif variant == 7:
        r = i % (128)
        g = i % (128)
        b = i % (128)
        return (r, g, b, 255)
    elif variant == 8:
        r = i % (256)
        g = 0
        b = i % (256)
        return (r, g, b, 255)


def create_rectangle(
    im, draw, rect_width, rect_height, w_offset, h_offset, variant: int, pct: float = 0.01
):
    rectangle = Rectangle(
        Point(w_offset, h_offset),
        Point(w_offset + rect_width, h_offset),
        Point(w_offset + rect_width, h_offset + rect_height),
        Point(w_offset, h_offset + rect_height),
    )
    for i in range(1000):
        p1 = rectangle[i % 4]
        p2 = rectangle[(i + 1) % 4]
        draw_line_antialiased(
            draw, im, p1.x, p1.y, p2.x, p2.y, get_color(i, variant=variant)
        )

        # draw.line((p1.x, p1.y, p2.x, p2.y), fill=get_color(i))
        rectangle[i % 4] = new_point(rectangle, i % 4, pct=pct)


def main():
    rect_width = 300
    rect_height = 300
    rows = 3
    cols = 3
    width = rows * rect_width
    height = cols * rect_height
    im = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    w_offset = (width - rect_width) / 2
    h_offset = (height - rect_height) / 2
    pct = [0.1, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1]
    for row in range(rows):
        w_offset = rect_width * row
        for col in range(cols):
            i = row * rows + col
            h_offset = rect_height * col
            create_rectangle(
                im,
                draw,
                rect_width,
                rect_height,
                w_offset,
                h_offset,
                variant=i,
                pct=pct[i % len(pct)],
            )

    # write to stdout
    im.save("rectangles.png", "PNG")


if __name__ == "__main__":
    main()
