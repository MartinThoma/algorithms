public class Geometry {

    public static final double EPSILON = 0.000001;

    /**
     * Calculate the cross product of two points.
     * @param a first point
     * @param b second point
     * @return the value of the cross product
     */
    public static double crossProduct(Point a, Point b) {
        return a.x * b.y - b.x * a.y;
    }

    /**
     * Checks if Point first is within first box. If first is on the end of
     * first box, its also in the box.
     *
     * @param box the box. The first value is the minimum x- and y-coordinate.
     *            The second value is the maximum x- and y-coordinate
     * @param first the point you want to check
     * @return <code>true</code> if first is in box, otherwise
     *         <code>false</code>
     */
    public static boolean isInBoundingBox(Point[] box, Point a) {
        return box[0].x <= a.x && a.x <= box[1].x && box[0].y <= a.y
                && a.y <= box[1].y;
    }

    /**
     * Checks if a Point is on a line
     * @param a line (interpreted as line, although given as line
     *                segment)
     * @param b point
     * @return <code>true</code> if point is on line, otherwise
     *         <code>false</code>
     */
    public static boolean isPointOnLine(LineSegment a, Point b) {
        // Move the image, so that a.first is on (0|0)
        LineSegment aTmp = new LineSegment(new Point(0, 0), new Point(
                a.second.x - a.first.x, a.second.y - a.first.y));
        Point bTmp = new Point(b.x - a.first.x, b.y - a.first.y);
        double r = crossProduct(aTmp.second, bTmp);
        return Math.abs(r) < EPSILON;
    }

    /**
     * Check if line segment first touches or crosses the line that is defined
     * by line segment second.
     *
     * @param first line segment first
     * @param second line second
     * @return <code>true</code> if line segment first touches or
     *                           crosses line second,
     *         <code>false</code> otherwise.
     */
    public static boolean lineSegmentTouchesOrCrossesLine(LineSegment a,
            LineSegment b) {
        return isPointOnLine(a, b.first)
                || isPointOnLine(a, b.second)
                || (isPointRightOfLine(a, b.first) ^ isPointRightOfLine(a,
                        b.second));
    }

    /**
     * Checks if a point is right of a line. If the point is on the
     * line, it is not right of the line.
     * @param a line segment interpreted as a line
     * @param b the point
     * @return <code>true</code> if the point is right of the line,
     *         <code>false</code> otherwise
     */
    public static boolean isPointRightOfLine(LineSegment a, Point b) {
        // Move the image, so that a.first is on (0|0)
        LineSegment aTmp = new LineSegment(new Point(0, 0), new Point(
                a.second.x - a.first.x, a.second.y - a.first.y));
        Point bTmp = new Point(b.x - a.first.x, b.y - a.first.y);
        return crossProduct(aTmp.second, bTmp) < 0;
    }

    /**
     * Check if line segments intersect
     * @param a first line segment
     * @param b second line segment
     * @return <code>true</code> if lines do intersect,
     *         <code>false</code> otherwise
     */
    public static boolean doLinesIntersect(LineSegment a, LineSegment b) {
        Point[] box1 = a.getBoundingBox();
        Point[] box2 = b.getBoundingBox();
        if (!isInBoundingBox(box1, b.first) && !isInBoundingBox(box1, b.second)
                && !isInBoundingBox(box2, a.first)
                && !isInBoundingBox(box2, a.second)) {
            return false;
        } else {
            // Bounding boxes do have an intersection
            if (isPointOnLine(a, b.first) || isPointOnLine(a, b.second)
                    || isPointOnLine(b, a.first) || isPointOnLine(b, a.second)) {
                // An endpoint of one line is on the other line
                return true;
            } else {
                if (lineSegmentTouchesOrCrossesLine(a, b)
                        && lineSegmentTouchesOrCrossesLine(b, a)) {
                    // real intersection
                    return true;
                } else {
                    return false;
                }
            }
        }
    }
}
