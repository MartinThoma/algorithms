import java.util.ArrayList;
import java.util.List;

import junit.framework.TestCase;

public class GeometryTest extends TestCase {

    /* Test crossProduct */
    public void testAntisymmetryOfCrossProduct() {
        List<Point> l = new ArrayList<Point>();
        l.add(new Point(0, 0));
        l.add(new Point(1, 1));
        for (int i = 0; i < 50; i++) {
            l.add(new Point(Math.random(), Math.random()));
        }

        for (Point p1 : l) {
            for (Point p2 : l) {
                double r1 = Geometry.crossProduct(p1, p2);
                double r2 = Geometry.crossProduct(p2, p1);
                boolean isAntisymmetric = Math.abs(r1 + r2) < Geometry.EPSILON;
                assertEquals("[ " + p1 + ", " + p2 + "]", true, isAntisymmetric);
            }
        }
    }

    /* Tests for isPointRightOfLine */
    public void testPointRightOfLine() {
        LineSegment line = new LineSegment(new Point(0, 0), new Point(0, 7));
        Point a = new Point(5, 5);
        assertEquals(true, Geometry.isPointRightOfLine(line, a));
    }

    public void testPointLeftOfLine() {
        LineSegment line = new LineSegment(new Point(0, 0), new Point(0, 7));
        Point a = new Point(-5, 5);
        assertEquals(false, Geometry.isPointRightOfLine(line, a));
    }

    public void testPointOnLine() {
        LineSegment line = new LineSegment(new Point(0, 0), new Point(4, 4));
        Point a = new Point(3, 3);
        assertEquals(false, Geometry.isPointRightOfLine(line, a));

        line = new LineSegment(new Point(4, 4), new Point(0, 0));
        assertEquals(false, Geometry.isPointRightOfLine(line, a));
    }

    /* Tests for isInBoundingBox */
    public void testOutsiteOfBoundingBox() {
        Point[] box = new Point[2];
        Point a = new Point(0, 0);
        box[0] = new Point(1, 1);
        box[1] = new Point(2, 2);
        assertEquals(false, Geometry.isInBoundingBox(box, a));
    }

    public void testInsideOfBoundingBox() {
        Point[] box = new Point[2];
        Point a = new Point(1, 1);
        box[0] = new Point(0, 0);
        box[1] = new Point(2, 2);
        assertEquals(true, Geometry.isInBoundingBox(box, a));
    }

    public void testCornerOfBoundingBox() {
        Point[] box = new Point[2];
        Point a = new Point(0, 0);
        box[0] = new Point(0, 0);
        box[1] = new Point(2, 2);
        assertEquals(true, Geometry.isInBoundingBox(box, a));
    }

    /* Tests for lineSegmentCrossesLine */
    public void testLineSegmentCorssesLine() {
        LineSegment lineSegment = new LineSegment(new Point(5, 5), new Point(
                17, 17));
        LineSegment line = new LineSegment(new Point(0, 0), new Point(1, 1));
        assertEquals(true, Geometry.lineSegmentTouchesOrCrossesLine(
                lineSegment, line));

        lineSegment = new LineSegment(new Point(17, 17), new Point(
                5, 5));
        line = new LineSegment(new Point(0, 0), new Point(1, 1));
        assertEquals(true, Geometry.lineSegmentTouchesOrCrossesLine(
                lineSegment, line));
    }

    /* Tests for doLinesIntersect */
    public void testLinesDontIntesectF1() {
        LineSegment a = new LineSegment(new Point(0, 0), new Point(7, 7));
        LineSegment b = new LineSegment(new Point(3, 4), new Point(4, 5));
        assertEquals(false, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDontIntesectF2() {
        LineSegment a = new LineSegment(new Point(-4, 4), new Point(-2, 1));
        LineSegment b = new LineSegment(new Point(-2, 3), new Point(0, 0));
        assertEquals(false, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDontIntesectF3() {
        LineSegment a = new LineSegment(new Point(0, 0), new Point(0, 1));
        LineSegment b = new LineSegment(new Point(2, 2), new Point(2, 3));
        assertEquals(false, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDontIntesectF4() {
        LineSegment a = new LineSegment(new Point(0, 0), new Point(0, 1));
        LineSegment b = new LineSegment(new Point(2, 2), new Point(3, 2));
        assertEquals(false, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDontIntesectF5() {
        LineSegment a = new LineSegment(new Point(-1, -1), new Point(2, 2));
        LineSegment b = new LineSegment(new Point(3, 3), new Point(5, 5));
        assertEquals(false, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDontIntesectF6() {
        LineSegment a = new LineSegment(new Point(0, 0), new Point(1, 1));
        LineSegment b = new LineSegment(new Point(2, 0), new Point(2, 0.5));
        assertEquals(false, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDontIntesectF8() {
        LineSegment a = new LineSegment(new Point(0, 5), new Point(6, 0));
        LineSegment b = new LineSegment(new Point(2, 1), new Point(2, 2));
        assertEquals(false, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDoIntesectT1() {
        LineSegment a = new LineSegment(new Point(0, -2), new Point(0, 2));
        LineSegment b = new LineSegment(new Point(-2, 0), new Point(2, 0));
        assertEquals(true, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDoIntesectT2() {
        LineSegment a = new LineSegment(new Point(7, 7), new Point(0, 0));
        LineSegment b = new LineSegment(new Point(3, 3), new Point(15, 2));
        assertEquals(true, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDoIntesectT3() {
        LineSegment a = new LineSegment(new Point(-1, 0), new Point(0, 0));
        LineSegment b = new LineSegment(new Point(-1, -1), new Point(-1, 1));
        assertEquals(true, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDoIntesectT4() {
        LineSegment a = new LineSegment(new Point(0, 2), new Point(2, 2));
        LineSegment b = new LineSegment(new Point(2, 0), new Point(2, 4));
        assertEquals(true, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDoIntesectT5() {
        LineSegment a = new LineSegment(new Point(0, 0), new Point(5, 5));
        LineSegment b = new LineSegment(new Point(1, 1), new Point(3, 3));
        assertEquals(true, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDoIntesectT6() {
        LineSegment a = new LineSegment(new Point(-27, 33), new Point(-7, 13));
        LineSegment b = new LineSegment(new Point(-27, 33), new Point(-7, 13));
        assertEquals(true, Geometry.doLinesIntersect(a, b));
    }
}
