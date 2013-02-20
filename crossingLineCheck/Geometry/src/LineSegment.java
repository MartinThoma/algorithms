public class LineSegment {
    Point first;
    Point second;

    /**
     * @param first the first point of this line
     * @param second the second point of this line
     */
    public LineSegment(Point a, Point b) {
        this.first = a;
        this.second = b;
    }

    public Point[] getBoundingBox() {
        Point[] result = new Point[2];
        result[0] = new Point(Math.min(first.x, second.x), Math.min(first.y,
                second.y));
        result[1] = new Point(Math.max(first.x, second.x), Math.max(first.y,
                second.y));
        return result;
    }
}
