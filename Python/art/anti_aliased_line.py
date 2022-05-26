"""Library to draw an antialiased line."""
# http://stackoverflow.com/questions/3122049/drawing-an-anti-aliased-line-with-thepython-imaging-library
# https://en.wikipedia.org/wiki/Xiaolin_Wu%27s_line_algorithm
import math


def plot(draw, img, x, y, c, col, steep, dash_interval):
    """Draws an antiliased pixel on a line."""
    if steep:
        x, y = y, x
    if x < img.size[0] and y < img.size[1] and x >= 0 and y >= 0:
        c = c * (float(col[3]) / 255.0)
        p = img.getpixel((x, y))
        x = int(x)
        y = int(y)
        if dash_interval:
            d = dash_interval - 1
            if (x / dash_interval) % d == 0 and (y / dash_interval) % d == 0:
                return
        draw.point(
            (x, y),
            fill=(
                int((p[0] * (1 - c)) + col[0] * c),
                int((p[1] * (1 - c)) + col[1] * c),
                int((p[2] * (1 - c)) + col[2] * c),
                255,
            ),
        )


def iround(x):
    """Rounds x to the nearest integer."""
    return ipart(x + 0.5)


def ipart(x):
    """Floors x."""
    return math.floor(x)


def fpart(x):
    """Returns the fractional part of x."""
    return x - math.floor(x)


def rfpart(x):
    """Returns the 1 minus the fractional part of x."""
    return 1 - fpart(x)


def draw_line_antialiased(draw, img, x1, y1, x2, y2, col, dash_interval=None):
    """Draw an antialised line in the PIL ImageDraw.

    Implements the Xialon Wu antialiasing algorithm.

    col - color
    """
    dx = x2 - x1
    if not dx:
        draw.line((x1, y1, x2, y2), fill=col, width=1)
        return

    dy = y2 - y1
    steep = abs(dx) < abs(dy)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx, dy = dy, dx
    if x2 < x1:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    gradient = float(dy) / float(dx)

    # handle first endpoint
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = rfpart(x1 + 0.5)
    xpxl1 = xend  # this will be used in the main loop
    ypxl1 = ipart(yend)
    plot(draw, img, xpxl1, ypxl1, rfpart(yend) * xgap, col, steep, dash_interval)
    plot(draw, img, xpxl1, ypxl1 + 1, fpart(yend) * xgap, col, steep, dash_interval)
    intery = yend + gradient  # first y-intersection for the main loop

    # handle second endpoint
    xend = round(x2)
    yend = y2 + gradient * (xend - x2)
    xgap = fpart(x2 + 0.5)
    xpxl2 = xend  # this will be used in the main loop
    ypxl2 = ipart(yend)
    plot(draw, img, xpxl2, ypxl2, rfpart(yend) * xgap, col, steep, dash_interval)
    plot(draw, img, xpxl2, ypxl2 + 1, fpart(yend) * xgap, col, steep, dash_interval)

    # main loop
    for x in range(int(xpxl1 + 1), int(xpxl2)):
        plot(draw, img, x, ipart(intery), rfpart(intery), col, steep, dash_interval)
        plot(draw, img, x, ipart(intery) + 1, fpart(intery), col, steep, dash_interval)
        intery = intery + gradient
