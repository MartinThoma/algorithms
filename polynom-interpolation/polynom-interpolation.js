'use strict';

/* global variables */
var STRETCH_X = 1;
var STRETCH_Y = 1;
var X_MIN = -10;
var X_MAX = +10;
var Y_MIN = -10;
var Y_MAX = +10;
var X_OFFSET = 256;
var Y_OFFSET = 100;
var points = [];
var canvas = document.getElementById("myCanvas");
var context = canvas.getContext("2d");

function setCursorByID(id, cursorStyle) {
    var elem = document.getElementById(id);
    elem.style.cursor = cursorStyle;
}

/** 
 * Calculates coordinates from worldspace to screenspace
 * @param {Number} x the coordinate you want to transform
 * @param {bool} isX true iff x is a x-coordinate, otherwise false
 * @return {Number} transformed coordinate
 */
function c(x, isX) {
    if (isX) {
        return STRETCH_X * (x + X_OFFSET);
    }

    return STRETCH_Y * (-x + Y_OFFSET);
}

/** 
 * Calculates coordinates from screenspace to worldspace
 * @param {Number} x the coordinate you want to transform
 * @param {bool} isX true iff x is a x-coordinate, otherwise false
 * @return {Number} transformed coordinate
 */
function r(x, isX) {
    if (isX) {
        return x / STRETCH_X - X_OFFSET;
    }

    return -x / STRETCH_Y + Y_OFFSET;
}

/**
 * Draw everything on canvas.
 * @param {DOMElement} canvas
 * @return {undefined}
 */
