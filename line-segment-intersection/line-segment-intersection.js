'use strict';

var canvas = document.getElementById('myCanvas');
var context = canvas.getContext('2d');
var POINT_RADIUS = 5;
var points = [{"x": 0, "y": 0},{"x": 200, "y": 200},{"x": 20, "y": 100},{"x": 500, "y": 100}];
updateBoard();
var EPSILON = 0.000001;

function updateBoard(){
    var canvas = document.getElementById("myCanvas");var canvas = document.getElementById("myCanvas");
    drawBoard(canvas, {"x":0,"y":0});
    var a = {"first":points[0], "second": points[1]};
    var b = {"first":points[2], "second": points[3]};

    /* bounding box indicator */
    var bbIndicator = document.getElementById("boundingBoxInd");
    var box1 = getBoundingBox(a);
    var box2 = getBoundingBox(b);
    if(doBoundingBoxesIntersect(box1, box2)){
        bbIndicator.style.backgroundColor = "green";
    } else {
        bbIndicator.style.backgroundColor = "red";
    }

    /* lineSegmentTouchesOrCrossesLine(a, b) */
    var lsABIndicator = document.getElementById("lineSegementABInd");
    if(lineSegmentTouchesOrCrossesLine(a, b)){
        lsABIndicator.style.backgroundColor = "green";
    } else {
        lsABIndicator.style.backgroundColor = "red";
    }

    /* lineSegmentTouchesOrCrossesLine(b, a) */
    var lsBAIndicator = document.getElementById("lineSegementBAInd");
    if(lineSegmentTouchesOrCrossesLine(b, a)){
        lsBAIndicator.style.backgroundColor = "green";
    } else {
        lsBAIndicator.style.backgroundColor = "red";
    }

    /* get intersection, if possible */
    if (doLinesIntersect(a, b)) {
        var intersection = getIntersection(a, b);
        context.beginPath();
        context.arc(intersection["first"]["x"],
                    intersection["first"]["y"],
                    5,
                    0, 2 * Math.PI, false);
        context.lineWidth = 1;
        context.strokeStyle = 'black';
        context.fillStyle = "green";
        context.fill();
        context.stroke();

        context.beginPath();
        context.arc(intersection["second"]["x"],
                    intersection["second"]["y"],
                    5,
                    0, 2 * Math.PI, false);
        context.lineWidth = 1;
        context.strokeStyle = 'black';
        context.fillStyle = "yellow";
        context.fill();
        context.stroke();
    }
}

