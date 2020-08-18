//           h h    m m    s s    ms
var time = [[0,0], [0,0], [0,0], [0,0]];
var isRunning = false;

function tick(){
    time[3][1]++;

    if (time[3][1]==10){
		time[3][1] = 0;
		time[3][0]++;
	}
    if (time[3][0]==10){
		time[3][0] = 0;
		time[2][1]++;
	}
    if (time[2][1]==10){
		time[2][1]=0;
		time[2][0]++;
	}
    if (time[2][0]==6){
		time[2][0]=0;
		time[1][1]++;
	}
    if (time[1][1]==10){
		time[1][1]=0;
		time[1][0]++;
	}
    if (time[1][0]==6){
		time[1][0]=0;
		time[0][0]++;
	}
}

function printTime(h, m, s, ms){
	var hT = document.getElementById("hh");
	var mT = document.getElementById("mm");
	var sT = document.getElementById("ss");
	var milli = document.getElementById("milli");
	hT.innerHTML =h[0] + '' + h[1];
	mT.innerHTML =m[0] + '' + m[1];
	sT.innerHTML =s[0] + '' + s[1];
	milli.innerHTML =ms[0] + '' + ms[1];
	document.title=h[0] + '' + h[1] + ':'
				  +m[0] + '' + m[1] + ':'
   				  +s[0] + '' + s[1];
}

function refreshTime(){
	var h = time[0];
	var m = time[1];
	var s = time[2];
	var ms = time[3];

	if (isRunning) {
		tick();
		printTime(h, m, s, ms);
		setTimeout(refreshTime, 10);
	}
}

function toggle(){
	isRunning = !isRunning;
	refreshTime();
	if (isRunning) {
		document.getElementById('start').value = "Stop";
	} else {
		document.getElementById('start').value = "Start";
	}
}

function clearTime(){
	time = [[0,0], [0,0], [0,0], [0,0]];
	printTime(time[0], time[1], time[2], time[3]);
}

document.addEventListener('keydown',
            function(evt) {
				if (evt.keyCode == 32) {
               toggle();
				}
            }, false);