function drawBoard(canvas) {
    var context = canvas.getContext('2d');
    X_MIN = parseFloat(document.getElementById("X_MIN").value, 10);
    X_MAX = parseFloat(document.getElementById("X_MAX").value, 10);
    Y_MIN = parseFloat(document.getElementById("Y_MIN").value, 10);
    Y_MAX = parseFloat(document.getElementById("Y_MAX").value, 10);

    // make canvas as big as possible
    context.canvas.width = window.innerWidth - 50;
    context.canvas.height = window.innerHeight - 100;
    context.clearRect(0, 0, canvas.width, canvas.height);

    // stretch
    STRETCH_X = context.canvas.width / Math.abs(X_MAX - X_MIN);
    STRETCH_Y = context.canvas.height / Math.abs(Y_MAX - Y_MIN);

    // Adjust general settings to canvas size
    X_OFFSET = context.canvas.width / (STRETCH_X * 2);
    Y_OFFSET = context.canvas.height / (STRETCH_Y * 2);

    // grid
    context.strokeStyle = "#CDCDCD";
    for (var x = 0; x < X_MAX; x += 10) {
        context.beginPath();
        context.moveTo(c(x, true), c(Y_MIN, false));
        context.lineTo(c(x, true), c(Y_MAX, false));
        context.stroke();
    }
    for (var x = 0; x > X_MIN; x -= 10) {
        context.beginPath();
        context.moveTo(c(x, true), c(Y_MIN, false));
        context.lineTo(c(x, true), c(Y_MAX, false));
        context.stroke();
    }
    for (var y = 0; y < Y_MAX; y += 10) {
        context.beginPath();
        context.moveTo(c(X_MIN, true), c(y, false));
        context.lineTo(c(X_MAX, true), c(y, false));
        context.stroke();
    }
    for (var y = 0; y > Y_MIN; y -= 10) {
        context.beginPath();
        context.moveTo(c(X_MIN, true), c(y, false));
        context.lineTo(c(X_MAX, true), c(y, false));
        context.stroke();
    }
    context.strokeStyle = "#000000";

    // x-axis
    context.beginPath();
    context.moveTo(c(X_MIN, true), c(0, false));
    context.lineTo(c(X_MAX, true), c(0, false));
    context.closePath();
    context.stroke();

    // y-axis
    context.beginPath();
    context.moveTo(c(0, true), c(Y_MIN));
    context.lineTo(c(0, true), c(Y_MAX));
    context.closePath();
    context.stroke();

    // x-ticks
    var X_TICKS_STEPS = parseFloat(document.getElementById("X_TICKS_STEPS").value);
    if (X_TICKS_STEPS > 0) {
        for (var x = 0; x < X_MAX; x += X_TICKS_STEPS) {
            context.beginPath();
            context.moveTo(c(x, true), c(0) + 10);
            context.lineTo(c(x, true), c(0) - 10);
            context.closePath();
            context.stroke();
        }
        for (var x = 0; x > X_MIN; x -= X_TICKS_STEPS) {
            context.beginPath();
            context.moveTo(c(x, true), c(0) + 10);
            context.lineTo(c(x, true), c(0) - 10);
            context.closePath();
            context.stroke();
        }
    }

    // y-ticks
    var Y_TICKS_STEPS = parseFloat(document.getElementById("Y_TICKS_STEPS").value);
    if (Y_TICKS_STEPS > 0) {
        for (var y = 0; y > Y_MIN; y -= Y_TICKS_STEPS) {
            context.beginPath();
            context.moveTo(c(0, true) - 10, c(y, false));
            context.lineTo(c(0, true) + 10, c(y, false));
            context.closePath();
            context.stroke();
        }
        for (var y = 0; y < Y_MAX; y += Y_TICKS_STEPS) {
            context.beginPath();
            context.moveTo(c(0, true) - 10, c(y, false));
            context.lineTo(c(0, true) + 10, c(y, false));
            context.closePath();
            context.stroke();
        }
    }

    // arrow x
    context.beginPath();
    context.moveTo(context.canvas.width - 30, context.canvas.height / 2 - 10);
    context.lineTo(context.canvas.width, context.canvas.height / 2);
    context.lineTo(context.canvas.width - 30, context.canvas.height / 2 + 10);
    context.lineTo(context.canvas.width - 25, context.canvas.height / 2);
    context.closePath();
    context.stroke();
    context.fill();


    // arrow y
    context.beginPath();
    context.moveTo(context.canvas.width / 2 - 10, 30);
    context.lineTo(context.canvas.width / 2, 0);
    context.lineTo(context.canvas.width / 2 + 10, 30);
    context.lineTo(context.canvas.width / 2, 25);
    context.closePath();
    context.stroke();
    context.fill();

    drawPoints();
    writePointList();
    var polynomial = {};
    for (var power = 0; power < points.length; power++) {
        polynomial[power] = 0;
    }

    var f = document.getElementById("function").value;

    // calculate coefficients for monom and draw
    {
        var A = setGauss(points);
        var x = gauss(A);

        for (var power = 0; power < points.length; power++) {
            polynomial[power] = x[power];
        }

        drawPolynomial(canvas, polynomial, 'blue');
        drawFunction(f, 'red');
    }

    // calculate and draw spline
    if (document.getElementById("SHOW_SPLINE_EQUALLY_SPACED").checked) {
        var SPLINE_COLOR = document.getElementById("SPLINE_COLOR").value;
        document.getElementById("SPLINE_LABEL").style.color = SPLINE_COLOR;
        spline(f, SPLINE_COLOR);
    }

    // equally spaced
    if (document.getElementById("SHOW_EQUALLY_SPACED").checked) {
        var EQUALLY_SPACED_COLOR = document.getElementById("EQUALLY_SPACED_COLOR").value;
        document.getElementById("EQUALLY_SPACED_LABEL").style.color = EQUALLY_SPACED_COLOR;
        var pointList = drawEquallySpacedPoints(f, EQUALLY_SPACED_COLOR);
        var A = setGauss(pointList);
        var x = gauss(A);

        for (var power = 0; power < pointList.length; power++) {
            polynomial[power] = x[power];
        }

        drawPolynomial(canvas, polynomial, EQUALLY_SPACED_COLOR);
    }

    // tschebyscheff spaced
    if (document.getElementById("SHOW_TSCHEBYSCHEFF_SPACED").checked) {
        var TSCHEBYSCHEFF_SPACED_COLOR = document.getElementById("TSCHEBYSCHEFF_SPACED_COLOR").value;
        document.getElementById("TSCHEBYSCHEFF_SPACED_LABEL").style.color = TSCHEBYSCHEFF_SPACED_COLOR;
        var pointList = drawTschebyscheffSpacedPoints(f, TSCHEBYSCHEFF_SPACED_COLOR);
        var A = setGauss(pointList);
        var x = gauss(A);

        for (var power = 0; power < pointList.length; power++) {
            polynomial[power] = x[power];
        }

        drawPolynomial(canvas, polynomial, TSCHEBYSCHEFF_SPACED_COLOR);
    }
}