/** You know that lines a and b have an intersection and now you
    want to get it!
*/
function getIntersection(a, b) {
    /* the intersection [(x1,y1), (x2, y2)]
       it might be a line or a single point. If it is a line,
       then x1 = x2 and y1 = y2.  */
    var x1, y1, x2, y2;

   if (a["first"]["x"] == a["second"]["x"]) {
        // Case (A)
        // As a is a perfect vertical line, it cannot be represented
        // nicely in a mathematical way. But we directly know that
        //
        x1 = a["first"]["x"];
        x2 = x1;
        if (b["first"]["x"] == b["second"]["x"]) {
            // Case (AA): all x are the same!
            // Normalize
            if(a["first"]["y"] > a["second"]["y"]) {
                a = {"first": a["second"], "second": a["first"]};
            }
            if(b["first"]["y"] > b["second"]["y"]) {
                b = {"first": b["second"], "second": b["first"]};
            }
            if(a["first"]["y"] > b["first"]["y"]) {
                var tmp = a;
                a = b;
                b = tmp;
            }

            // Now we know that the y-value of a["first"] is the
            // lowest of all 4 y values
            // this means, we are either in case (AAA):
            //   a: x--------------x
            //   b:    x---------------x
            // or in case (AAB)
            //   a: x--------------x
            //   b:    x-------x
            // in both cases:
            // get the relavant y intervall
            y1 = b["first"]["y"];
            y2 = Math.min(a["second"]["y"], b["second"]["y"]);
        } else {
            // Case (AB)
            // we can mathematically represent line b as
            //     y = m*x + t <=> t = y - m*x
            // m = (y1-y2)/(x1-x2)
            var m, t;
            m = (b["first"]["y"] - b["second"]["y"])/
                (b["first"]["x"] - b["second"]["x"]);
            t = b["first"]["y"] - m*b["first"]["x"];
            y1 = m*x1 + t;
            y2 = y1
        }
    } else if (b["first"]["x"] == b["second"]["x"]) {
        // Case (B)
        // essentially the same as Case (AB), but with
        // a and b switched
        x1 = b["first"]["x"];
        x2 = x1;

        var tmp = a;
        a = b;
        b = tmp;

        var m, t;
        m = (b["first"]["y"] - b["second"]["y"])/
            (b["first"]["x"] - b["second"]["x"]);
        t = b["first"]["y"] - m*b["first"]["x"];
        y1 = m*x1 + t;
        y2 = y1
    } else {
        // Case (C)
        // Both lines can be represented mathematically
        var ma, mb, ta, tb;
        ma = (a["first"]["y"] - a["second"]["y"])/
             (a["first"]["x"] - a["second"]["x"]);
        mb = (b["first"]["y"] - b["second"]["y"])/
             (b["first"]["x"] - b["second"]["x"]);
        ta = a["first"]["y"] - ma*a["first"]["x"];
        tb = b["first"]["y"] - mb*b["first"]["x"];
        if (ma == mb) {
            // Case (CA)
            // both lines are in parallel. As we know that they
            // intersect, the intersection could be a line
            // when we rotated this, it would be the same situation
            // as in case (AA)

            // Normalize
            if(a["first"]["x"] > a["second"]["x"]) {
                a = {"first": a["second"], "second": a["first"]};
            }
            if(b["first"]["x"] > b["second"]["x"]) {
                b = {"first": b["second"], "second": b["first"]};
            }
            if(a["first"]["x"] > b["first"]["x"]) {
                var tmp = a;
                a = b;
                b = tmp;
            }

            // get the relavant x intervall
            x1 = b["first"]["x"];
            x2 = Math.min(a["second"]["x"], b["second"]["x"]);
            y1 = ma*x1+ta;
            y2 = ma*x2+ta;
        } else {
            // Case (CB): only a point as intersection:
            // y = ma*x+ta
            // y = mb*x+tb
            // ma*x + ta = mb*x + tb
            // (ma-mb)*x = tb - ta
            // x = (tb - ta)/(ma-mb)
            x1 = (tb-ta)/(ma-mb);
            y1 = ma*x1+ta;
            x2 = x1;
            y2 = y1;
        }
    }

    return {"first": {"x":x1, "y":y1}, "second": {"x":x2, "y":y2}};
}

function setCursorByID(id,cursorStyle) {
    var elem;
    if (document.getElementById &&
    (elem=document.getElementById(id)) ) {
        if (elem.style) elem.style.cursor=cursorStyle;
    }
}

/** get the current position of the mouse */
function getMouseCoords(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        "x": evt.clientX - rect.left,
        "y": evt.clientY - rect.top
    };
}

/** draw all permanently added points */
function drawLines(canvas) {
    context.lineWidth = document.getElementById("lineWidth").value;

    context.strokeStyle = 'red';
    context.beginPath();
    context.moveTo(points[0]["x"], points[0]["y"]);
    context.lineTo(points[1]["x"], points[1]["y"]);
    context.closePath();
    context.stroke();

    context.strokeStyle = 'blue';
    context.beginPath();
    context.moveTo(points[2]["x"], points[2]["y"]);
    context.lineTo(points[3]["x"], points[3]["y"]);
    context.closePath();
    context.stroke();
}

function drawBoard(canvas, mouseCoords) {
    var context = canvas.getContext('2d');
    context.canvas.width  = window.innerWidth - 50;
    context.canvas.height = window.innerHeight - 120;
    context.clearRect(0, 0, canvas.width, canvas.height);

    drawLines(canvas);
}

/**
 * Calculate the cross product of two points.
 * @param a first point
 * @param b second point
 * @return the value of the cross product
 */
