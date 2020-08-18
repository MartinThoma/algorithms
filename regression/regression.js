function setCursorByID(id,cursorStyle) {
    var elem;
    if (document.getElementById &&
    (elem=document.getElementById(id)) ) {
        if (elem.style) elem.style.cursor=cursorStyle;
    }
}

function euklideanDist(p1, p2) {
    return Math.sqrt(
                  Math.pow(p1["x"]-p2["x"], 2)
                + Math.pow(p1["y"]-p2["y"], 2));
}

function getColor(i, k, transparency) {
    var t = (i+1)*(360/k);
    var color = 'hsla('+t+', 100%, 50%, '+transparency+')';
    return color;
}

function drawBoard(canvas, mouseCoords, radius) {
    var context = canvas.getContext('2d');
    context.canvas.width  = window.innerWidth - 50;
    context.canvas.height = window.innerHeight - 120;
    context.clearRect(0, 0, canvas.width, canvas.height);

    drawPoints(canvas);
    drawRegressionLine(canvas);
}

/** permanently add a point */
function addPoint(event, canvas, mouseCoords, radius) {
    updateBoard();

    points.push({"x": mouseCoords["x"],
                 "y": mouseCoords["y"],
                 "radius": radius});
}

/** Calculate and draw regression line y = a*x + b */
function drawRegressionLine(canvas) {
	if(points.length > 1) {
		var a, b;
		var schwerpunktX = 0;
		var schwerpunktY = 0;
		for(var i = 0; i < points.length; i++) {
			schwerpunktX += points[i]["x"];
			schwerpunktY += points[i]["y"];
		}
		schwerpunktX /= points.length;
		schwerpunktY /= points.length;

		var zaehler = 0;
		var nenner = 0;
		for(var j = 0; j < points.length; j++) {
			console.log(zaehler);
			zaehler += (points[j]["x"]- schwerpunktX) * (points[j]["y"] - schwerpunktY);
			nenner += (points[j]["x"] - schwerpunktX)*(points[j]["x"] - schwerpunktX);
		}
		a = zaehler / nenner;
		b = schwerpunktY - a*schwerpunktX;
		context.strokeStyle = 'blue';
		context.lineWidth=3;
		context.beginPath();
		context.moveTo(0, a*0+b+2);
		context.lineTo(canvas.width, a*canvas.width+b);
		context.stroke();
	}
}

/** draw all permanently added points */
function drawPoints(canvas) {
    for(var i = 0; i < points.length; i++) {
        context.beginPath();
        context.arc(points[i]["x"],
                    points[i]["y"],
                    points[i]["radius"],
                    0, 2 * Math.PI, false);
        context.lineWidth = 1;
        context.strokeStyle = 'black';
        context.fillStyle = 'red';
        context.fill();
        context.stroke();
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

function updateBoard(){
    var canvas = document.getElementById("myCanvas");var canvas = document.getElementById("myCanvas");
    drawBoard(canvas, {"x":0,"y":0}, INITIAL_RADIUS);
}


/** global variables */
var INITIAL_RADIUS = 20;
var POINT_RADIUS = 5;
var points = new Array();
var canvas = document.getElementById("myCanvas");
var context = canvas.getContext("2d");
drawBoard(canvas, {"x":0,"y":0}, INITIAL_RADIUS);
setCursorByID("myCanvas", "crosshair");

/** event listeners */
canvas.addEventListener('mousemove',
    function(evt) {
        var mouseCoords = getMouseCoords(canvas, evt);
        drawBoard(canvas, mouseCoords, INITIAL_RADIUS);
    }, false);

canvas.addEventListener("mousedown",
    function(event) {
        var mouseCoords = getMouseCoords(canvas, event);
        addPoint(event, canvas, mouseCoords, POINT_RADIUS);
    }, false);
