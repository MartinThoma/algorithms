'use strict';

var canvas = document.getElementById('myCanvas');
var context = canvas.getContext('2d');
var POINT_RADIUS = 5;
var INITIAL_RADIUS = 20;
var points = [[]];
var start = {"x": 0, "y": 0, "src": "emoticon_smile.png"};
var target = {"x": canvas.width-1, "y": canvas.height-1, "src": "flag_red.png"}

function updateBoard(){
    var canvas = document.getElementById("myCanvas");var canvas = document.getElementById("myCanvas");
    drawBoard(canvas, {"x":0,"y":0}, INITIAL_RADIUS);
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

/** permanently add a point */
function addPoint(event, canvas, mouseCoords, radius) {
    var currentPolygon = parseInt(document.getElementById("polygonNumber").value);
    points[currentPolygon].push({"x": mouseCoords["x"],
                 "y": mouseCoords["y"],
                 "radius": radius});

    if (document.getElementById("polygonNumber").max == currentPolygon) {
        document.getElementById("polygonNumber").max = currentPolygon + 1;
        points.push([]);
    }
    updateBoard();
}

function getColor(i, k, transparency) {
    var t = (i+1)*(360/k);
    var color = 'hsla('+t+', 100%, 50%, '+transparency+')';
    return color;
}

/** draw all permanently added points */
function drawPolygons(canvas) {
    for(var cluster = 0; cluster < points.length; cluster++) {
        context.fillStyle = getColor(cluster, document.getElementById("polygonNumber").max, 0.9);
        for (var i=0; i < points[cluster].length; i++) {
            context.beginPath();
            context.arc(points[cluster][i]["x"], 
                        points[cluster][i]["y"], 
                        points[cluster][i]["radius"], 
                        0, 2 * Math.PI, false);
            context.lineWidth = 1;
            context.strokeStyle = 'black';
            context.fillStyle = getColor(points[cluster][i]["polygon"], document.getElementById("polygonNumber").max, 0.9);
            context.fill();
            context.stroke();
        }

        if (points[cluster].length < 3) {
            continue;
        }

        context.beginPath();

        context.moveTo(points[cluster][0]["x"], points[cluster][0]["y"]);
        for (var i=1; i < points[cluster].length; i++) {
            context.lineTo(points[cluster][i]["x"], points[cluster][i]["y"]);
        }
        context.closePath();
        context.fill();
    }
}

function drawBoard(canvas, mouseCoords, radius) {
    var context = canvas.getContext('2d');
    context.canvas.width  = window.innerWidth - 50;
    context.canvas.height = window.innerHeight - 120;
    context.clearRect(0, 0, canvas.width, canvas.height);

    drawPolygons(canvas);

    // Algorithmus
    polygonzerlegung(canvas);

    // Draw Start
    var imageObj = new Image();
    imageObj.onload = function() {
        context.drawImage(imageObj, start["x"], start["y"]);
    };
    imageObj.src = start["src"];

    // Draw End
    var imageObjT = new Image();
    imageObjT.onload = function() {
        context.drawImage(imageObjT, target["x"], target["y"]);
    };
    imageObjT.src = target["src"];
}

function polygonzerlegung(canvas) {
    var context = canvas.getContext('2d');
    for(var cluster = 0; cluster < points.length; cluster++) {
        context.fillStyle = getColor(0, 1, 0.9);
        for (var i=0; i < points[cluster].length; i++) {
            context.beginPath();
            context.moveTo(0, points[cluster][i]["y"]);
            context.lineTo(points[cluster][i]["x"], points[cluster][i]["y"]);
            context.stroke();
        }
    }
}

canvas.addEventListener("mousedown", 
    function(event) {
        var mouseCoords = getMouseCoords(canvas, event);
        if (document.getElementById("nextClickType").value == "obstacle") {
            addPoint(event, canvas, mouseCoords, POINT_RADIUS);
        } else if (document.getElementById("nextClickType").value == "start") {
            start["x"] = mouseCoords["x"];
            start["y"] = mouseCoords["y"];
            updateBoard();
        } else if (document.getElementById("nextClickType").value == "target") {
            target["x"] = mouseCoords["x"];
            target["y"] = mouseCoords["y"];
            updateBoard();
        }
    }, false);
