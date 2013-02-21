public class LineSegment {
    Point first;
    Point second;
    String name;

    /**
     * @param first the first point of this line
     * @param second the second point of this line
     */
    public LineSegment(Point a, Point b) {
        this.first = a;
        this.second = b;
        this.name = "LineSegment";
    }

    public LineSegment(Point a, Point b, String name) {
        this.first = a;
        this.second = b;
        this.name = name;
    }

    /**
     * Get the bounding box of this line by two points. The first point is in
     * the lower left corner, the second one at the upper right corner.
     *
     * @return the bounding box
     */
    public Point[] getBoundingBox() {
        Point[] result = new Point[2];
        result[0] = new Point(Math.min(first.x, second.x), Math.min(first.y,
                second.y));
        result[1] = new Point(Math.max(first.x, second.x), Math.max(first.y,
                second.y));
        return result;
    }

    @Override
    public String toString() {
        if (name.equals("LineSegment")) {
            return "LineSegment [" + first + " to " + second + "]";
        } else {
            return name;
        }
    }

    /* (non-Javadoc)
     * @see java.lang.Object#hashCode()
     */
    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((first == null) ? 0 : first.hashCode());
        result = prime * result + ((name == null) ? 0 : name.hashCode());
        result = prime * result + ((second == null) ? 0 : second.hashCode());
        return result;
    }

    /* (non-Javadoc)
     * @see java.lang.Object#equals(java.lang.Object)
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        LineSegment other = (LineSegment) obj;
        if (first == null) {
            if (other.first != null)
                return false;
        } else if (!first.equals(other.first))
            return false;
        if (name == null) {
            if (other.name != null)
                return false;
        } else if (!name.equals(other.name))
            return false;
        if (second == null) {
            if (other.second != null)
                return false;
        } else if (!second.equals(other.second))
            return false;
        return true;
    }
}
