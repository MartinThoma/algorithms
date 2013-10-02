'use strict';

var video = document.querySelector("#vid");
var canvas = document.querySelector('#canvas');
var context = canvas.getContext('2d');
var localMediaStream = null;

var onCameraFail = function (e) {
    console.log('Camera did not work.', e);
};

/**
 * Apply a filter to grayscale image. (Covolution)
 * @param {ImageData} imgData 
 * @param {matrix of numbers} matrix
 * @return {undefined}
 */
function applyMatrix(imgData, matrix) {
    var imgDataNormal = context.getImageData(0, 0, 
				context.canvas.width, context.canvas.height);
	var sep = (matrix.length-1)/2

    for (var i = 0; i < imgData.width * imgData.height * 4; i += 4) {
		var tmp = i/4;
		var x = tmp % imgData.width;
		var y = (tmp - x)/imgData.width;
		if (x <= sep || y <= sep) {
			// to small to apply filter
			continue;
		}

		var tmpPxl = 0;
		for (var ym=0; ym < matrix.length; ym++) {
			for (var xm=0; xm < matrix[0].length; xm++) {
				var tmpYPos = y+(-matrix.length+ym);
				var tmpXPos = x+(-matrix[0].length+xm);
				var tmpPos = 4*(imgData.width*tmpYPos+tmpXPos);
				tmpPxl += matrix[ym][xm]*imgDataNormal.data[tmpPos];
			}
		}
		imgData.data[4*(imgData.width*y+x)+0] = tmpPxl; // r
		imgData.data[4*(imgData.width*y+x)+1] = tmpPxl; // g
		imgData.data[4*(imgData.width*y+x)+2] = tmpPxl; // b
	}
	context.putImageData(imgData, 0, 0);
}

function harrisCornerDetector(imgData) {
    var imgDataNormal = context.getImageData(0, 0, 
				context.canvas.width, context.canvas.height);
    var n = 3;
    for (var x=n-1; x<context.canvas.width - n; x++) {
        for (var y=n-1; y<context.canvas.height - n; y++) {
            var a = 0;
            var b = 0;
            var c = 0;
            var d = 0;
            // TODO
        }
    }
	context.putImageData(imgData, 0, 0);
}

setInterval(function snapshot() {
    if (localMediaStream) {
        context.drawImage(video, 0, 0);
		var width = 640;
		var height = 480;
        var imgDataNormal = context.getImageData(0, 0, width, height);
        var imgData = context.createImageData(width, height);

        for (var i = 0; i < imgData.width * imgData.height * 4; i += 4) {
            var r = (imgDataNormal.data[i + 0] * .393) + (imgDataNormal.data[i + 1] * .769) + (imgDataNormal.data[i + 2] * .189);
            var g = (imgDataNormal.data[i + 0] * .349) + (imgDataNormal.data[i + 1] * .686) + (imgDataNormal.data[i + 2] * .168);
            var b = (imgDataNormal.data[i + 0] * .272) + (imgDataNormal.data[i + 1] * .534) + (imgDataNormal.data[i + 2] * .131);
            if (r > 255) {
                r = 255;
            }
            if (g > 255) {
                g = 255;
            }
            if (b > 255) {
                b = 255;
            }
            imgData.data[i + 0] = r;
            imgData.data[i + 1] = g;
            imgData.data[i + 2] = b;
            imgData.data[i + 3] = imgDataNormal.data[i + 3];

			// Grayscale
			var brightness = (3*r+4*g+b)>>>3;
			imgData.data[i] = brightness;
			imgData.data[i+1] = brightness;
			imgData.data[i+2] = brightness;
        }

		var filter = document.getElementById('filter').value;

        if(filter != 'harris') {
		    var matrix;
		    if (filter === 'prewitt-x') {
			    matrix = [[-1,0,1],[-1,0,1],[-1,0,1]];
		    } else if (filter == 'prewitt-y') {
			    matrix = [[-1,-1,-1],[0,0,0],[1,1,1]];
		    } else if (filter == 'prewitt-y-switched') {
			    matrix = [[1,1,1],[0,0,0],[-1,-1,-1]];
		    } else if (filter == 'sobel-x') {
			    matrix = [[1,0,-1],[2,0,-2],[1,0,-1]];
		    } else if (filter == 'sobel-y') {
			    matrix = [[1,2,1],[0,0,0],[-1,-2,-1]];
		    } else if (filter == 'kirsh-x') {
			    matrix = [[5,-3,-3],[5,0,-3],[5,-3,-3]];
		    } else if (filter == 'kirsh-y') {
			    matrix = [[5,5,5],[-3,0,-3],[-3,-3,-3]];
		    } else if (filter == 'laplace') {
			    matrix = [[0,1,0],[1,-4,1],[0,1,0]];
		    } else if (filter == 'canny-edge-detector') {
			    matrix = [[2.0/159,4.0/159,5.0/159,4.0/159,2.0/159],[4.0/159,9.0/159,12.0/159,9.0/159,4.0/159],[5.0/159,12.0/159,15.0/159,12.0/159,5.0/159],[4.0/159,9.0/159,12.0/159,9.0/159,4.0/159],[2.0/159,4.0/159,5.0/159,4.0/159,2.0/159]];
		    } else if (filter == 'roberts-1') {
			    matrix = [[-1,0],[0,1]];
		    } else if (filter == 'roberts-2') {
			    matrix = [[0,-1],[1,0]];
		    } else {
			    matrix = [[1]];
		    }

            context.putImageData(imgData, 0, 0);

		    applyMatrix(imgData, matrix);
        } else {
            context.putImageData(imgData, 0, 0);
            applyMatrix(imgData);
        }
    }
}, 500);

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
window.URL = window.URL || window.webkitURL;
navigator.getUserMedia({video:true}, function (stream) {
    video.src = window.URL.createObjectURL(stream);
    localMediaStream = stream;
}, onCameraFail);
console.log(localMediaStream);
