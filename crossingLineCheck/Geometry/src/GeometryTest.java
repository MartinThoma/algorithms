import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

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

    /* Tests for doBoundingBoxesIntersect */
    public void testBoundingBoxesIntersectT1() {
        Point[] a = new Point[2];
        Point[] b = new Point[2];
        a[0] = new Point(0, 0);
        a[1] = new Point(5, 5);
        b[0] = new Point(1, 1);
        b[1] = new Point(2, 2);
        assertEquals(true, Geometry.doBoundingBoxesIntersect(a, b));
    }

    public void testBoundingBoxesIntersectT2() {
        Point[] a = new Point[2];
        Point[] b = new Point[2];
        a[0] = new Point(0, 0);
        a[1] = new Point(3, 3);
        b[0] = new Point(1, -1);
        b[1] = new Point(2, 7);
        assertEquals(true, Geometry.doBoundingBoxesIntersect(a, b));
    }

    public void testBoundingBoxesIntersectT3() {
        Point[] a = new Point[2];
        Point[] b = new Point[2];
        a[0] = new Point(0, 0);
        a[1] = new Point(3, 3);
        b[0] = new Point(1, -1);
        b[1] = new Point(2, 2);
        assertEquals(true, Geometry.doBoundingBoxesIntersect(a, b));
    }

    public void testBoundingBoxesIntersectT4() {
        Point[] a = new Point[2];
        Point[] b = new Point[2];
        a[0] = new Point(0, 0);
        a[1] = new Point(3, 3);
        b[0] = new Point(3, 3);
        b[1] = new Point(5, 5);
        assertEquals(true, Geometry.doBoundingBoxesIntersect(a, b));
    }

    public void testBoundingBoxesIntersectF1() {
        Point[] a = new Point[2];
        Point[] b = new Point[2];
        a[0] = new Point(0, 0);
        a[1] = new Point(3, 3);
        b[0] = new Point(4, 4);
        b[1] = new Point(5, 5);
        assertEquals(false, Geometry.doBoundingBoxesIntersect(a, b));
    }

    /* Tests for lineSegmentCrossesLine */
    public void testLineSegmentCorssesLine() {
        LineSegment lineSegment = new LineSegment(new Point(5, 5), new Point(
                17, 17));
        LineSegment line = new LineSegment(new Point(0, 0), new Point(1, 1));
        assertEquals(true, Geometry.lineSegmentTouchesOrCrossesLine(
                lineSegment, line));

        lineSegment = new LineSegment(new Point(17, 17), new Point(5, 5));
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
        LineSegment b = new LineSegment(new Point(2, 0), new Point(0.5, 2));
        assertEquals(false, Geometry.doLinesIntersect(a, b));
    }

    public void testLinesDontIntesectF7() {
        LineSegment a = new LineSegment(new Point(1, 1), new Point(4, 1));
        LineSegment b = new LineSegment(new Point(2, 2), new Point(3, 2));
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
        LineSegment a = new LineSegment(new Point(5, 5), new Point(0, 0));
        LineSegment b = new LineSegment(new Point(1, 1), new Point(8, 2));
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
        for (int i = 0; i < 50; i++) {
            double ax = Math.random();
            double ay = Math.random();
            double bx = Math.random();
            double by = Math.random();
            LineSegment a = new LineSegment(new Point(ax, ay),
                    new Point(bx, by));
            LineSegment b = new LineSegment(new Point(ax, ay),
                    new Point(bx, by));
            assertEquals(true, Geometry.doLinesIntersect(a, b));
        }
    }

    /* check getAllIntersectingLines() */
    public void testBlogExample() {
        LineSegment[] lines = new LineSegment[15];
        lines[0] = new LineSegment(new Point(1, 4), new Point(6, 1), "a");
        lines[1] = new LineSegment(new Point(2, 1), new Point(5, 4), "b");
        lines[2] = new LineSegment(new Point(3, 1), new Point(6, 4), "c");
        lines[3] = new LineSegment(new Point(4, 1), new Point(8, 5), "d");
        lines[4] = new LineSegment(new Point(3, 4), new Point(9, 3), "e");
        lines[5] = new LineSegment(new Point(7, 2), new Point(9, 3), "f");
        lines[6] = new LineSegment(new Point(6, 7), new Point(9, 1), "g");
        lines[7] = new LineSegment(new Point(11, 1), new Point(16, 5), "h");
        lines[8] = new LineSegment(new Point(13, 3), new Point(13, 4), "i");
        lines[9] = new LineSegment(new Point(15, 3), new Point(15, 4), "j");
        lines[10] = new LineSegment(new Point(13, 2), new Point(14, 2), "k");
        lines[11] = new LineSegment(new Point(14, 1), new Point(14, 2), "l");
        lines[12] = new LineSegment(new Point(17, 3), new Point(21, 3), "m");
        lines[13] = new LineSegment(new Point(19, 5), new Point(19, 1), "n");
        lines[14] = new LineSegment(new Point(11, 1), new Point(16, 5), "o");

        Set<LineSegment[]> intersections = new LinkedHashSet<LineSegment[]>();
        LineSegment[] add = new LineSegment[2];
        add[0] = lines[0];
        add[1] = lines[1];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[0];
        add[1] = lines[2];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[0];
        add[1] = lines[3];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[3];
        add[1] = lines[6];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[4];
        add[1] = lines[1];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[4];
        add[1] = lines[2];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[4];
        add[1] = lines[3];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[4];
        add[1] = lines[5];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[4];
        add[1] = lines[6];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[5];
        add[1] = lines[6];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[10];
        add[1] = lines[11];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[12];
        add[1] = lines[13];
        intersections.add(add);
        add = new LineSegment[2];
        add[0] = lines[7];
        add[1] = lines[14];
        intersections.add(add);

        Set<LineSegment[]> intersectionsBrute = Geometry
                .getAllIntersectingLinesByBruteForce(lines);
        Set<LineSegment[]> intersectionsSweep = Geometry
                .getAllIntersectingLines(lines);

        System.out.println(Arrays.deepToString(intersections.toArray()));
        System.out.println(Arrays.deepToString(intersectionsBrute.toArray()));
        System.out.println(Arrays.deepToString(intersectionsSweep.toArray()));

        assertEquals(true, intersectionsBrute.equals(intersections));

        // twice [e,g], but not [[d, g], [e, c], [e, d], [e, f]]
        assertEquals(true, intersectionsSweep.equals(intersections));
    }

    public void testCompareToBruteForce() {
        int n = 30;
        int maxIntersections = (n * n - n) / 2;

        LineSegment[] lines = new LineSegment[n];
        for (int i = 0; i < n; i++) {
            Point a = new Point(Math.random(), Math.random());
            Point b = new Point(Math.random(), Math.random());
            lines[i] = new LineSegment(a, b);
        }

        Set<LineSegment[]> intersectionsBrute = Geometry
                .getAllIntersectingLinesByBruteForce(lines);
        Set<LineSegment[]> intersectionsSweep = Geometry
                .getAllIntersectingLines(lines);
        assertEquals(true, intersectionsBrute.size() <= maxIntersections);
        System.out.println("Brute: " + intersectionsBrute.size());
        System.out.println("Sweep: " + intersectionsSweep.size());
        assertEquals(true, intersectionsBrute.equals(intersectionsSweep));
    }

    /* test getConvexHull */
    public void testGetConvexHullQuadratic() {
        int n = 30;
        List<Point> l = new ArrayList<Point>();

        for (int i = 0; i < n; i++) {
            l.add(new Point(i, i * i));
        }

        Collections.shuffle(l);

        List<Point> convexHull = Geometry.getConvexHull(l);
        System.out.println(l);
        assertEquals(true, convexHull.equals(l));
    }

    public void testGetConvexHullMinimal() {
        List<Point> l = new ArrayList<Point>();
        l.add(new Point(3, 0));
        l.add(new Point(5, 1));
        l.add(new Point(5, 3));
        l.add(new Point(6, 4));
        l.add(new Point(4, 5));
        l.add(new Point(1, 3));

        List<Point> solution = new ArrayList<Point>();
        solution.add(new Point(3, 0));
        solution.add(new Point(5, 1));
        solution.add(new Point(6, 4));
        solution.add(new Point(4, 5));
        solution.add(new Point(1, 3));

        List<Point> convexHull = Geometry.getConvexHull(l);
        System.out.println(l);
        assertEquals(true, convexHull.equals(l));
    }
}
