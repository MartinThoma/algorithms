public class Geometry {
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
     * Check if line segment first touches or crosses the line that is defined
     * by line segment second.
     *
     * @param first line segment first
     * @param second line second
     * @return <code>true</code> if line segment first touches line second,
     *         <code>false</code> otherwise.
     */
    public static boolean lineSegmentCrossesLine(LineSegment a, LineSegment b) {
        return isPointRightOfLine(a, b.first) ^ isPointRightOfLine(a, b.second);
    }

    public static boolean isPointRightOfLine(LineSegment a, Point b) {
        // Move the image, so that a.first is on (0|0)
        LineSegment a_tmp = new LineSegment(new Point(0, 0), new Point(
                a.second.x - a.first.x, a.second.y - a.first.y));
        Point b_tmp = new Point(b.x - a.first.x, b.y - a.second.y);
        System.out.println(crossProduct(a_tmp.second, b_tmp));
        return (crossProduct(a_tmp.second, b_tmp) < 0);
    }

    public static boolean doLinesIntersect(LineSegment a, LineSegment b) {
        Point[] box1 = a.getBoundingBox();
        Point[] box2 = b.getBoundingBox();
        if (!isInBoundingBox(box1, b.first) && !isInBoundingBox(box1, b.second)
                && !isInBoundingBox(box2, a.first)
                && !isInBoundingBox(box2, a.second)) {
            return false;
        } else {
            // TODO bounding box check is not enough
            return true;
        }
    }
}