/**
 * Calculate spline and draw it to canvas.
 * done like in http://code.activestate.com/recipes/457658-cubic-spline-interpolator/
 * @param {function as string} f
 * @param {string} color
 * @return {undefined}
 */
function spline(f, color) {
    var x,y;
    var points = drawEquallySpacedPoints(f, color);

    for(var i=0; i<points.length-1; i++) {
        var u = points[i].x;
        var v = points[i+1].x;

        var FU = math.eval(f, {x: u});
        var FV = math.eval(f, {x: v});

        // Poor mans derivate :-/
        var h = parseFloat(document.getElementById("evaluationSteps").value);
        y = math.eval(f, {x: u+h});
        var DU = (y - FU) / h;
        y = math.eval(f, {x: v+h});
        var DV = (y - FV) / h;

        var denom = Math.pow((u - v),3);
        var a = ((-DV - DU) * v + (DV + DU) * u + 2 * FV - 2 * FU) / denom;
        var b = -((-DV - 2 * DU) * Math.pow(v,2)  + u * ((DU - DV) * v + 3 * FV - 3 * FU) + 3 * FV * v - 3 * FU * v + (2 * DV + DU) * Math.pow(u,2)) / denom;
        var C = (- DU * Math.pow(v,3)  + u * ((- 2 * DV - DU) * Math.pow(v,2)  + 6 * FV * v  - 6 * FU * v) + (DV + 2 * DU) * Math.pow(u,2) * v + DV * Math.pow(u,3)) / denom; // ATTENTION! THERE IS A FUNCTION CALLED 'c'!!!!
        var d = -(u *(-DU * Math.pow(v,3)  - 3 * FU * Math.pow(v,2)) + FU * Math.pow(v,3) + Math.pow(u,2) * ((DU - DV) * Math.pow(v,2) + 3 * FV * v) +  Math.pow(u,3) * (DV * v - FV)) / denom;
        //var m = {'a': a, 'b': b, 'c': c, 'd': d, 'u':u, 'v':v};

        context.strokeStyle = color;
        context.beginPath();
        var isFirst = true;
        for (var x = u; x <= v; x += 0.01) {
            y = a*x*x*x + b*x*x + C*x + d;
            if (isFirst) {
                context.moveTo(c(x, true), c(y, false));
                isFirst = false;
            } else {
                context.lineTo(c(x, true), c(y, false));
            }
        }
        context.stroke();
    }
}

/**
 * Calculated positions of equally spaced points and draw them to
 * canvas.
 * @param {function as string} f
 * @param {string} color
 * @return {Array} list of equally spaced points as list of maps
 */
