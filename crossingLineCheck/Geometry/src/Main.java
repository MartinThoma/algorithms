
public class Main {

    /**
     * @param args
     */
    public static void main(String[] args) {
        LineSegment line = new LineSegment(new Point(0,0), new Point(5, 5));
        Point a = new Point(3,3);
        System.out.println(Geometry.isPointRightOfLine(line, a));
    }

}
