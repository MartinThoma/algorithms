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
    if(document.getElementById("algorithm").value == "k-means") {
        return parseInt(document.getElementById("k").value);
    } else if (document.getElementById("algorithm").value == "k-nearest-neighbor") {
        return maxKnearestNeighborClasses;
    }
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

function getKMeansInfo(k, mouseCoords) {
    var context = canvas.getContext('2d');
    var width = canvas.width;
    var height = canvas.height;

	do {
		// randomly choose cluster centers
		var clusterCenters = new Array(k);
		for (i=0; i<k; i++) {
		    var x = Math.floor(Math.random()*width);
		    var y = Math.floor(Math.random()*height);
		    clusterCenters[i] = {"x": x,"y": y, "points": 0};
		}

		var iteration=0;
		var minChange=true;
		while (iteration < 2000 && minChange) {

			iteration++;
			minChange=false;

			// for each object, check which cluster is nearest
			for (i=0; i<points.length; i++) {
			    var distMin = width+height+10;
			    var clusterMin = 0;
			    for(j=0; j<k; j++) {
			        var dist = euklideanDist(clusterCenters[j], points[i]);
			        if (dist < distMin) {
			            distMin = dist;
			            clusterMin = j
			        }
			    }
			    points[i]["cluster"] = clusterMin;
				clusterCenters[clusterMin]["points"]++;
			}


		    // calculate center of cluster
		    var clusterSum = new Array(k);
		    for (i=0; i<k; i++) {
		        clusterSum[i] = {"x":0, "y":0, "n":0};
		    }
		    for (i=0; i<points.length; i++) {

		        clusterSum[points[i]["cluster"]]["x"] += points[i]["x"];
		        clusterSum[points[i]["cluster"]]["y"] += points[i]["y"];
		        clusterSum[points[i]["cluster"]]["n"] += 1;
		    }
		    for (i=0; i<k; i++) {
		        if (clusterSum[i]["n"] > 0) {
		            var newCenterVar = {"x":clusterSum[i]["x"]/clusterSum[i]["n"],"y":clusterSum[i]["y"]/clusterSum[i]["n"]};
		            if (euklideanDist(clusterCenters[i], newCenterVar) > 2) {
		                minChange = true;
		            }
		            clusterCenters[i] =  {"x":clusterSum[i]["x"]/clusterSum[i]["n"],"y":clusterSum[i]["y"]/clusterSum[i]["n"]};
		        }
		    }
		}
	// check if a cluster center has no points
	} while (points.length >= k && doesCenterWithoutPointsExist(clusterCenters, k));
    document.getElementById("iterations").value = iteration;

    // show where clusters are
    var radiusCenter = 16;
    for (i=0; i < clusterCenters.length; i++){
		context.fillStyle = 'rgb(0,0,0)';
        context.fillRect(clusterCenters[i]["x"]-radiusCenter/2-1,clusterCenters[i]["y"]-radiusCenter/2-1,radiusCenter+2,radiusCenter+2);
		context.fillStyle = getColor(i, 1);
        context.fillRect(clusterCenters[i]["x"]-radiusCenter/2,clusterCenters[i]["y"]-radiusCenter/2,radiusCenter,radiusCenter);
		context.fillStyle = 'rgb(0,0,0)';
		context.font = "bold 16px Arial";
		context.fillText("C", clusterCenters[i]["x"]-6, clusterCenters[i]["y"]+6);
    }

    // for mouse, check which cluster is nearest
    var distMin = width+height+10;
    var clusterMin = 0;
    for(j=0; j<k; j++) {
        var dist = euklideanDist(clusterCenters[j], mouseCoords);
        if (dist < distMin) {
            distMin = dist;
            clusterMin = j
        }
    }

    return {"cluster":clusterMin,
            "radius":distMin};
}