function drawEquallySpacedPoints(f, color) {
    var context = canvas.getContext('2d');
    context.beginPath();
    context.strokeStyle = color;
    var n = parseInt(document.getElementById("N_EVALUATION_POINTS").value, 10);
    var X_FROM = parseFloat(document.getElementById("X_FROM").value, 10);
    var X_TO = parseFloat(document.getElementById("X_TO").value, 10);
    var evaluationSteps = (X_TO - X_FROM) / n;
    var pointList = new Array(n + 1);
    if (evaluationSteps > 0) {
        var i = 0;
        var y = 0;
        for (var x = X_FROM; x <= X_TO; x += evaluationSteps) {
            y = math.eval(f, {x: x});
            pointList[i] = {
                "x": x,
                "y": y
            };
            i++;
        }
        drawPointsGeneral(pointList, color);
    }
    return pointList;
}

function affineTransformation(y, a, b) {
    return (0.5 * y) * (b - a); // - (a+b)/(b-a);
}

/**
 * Calculated positions of tschebyscheff spaced points and draw them to
 * canvas.
 * @param {function as string} f
 * @param {string} color
 * @return {Array} list of equally spaced points as list of maps
 */
function drawTschebyscheffSpacedPoints(f, color) {
    var context = canvas.getContext('2d');
    context.beginPath();
    context.strokeStyle = color;
    var n = parseInt(document.getElementById("N_EVALUATION_POINTS").value, 10);
    var evaluationSteps = (X_MAX - X_MIN) / n;
    var pointList = new Array(n + 1);
    if (evaluationSteps > 0) {
        var i = 0;
        for (var i = 0; i <= n; i++) {
            var x = Math.cos((2.0 * i + 1) / (2 * n + 2) * Math.PI);
            x = affineTransformation(x, parseFloat(document.getElementById("X_FROM").value, 10), parseFloat(document.getElementById("X_TO").value, 10));
            var y = 0;
            y = math.eval(f, {x: x});
            pointList[i] = {
                "x": x,
                "y": y
            };
        }
        drawPointsGeneral(pointList, color);
    }
    return pointList;
}

/**
 * Draw points to canvas.
 * @param {Array} pointList
 * @param {string} color
 * @return {undefined}
 */
function drawPointsGeneral(pointList, color) {
    for (var i = 0; i < pointList.length; i++) {
        context.beginPath();
        if (pointList[i] !== undefined) {
        context.arc(c(pointList[i].x, true),
            c(pointList[i].y, false),
            2, /*radius*/
            0, 2 * Math.PI, false);
        }

        context.lineWidth = 1;
        context.strokeStyle = 'black';
        context.fillStyle = color;
        context.fill();
        context.stroke();
    }
}

/**
 * Generate a linear system of equations and store them to a 
 * n×(n+1) matrix.
 * @param {Array} points
 * @return {Array} 
 */
function setGauss(points) {
    var n = points.length - 1;
    var A = new Array(n + 1);
    for (var i = 0; i < n + 1; i++) {
        A[i] = new Array(n + 2);
        if (points[i] != undefined) {
            var x = points[i].x;
            for (var j = 0; j < n + 1; j++) {
                A[i][j] = Math.pow(x, j);
            }
            A[i][n + 1] = points[i].y;
        }
    }
    return A;
}

/** 
 * Solve a linear system of equations given by a n×n matrix A 
 * with a n×1 result vector b. 
 * @param {matrix} A|b
 * @return {array} x
 */
function gauss(A) {
    var n = A.length;

    for (var i = 0; i < n; i++) {
        // Search for maximum in this column
        var maxEl = Math.abs(A[i][i]);
        var maxRow = i;
        for (var k = i + 1; k < n; k++) {
            if (Math.abs(A[k][i]) > maxEl) {
                maxEl = Math.abs(A[k][i]);
                maxRow = k;
            }
        }

        // Swap maximum row with current row (column by column)
        for (var k = i; k < n + 1; k++) {
            var tmp = A[maxRow][k];
            A[maxRow][k] = A[i][k];
            A[i][k] = tmp;
        }

        // Make all rows below this one 0 in current column
        for (k = i + 1; k < n; k++) {
            var c = -A[k][i] / A[i][i];
            for (var j = i; j < n + 1; j++) {
                if (i == j) {
                    A[k][j] = 0;
                } else {
                    A[k][j] += c * A[i][j];
                }
            }
        }
    }

    // Solve equation Ax=b for an upper triangular matrix A
    var x = new Array(n);
    for (var i = n - 1; i > -1; i--) {
        x[i] = A[i][n] / A[i][i];
        for (var k = i - 1; k > -1; k--) {
            A[k][n] -= A[k][i] * x[i];
        }
    }
    return x;
}

