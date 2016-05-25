/** Optics stuff *************************************************************/
function Point(x, y) {
    this.x = x;
    this.y = y;
    this.cd = null;
    this.rd = null;
    this.processed = false;
}

Point.prototype.distance = function(point) {
    var dx = (point.x - this.x);
    var dy = (point.y - this.y);
    return sqrt(dx*dx + dy*dy);
}

function Cluster(points) {
    this.points = points;
}

Cluster.prototype.centroid = function() {
    var n = 0;
    var sum_x = 0.0;
    var sum_y = 0.0;
    for (var i = this.points.length - 1; i >= 0; i--) {
        n += 1;
        sum_x = this.points[i].x;
        sum_y = this.points[i].y;
    }
    return Point(sum_x / n, sum_y/n);
}

Cluster.prototype.region = function() {
    var centroid = this.centroid();
    var radius = 0.0;
    for (var i = this.points.length - 1; i >= 0; i--) {
        radius = Math.max(radius, this.points[i].distance(centroid));
    }
    return [centroid, radius];
}

function Optics(points, max_radius, min_cluster_size) {
    this.points = points;
    this.max_radius = max_radius;
    this.min_cluster_size = min_cluster_size;
}

Optics.prototype._setup = function() {
    for (var i = this.points.length - 1; i >= 0; i--) {
        this.points[i].rd = null;
        this.processed = False;
    }
    this.unprocessed = this.points.slice();
    this.ordered = [];
}

Optics.prototype._core_distance = function(point, neighbors){
    if (point.cd !== null){
        return point.cd;
    }

    if (neighbors.length >= this.min_cluster_size - 1) {
        sorted_neighbors = sorted([n.distance(point) for n in neighbors]);
        point.cd = sorted_neighbors[self.min_cluster_size - 2];
        return point.cd;
    }
}


/** Drawing stuff*************************************************************/
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

function getNrOfClusters() {
    return 1;
}

function getColor(i, transparency) {
    return getColorGeneral(i, getNrOfClusters(), transparency);
}

function getColorGeneral(i, k, transparency) {
    var t = (i+1)*(360/k);
    var color = 'hsla('+t+', 100%, 50%, '+transparency+')';
    return color;
}

function doesCenterWithoutPointsExist(clusterCenters, k) {
    for (i=0; i<k; i++) {
        if (clusterCenters[i]["points"] == 0) {
            return true;
        }
    }
    return false;
}


function drawBoard(canvas, mouseCoords, radius) {
    var context = canvas.getContext('2d');
    //var k = parseInt(kElement.value);
    context.canvas.width  = window.innerWidth - 50;
    context.canvas.height = window.innerHeight - 120;
    context.clearRect(0, 0, canvas.width, canvas.height);

    drawPoints(canvas);
}

/** permanently add a point */
function addPoint(event, canvas, mouseCoords, radius) {
    update();

    pointCluster = 1;

    if (pointCluster > maxKnearestNeighborClasses) {
        maxKnearestNeighborClasses = pointCluster;
    }

    points.push({"x": mouseCoords["x"],
                 "y": mouseCoords["y"],
                 "radius": radius,
                 "cluster": pointCluster,
                 "class": pointCluster});
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
        context.fillStyle = getColor(points[i]["cluster"], getNrOfClusters(), 0.9);
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

function update(){
    var canvas = document.getElementById("myCanvas");
    drawBoard(canvas, {"x":0,"y":0}, INITIAL_RADIUS);
    drawReachabilityPlot();
}

function drawReachabilityPlot(){
    var c = document.getElementById("reachabilityPlot");
    var context = c.getContext("2d");

    for(var i = 0; i < points.length; i++) {
        context.beginPath();
        context.arc(points[i]["x"],
                    points[i]["y"],
                    points[i]["radius"],
                    0, 2 * Math.PI, false);
        context.lineWidth = 1;
        context.strokeStyle = 'black';
        context.fillStyle = getColor(points[i]["cluster"], getNrOfClusters(), 0.9);
        context.fill();
        context.stroke();
    }
    ctx.rect(20, 0, 25, 100);
    ctx.stroke();
}

function updateNumberBgColor(){
    var domEl = document.getElementById("class");
    if(parseInt(domEl.value) > getNrOfClusters()+1) {
        domEl.value = getNrOfClusters()+1;
    }
    domEl.style.backgroundColor = getColorGeneral(parseInt(domEl.value), Math.max(parseInt(domEl.value), getNrOfClusters()), 0.5);
}

/** global variables */
var maxKnearestNeighborClasses = 1;
var INITIAL_RADIUS = 20;
var POINT_RADIUS = 5;
var points = new Array();
var canvas = document.getElementById("myCanvas");
var kElement = document.getElementById("k");
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
