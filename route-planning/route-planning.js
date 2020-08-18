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
        context.fillStyle = getColor(cluster, parseInt(document.getElementById("polygonNumber").max)+4, 0.9);
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

    // Voronoi
    if (document.getElementById("voronoi").checked) {
        var add = parseInt(document.getElementById("voronoiAdd").value);
        for (var x=0; x < canvas.width; x+=add) {
            for (var y=0; y < canvas.height; y+=add) {
                var i = getNearestBorder(x, y);
                //console.log(i);
                context.fillStyle = getColor(i,points.length+4, 0.9);
                context.fillRect(x, y, add/2, add/2);
            }
        }
    }

    drawPolygons(canvas);

    // Algorithmus
    if (document.getElementById("polygonSegmentation").checked) {
        polygonzerlegung(canvas);
    }

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

function getEuclideanDistance(a, b) {
    return Math.sqrt((a["x"]-b["x"])*(a["x"]-b["x"])+(a["y"]-b["y"])*(a["y"]-b["y"]));
}

function getDistToLine(line, p) {
    var px = line[1]["x"]-line[0]["x"];
    var py = line[1]["y"]-line[0]["y"];

    var tmp = px*px + py*py

    var u =  ((p["x"] - line[0]["x"]) * px + (p["y"] - line[0]["y"]) * py) / tmp;

    if (u > 1) {
        u = 1;
    } else if(u < 0) {
        u = 0;
    }

    var x = line[0]["x"] + u * px;
    var y = line[0]["y"] + u * py;

    var dx = x - p["x"];
    var dy = y - p["y"];

    var dist = Math.sqrt(dx*dx + dy*dy);
    return dist;
}

function getDistToPolygon(polygon, p) {
    var minDist = Math.max(canvas.width, canvas.height);
    for(var i=0; i+1<polygon.length;i++) {
        var tmpDist = getDistToLine([polygon[i], polygon[i+1]], p);
        if (tmpDist < minDist) {
            minDist = tmpDist;
        }
    }

    var tmpDist = getDistToLine([polygon[0], polygon[polygon.length-1]], p);
    if (tmpDist < minDist) {
        minDist = tmpDist;
    }

    return minDist;
}

function getNearestBorder(x, y) {
    var d = [];

    for(var cluster = 0; cluster < document.getElementById("polygonNumber").max; cluster++) {
        d.push(getDistToPolygon(points[cluster], {"x":x, "y":y}));
    }

    // distance to "down border"
    d.push(canvas.height - y);

    // distance to "up border"
    d.push(y);

    // distance to "left border"
    d.push(x);

    // distance to "right border"
    d.push(canvas.width - x);

    var i = 0, m = d[0], mI = 0;
    while(++i < d.length) {
        if(d[i] < m) {
            mI = i;
            m = d[i];
        }
    }

    return mI;
}

function polygonzerlegung(canvas) {
    var context = canvas.getContext('2d');
    for(var cluster = 0; cluster < points.length; cluster++) {
        context.fillStyle = getColor(0, 1, 0.9);
        for (var i=0; i < points[cluster].length; i++) {
            context.beginPath();
            context.moveTo(points[cluster][i]["x"], 0);
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
