public class Point {

    double x;
    double y;

    /**
     * @param x the x-coordinate
     * @param y the y-coordinate
     */
    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public String toString() {
        return "(" + x + "|" + y + ")";
    }
}
