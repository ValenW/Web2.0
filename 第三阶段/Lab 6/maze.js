/**
 * 
 * @Author  : ValenW
 * @Link    : https://github.com/ValenW
 * @Email   : ValenW@qq.com
 * @Date    : 2014-12-13 09:36:57
 * @Last Modified by:   ValenW
 * @Last Modified time: 2014-12-19 12:14:34
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

function $c(classname) {
    return document.getElementsByClassName(classname);
}

window.onload = function() {
    $("start").onmouseover = start;
    $("start").onclick = restart;
    $("maze").onmouseleave = fail;
}

var wined = 0;

function start() {
    if (wined) return;
    for (var i = 0; i < $c("boundary").length; i++)
        $c("boundary")[i].onmouseover = fail;
    $("end").onmouseover = win;
    $("status").innerHTML = "The game started.";
}

function fail() {
    if (wined === 1) return;
    wined = -1;
    for (var i = 0; i < $c("boundary").length; i++) {
        var oldClass = $c("boundary")[i].className;
        if (oldClass.indexOf("youlose") >= 0 | oldClass.indexOf("example") >= 0) continue;
        $c("boundary")[i].className = oldClass + " youlose";
    }
    $("status").innerHTML = "You Lost! Click the S to restart.";
    $("status").style.color = "red"
}

function win() {
    if (wined !== -1) {
        wined = 1;
        $("status").innerHTML = "You Win! Click the S to restart!";
        $("status").style.color = "orange"
    }
}

function restart() {
    wined = 0;
    var bos = $c("boundary youlose");
    while (bos.length) bos[0].className = "boundary";
    $("status").innerHTML = "The game started.";
    $("status").style.color = "black";
}