/** 
 * Draw an arbitrary function.
 * @param {function as string} f
 * @param {string} color
 * @return {undefined}
 */
function drawFunction(f, color) {
    var context = canvas.getContext('2d');
    context.beginPath();
    context.strokeStyle = color;
    var evaluationSteps = parseFloat(document.getElementById("evaluationSteps").value);
    if (evaluationSteps > 0) {
        var y = 0;
        for (var x = X_MIN; x < X_MAX; x += evaluationSteps) {
            y = math.eval(f, {x: x});

            if(c(y,false) > canvas.height) {
                y=r(canvas.height, false);
            }

            if(c(y,false) < 0) {
                y=r(0, false);
            }


            if (x == X_MIN) {
                context.moveTo(c(x, true), c(y, false));
            } else {
                context.lineTo(c(x, true), c(y, false));
            }
        }
        context.stroke();
    }
}

/**
 * Draw polynomial and write it to the document.
 * @param {DOMElement} canvas
 * @param {Array} polynomial
 * @param {string} color
 * @return {undefined}
 */
function drawPolynomial(canvas, polynomial, color) {
    var context = canvas.getContext('2d');
    context.beginPath();
    context.strokeStyle = color;
    var evaluationSteps = parseFloat(document.getElementById("evaluationSteps").value);
    if (evaluationSteps > 0) {
        for (var x = X_MIN; x < X_MAX; x += evaluationSteps) {
            var y = 0;
            for (var power in polynomial) {
                y += polynomial[power] * Math.pow(x, power);
            }

            if(c(y,false) > canvas.height) {
                y=r(canvas.height, false);
            }

            if(c(y,false) < 0) {
                y=r(0, false);
            }


            if (x == X_MIN) {
                context.moveTo(c(x, true), c(y, false));
            } else {
                context.lineTo(c(x, true), c(y, false));
            }
        }
        context.stroke();
    }

    // Write polynomial to document
    var mathEl = document.getElementById("polynomial");
    mathEl.innerHTML = '$p(x) = ';
    for (var power in polynomial) {
        if (polynomial[power] !== 0) {
            if (polynomial[power] == 1) {
                mathEl.innerHTML += '+x^' + power + ' ';
            } else {
                mathEl.innerHTML += '+' + polynomial[power] + 'x^' + power + ' ';
            }
        }
    }
    mathEl.innerHTML += '$';
}

/**
 * Calcualte euklidean distance of two points.
 * @param {Map} p1
 * @param {Map} p2
 * @return {Number} euklidean distance of p1 and p2
 */
