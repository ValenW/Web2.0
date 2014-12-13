/* 
* @Author: ValenW
* @Date:   2014-12-12 16:24:40
* @Last Modified by:   ValenW
* @Last Modified time: 2014-12-13 17:17:13
*/

function $(id) {
    return document.getElementById(id);
}

function $t(tag) {
    return document.getElementsByTagName(tag);
}

function $n(name) {
    return document.getElementsByName(name);
}

window.onload = function() {
    var sizes = $n("size");
    for (var i = 0; i < sizes.length; i++) sizes[i].onclick = size;

    $("start").onclick = start;
    $("stop").onclick = stop;

    $("anim").onchange = anim;

    $n("Turbo")[0].onclick = speedC;
}

var played = [""];
var speed = 300;
var animTh = 0;
var timer = null;

function size() {
    var spd = this.value;
    if (spd === "Small") {
        $("displayarea").style.fontSize = "7pt";
    } else if (spd === "Medium") {
        $("displayarea").style.fontSize = "12pt";
    } else {
        $("displayarea").style.fontSize = "24pt";
    }
}

function start() {
    if (timer) return;
    timer = setInterval(play, speed);
}

function stop() {
    if (timer === null) return;
    clearInterval(timer);
    timer = null;
}

function speedC() {
    speed = (speed === 300 ? 150 : 300);
    if (timer != null) {
        clearInterval(timer);
        timer = setInterval(play, speed);
    }
}

function anim() {
    played = ANIMATIONS[this.value].split("=====\n");
    animTh = 0;
    play();
}

function play() {
    $("displayarea").value = played[animTh];
    animTh = (animTh >= played.length - 1 ? 0 : animTh + 1);
}