/** Returns a dictionary with a cluster and a radius*/
function getKNearestNeighbor(k, mouseCoords) {
    if (points.length == 0) {
        return {"cluster":0, "radius":INITIAL_RADIUS};
    }

    var Distances = new Array();
    for(var i = 0; i < points.length; i++) {
        points[i]["cluster"] = points[i]["class"];
        var dist = euklideanDist(points[i], mouseCoords);
        Distances.push({"dist":dist, "class":points[i]["class"]});
    }

    numberSort = function (a,b) {
        return a["dist"] - b["dist"];
    };

    Distances.sort(numberSort);
    if (Distances.length < k) {
        /* initialise array to count */
        var classCount = new Array(maxKnearestNeighborClasses);
        for(var i=0;i<maxKnearestNeighborClasses;i++) {
            classCount[i] = 0;
        }

        /* count classes */
        for(var i = 0; i < Distances.length; i++) {
            classCount[Distances[i]["class"]]++;
        }

        /* find maximum */
        maxClass = 0;
        maxClassCount = 0;
        for(var i =0; i <maxKnearestNeighborClasses;i++) {
            if(maxClassCount < classCount[i]) {
                maxClassCount = classCount[i];
                maxClass = i;
            }
        }
        return {"cluster":maxClass, "radius":Distances.slice(-1)[0]["dist"]};
    } else {
        /* initialise array to count */
        var classCount = new Array(maxKnearestNeighborClasses);
        for(var i=0;i<maxKnearestNeighborClasses;i++) {
            classCount[i] = 0;
        }


        for(var i = 0; i < k; i++) {
            classCount[Distances[i]["class"]]++;
        }

        /* find maximum */
        maxClass = 0;
        maxClassCount = 0;
        for(var i =0; i <maxKnearestNeighborClasses;i++) {
            if(maxClassCount < classCount[i]) {
                maxClassCount = classCount[i];
                maxClass = i;
            }
        }
        return {"cluster":maxClass,
                "radius":Distances[k-1]["dist"]};
    }
}

function drawBoard(canvas, mouseCoords, radius) {
    var context = canvas.getContext('2d');
    var k = parseInt(kElement.value);
    context.canvas.width  = window.innerWidth - 50;
    context.canvas.height = window.innerHeight - 120;
    context.clearRect(0, 0, canvas.width, canvas.height);

    if(document.getElementById("algorithm").value == "k-means") {
        var algorithm = getKMeansInfo;
        getKMeansInfo(k, 0, 0);
    } else {
        var algorithm = getKNearestNeighbor;
    }

    if (document.getElementById("voronoi").checked && algorithm != getKMeansInfo) {
        var add = parseInt(document.getElementById("density").value);
        for (x=0; x < canvas.width; x+=add) {
            for (y=0; y < canvas.height; y+=add) {
                var algorithmResult = algorithm(k, {"x":x, "y":y});
                context.fillStyle = getColor(algorithmResult["cluster"],1);
                context.fillRect(x, y, add/2, add/2);
            }
        }
    }

    drawPoints(canvas, k);

    if (document.getElementById("circle").checked && algorithm != getKMeansInfo) {
        var algorithmResult = algorithm(k, mouseCoords);
        context.beginPath();
        context.arc(mouseCoords["x"], mouseCoords["y"], algorithmResult["radius"],
                    0, 2 * Math.PI, false);
        context.fillStyle = getColor(algorithmResult["cluster"], 0.4);
        context.strokeStyle = getColor(algorithmResult["cluster"], 1);
        context.lineWidth = 2;
        context.fill();
        context.stroke();
    }
}

/** permanently add a point */
function addPoint(event, canvas, mouseCoords, radius) {
    updateBoard();

    pointCluster = parseInt(document.getElementById("class").value);

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
function drawPoints(canvas, k) {
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

function updateBoard(){
    var canvas = document.getElementById("myCanvas");var canvas = document.getElementById("myCanvas");
    drawBoard(canvas, {"x":0,"y":0}, INITIAL_RADIUS);
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
updateNumberBgColor();
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