function euklideanDist(p1, p2) {
    return Math.sqrt(
        Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
}

/** 
 * Add or remove a point.
 * @param {event} event
 * @param {DOMElement} canvas
 * @param {map} mouseCoords
 * @return {undefined}
 */
function addPoint(event, canvas, mouseCoords) {
    if (event.ctrlKey) {
        // remove point that is nearest to mouse coords
        if (points.length >= 1) {
            var nearestMouseCIndex = 0;
            var nearestDist = euklideanDist(mouseCoords, points[0]);
            var mCoords = {
                "x": r(mouseCoords.x, true),
                "y": r(mouseCoords.y, false)
            };
            for (var i = 1; i < points.length; i++) {
                var tmpDist = euklideanDist(mCoords, points[i]);
                if (tmpDist < nearestDist) {
                    nearestDist = tmpDist;
                    nearestMouseCIndex = i;
                }
            }
            points.splice(nearestMouseCIndex, 1);
        }
    } else {
        points.push({
            "x": r(mouseCoords.x, true),
            "y": r(mouseCoords.y, false)
        });
    }
}

/** 
 * Draw all permanently added points.
 * @return {undefined}
 */
function drawPoints() {
    for (var i = 0; i < points.length; i++) {
        context.beginPath();
        context.arc(c(points[i].x, true),
            c(points[i].y, false),
            2, /*radius*/
            0, 2 * Math.PI, false);
        context.lineWidth = 1;
        context.strokeStyle = 'black';
        context.fillStyle = "rgb(0,0,0)";
        context.fill();
        context.stroke();
    }
}

/**
 * Write all points to textarea
 * @return {undefined}
 */
function writePointList() {
    var tArea = document.getElementById("pointlist");
    tArea.value = '';
    for (var i = 0; i < points.length; i++) {
        tArea.value += "(" + points[i].x + "|" + points[i].y + "), ";
    }
}

/** 
 * Get current position of mouse.
 * @param {DOMElement} canvas
 * @param {event} event
 * @return {map}
 */
function getMouseCoords(canvas, event) {
    var rect = canvas.getBoundingClientRect();
    return {
        "x": event.clientX - rect.left,
        "y": event.clientY - rect.top
    };
}

function store() {
	var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream"); // here is the most important part because if you dont replace you will get a DOM 18 exception.
	window.location.href=image; // it will save locally
}

/**
 * Modify url so that I can later read all information from it.
 * @return {undefined}
 */
function modifyURL() {
    var f = encodeURIComponent(document.getElementById("function").value);
    var evaluationSteps = encodeURIComponent(document.getElementById("evaluationSteps").value);
    var X_MIN = encodeURIComponent(document.getElementById("X_MIN").value);
    var X_MAX = encodeURIComponent(document.getElementById("X_MAX").value);
    var Y_MAX = encodeURIComponent(document.getElementById("Y_MAX").value);
    var Y_MIN = encodeURIComponent(document.getElementById("Y_MIN").value);
    var xt = encodeURIComponent(document.getElementById("X_TICKS_STEPS").value);
    var yt = encodeURIComponent(document.getElementById("Y_TICKS_STEPS").value);
    var X_FROM = encodeURIComponent(document.getElementById("X_FROM").value);
    var X_TO = encodeURIComponent(document.getElementById("X_TO").value);
    var equallySwitch = encodeURIComponent(document.getElementById("SHOW_EQUALLY_SPACED").checked);
    var tschebyscheffSwitch = encodeURIComponent(document.getElementById("SHOW_TSCHEBYSCHEFF_SPACED").checked);
    var N_EVALUATION_POINTS = encodeURIComponent(document.getElementById("N_EVALUATION_POINTS").value);
	var SHOW_SPLINE_EQUALLY_SPACED = encodeURIComponent(document.getElementById("SHOW_SPLINE_EQUALLY_SPACED").checked);
    document.getElementById("newWindow").href = "polynom-interpolation.htm?function=" + f + "&evaluationSteps=" + evaluationSteps + "&X_MIN=" + X_MIN + "&X_MAX=" + X_MAX + "&Y_MAX=" + Y_MAX + "&Y_MIN=" + Y_MIN + "&X_TICKS_STEPS=" + xt + "&Y_TICKS_STEPS=" + yt + "&X_FROM=" +X_FROM+"&X_TO=" +X_TO+"&N_EVALUATION_POINTS=" +N_EVALUATION_POINTS+ "&points=" + encodeURIComponent(JSON.stringify(points)) + "&tschebyscheffSwitch="+tschebyscheffSwitch+"&equallySwitch="+equallySwitch+"&SHOW_SPLINE_EQUALLY_SPACED="+SHOW_SPLINE_EQUALLY_SPACED;
}

window.onload = function WindowLoad(event) {
    var qs = (function (a) {
        if (a === ""){
            return {};
        }

        var b = {};
        for (var i = 0; i < a.length; ++i) {
            var p = a[i].split('=');
            if (p.length != 2){
                continue;
            }

            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'));

    var parameters = ["function", "X_TICKS_STEPS", "Y_TICKS_STEPS", "X_MIN", "X_MAX", "Y_MIN", "Y_MAX", "evaluationSteps", "X_FROM", "X_TO", "N_EVALUATION_POINTS"];
    for (var i = 0; i < parameters.length; i++) {
        if (qs[parameters[i]] != undefined) {
            document.getElementById(parameters[i]).value = qs[parameters[i]];
        }
    }

    if (qs.points !== undefined) {
        points = JSON.parse(qs.points);
    }

    if (qs.equallySwitch !== undefined) {
        document.getElementById("SHOW_EQUALLY_SPACED").checked = (qs.equallySwitch === 'true');
    }

    if (qs.tschebyscheffSwitch !== undefined) {
        document.getElementById("SHOW_TSCHEBYSCHEFF_SPACED").checked = (qs.tschebyscheffSwitch === 'true');
    }

    if (qs.SHOW_SPLINE_EQUALLY_SPACED !== undefined) {
        document.getElementById("SHOW_SPLINE_EQUALLY_SPACED").checked = (qs.SHOW_SPLINE_EQUALLY_SPACED === 'true');
    }

    drawBoard(canvas, {
        "x": 0,
        "y": 0
    }, 10);
    setCursorByID("myCanvas", "crosshair");

    /** scroll */
    function scroll(event) {
        var wheel;

        event.preventDefault();
        //var mousex = event.clientX - canvas.offsetLeft;
        //var mousey = event.clientY - canvas.offsetTop;

        if (event.wheelDelta !== undefined) {
            wheel = parseInt(event.wheelDelta, 10) / 120; //n or -n
        } else {
            wheel = parseInt(event.detail, 10) * (-1/3);
        }

        if (parseFloat(document.getElementById("X_MAX").value, 10) - wheel > 0) {
            document.getElementById("X_MIN").value = parseFloat(document.getElementById("X_MIN").value, 10) + wheel;
            document.getElementById("X_MAX").value = parseFloat(document.getElementById("X_MAX").value, 10) - wheel;
            document.getElementById("Y_MIN").value = parseFloat(document.getElementById("Y_MIN").value, 10) + wheel;
            document.getElementById("Y_MAX").value = parseFloat(document.getElementById("Y_MAX").value, 10) - wheel;
            drawBoard(canvas, {
                "x": 0,
                "y": 0
            }, 10);
        }
    }

    var mousewheelevt=(/Firefox/i.test(navigator.userAgent))? "DOMMouseScroll" : "mousewheel"; //FF doesn't recognize mousewheel as of FF3.x

    if (canvas.attachEvent){ //if IE (and Opera depending on user setting)
            canvas.attachEvent("on"+mousewheelevt, scroll);
    } else if (document.addEventListener) { //WC3 browsers
        canvas.addEventListener(mousewheelevt, scroll, false);
    }

    /** event listeners */
    canvas.addEventListener('mousemove',
        function (evt) {
            var mouseCoords = getMouseCoords(canvas, evt);
            drawBoard(canvas, mouseCoords, 10);
            // draw coordinates next to mouse
            context.fillStyle = "blue";
            context.font = "bold 16px Arial";
            var x = r(mouseCoords.x, true).toFixed(3);
            var y = r(mouseCoords.y, false).toFixed(3);
            context.fillText("(" + x + ", " + y + ")", mouseCoords.x + 5, mouseCoords.y - 5);
        }, false);

    canvas.addEventListener("mousedown",
        function (event) {
            var mouseCoords = getMouseCoords(canvas, event);
            addPoint(event, canvas, mouseCoords);
        }, false);
};