function crossProduct(a, b) {
    return a.x * b.y - b.x * a.y;
}

/**
 * Check if bounding boxes do intersect. If one bounding box
 * touches the other, they do intersect.
 * @param a first bounding box
 * @param b second bounding box
 * @return <code>true</code> if they intersect,
 *         <code>false</code> otherwise.
 */
function doBoundingBoxesIntersect(a, b) {
    return a[0].x <= b[1].x && a[1].x >= b[0].x && a[0].y <= b[1].y
            && a[1].y >= b[0].y;
}

/**
 * Checks if a Point is on a line
 * @param a line (interpreted as line, although given as line
 *                segment)
 * @param b point
 * @return <code>true</code> if point is on line, otherwise
 *         <code>false</code>
 */
function isPointOnLine(a, b) {
    // Move the image, so that a.first is on (0|0)
    var aTmp = {"first":{"x":0, "y":0}, "second":{"x":a.second.x - a.first.x, "y":a.second.y - a.first.y}};
    var bTmp = {"x":b.x - a.first.x, "y":b.y - a.first.y};
    var r = crossProduct(aTmp.second, bTmp);
    return Math.abs(r) < EPSILON;
}

/**
 * Checks if a point is right of a line. If the point is on the
 * line, it is not right of the line.
 * @param a line segment interpreted as a line
 * @param b the point
 * @return <code>true</code> if the point is right of the line,
 *         <code>false</code> otherwise
 */
function isPointRightOfLine(a, b) {
    // Move the image, so that a.first is on (0|0)
    var aTmp = {"first":{"x":0, "y":0}, "second":{"x":a.second.x - a.first.x, "y":a.second.y - a.first.y}};
    var bTmp = {"x":b.x - a.first.x, "y": b.y - a.first.y};
    return crossProduct(aTmp.second, bTmp) < 0;
}

/**
 * Check if line segment first touches or crosses the line that is
 * defined by line segment second.
 *
 * @param first line segment interpreted as line
 * @param second line segment
 * @return <code>true</code> if line segment first touches or
 *                           crosses line second,
 *         <code>false</code> otherwise.
 */
function lineSegmentTouchesOrCrossesLine(a, b) {
    return isPointOnLine(a, b.first)
            || isPointOnLine(a, b.second)
            || (isPointRightOfLine(a, b.first) ^ isPointRightOfLine(a,
                    b.second));
}

function getBoundingBox(a) {
    return [{"x":Math.min(a["first"]["x"], a["second"]["x"]),
             "y":Math.min(a["first"]["y"], a["second"]["y"])},
            {"x":Math.max(a["first"]["x"], a["second"]["x"]),
             "y":Math.max(a["first"]["y"], a["second"]["y"])}];
}

/**
 * Check if line segments intersect
 * @param a first line segment
 * @param b second line segment
 * @return <code>true</code> if lines do intersect,
 *         <code>false</code> otherwise
 */
function doLinesIntersect(a, b) {
    var box1 = getBoundingBox(a);
    var box2 = getBoundingBox(b);
    return doBoundingBoxesIntersect(box1, box2)
            && lineSegmentTouchesOrCrossesLine(a, b)
            && lineSegmentTouchesOrCrossesLine(b, a);
}

var isDragFlag = false;

canvas.addEventListener("mousedown",
    function(event) {
        var mouseCoords = getMouseCoords(canvas, event);
        var i = parseInt(document.getElementById("movePoint").value);
        points[i]["x"] = mouseCoords["x"];
        points[i]["y"] = mouseCoords["y"];
        updateBoard();
        isDragFlag = true;
    }, false);

canvas.addEventListener("mousemove",
    function(event) {
        if(isDragFlag) {
            var mouseCoords = getMouseCoords(canvas, event);
            var i = parseInt(document.getElementById("movePoint").value);
            points[i]["x"] = mouseCoords["x"];
            points[i]["y"] = mouseCoords["y"];
            updateBoard();
        }
    }, false);

canvas.addEventListener("mouseup",
    function(event) {
        isDragFlag = false;
    }, false);
