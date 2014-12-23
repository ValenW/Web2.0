/**
 * @Author  : ValenW
 * @Link    : https://github.com/ValenW
 * @Email   : ValenW@qq.com
 * @Date    : 2014-12-13 13:03:50
 * @Last Modified by:   ValenW
 * @Last Modified time: 2014-12-20 14:11:02
 */

window.onload = function() {
    document.getElementById("shufflebutton").onclick = shuffle;
    wx = wy = 3;
    box = [];
    pieces = document.querySelectorAll("#puzzlearea > div");
    for (var i = 0; i < pieces.length; i++) {
        pieces[i].className = "puzzlepiece";
        pieces[i].style.backgroundPosition = "-" + (i % 4)*100 + "px -" + parseInt(i / 4)*100 + "px";
        pieces[i].style.top = parseInt(i / 4)*100 + "px";
        pieces[i].style.left = (i % 4)*100 + "px";
        pieces[i].bId = i;
        pieces[i].onclick = pieClick;
        box[i] = i;
    }
}

function shuffle() {
    var oldR = 3, t = false;
    var rList = [];
    rList[0] = wy*4 + wx;
    for (var i = 1; i <= 100; i++) {
        var r = parseInt(Math.random()*2);
        if (t) r += 2;
        var x = rList[i-1]%4, y = parseInt(rList[i-1]/4);
        if (r == 0)
                y - 1 < 0 ? y++ : y--;
        else if (r == 1)
                y + 1 > 3 ? y-- : y++;
        else if (r == 2)
                x + 1 > 3 ? x-- : x++;
        else if (r == 3)
                x - 1 < 0 ? x++ : x--;
        rList[i] = y*4 + x;
        t = !t;
    }
    for (var i = 1; i <= 100; i++) moveP(rList[i]);
    update();
}

function moveP(bid) {
    pieces[box[bid]].style.top = wy*100 + 'px';
    pieces[box[bid]].style.left = wx*100 + 'px';
    pieces[box[bid]].bId = wy*4 + wx;
    box[wy*4 + wx] = box[bid];
    wx = bid % 4;
    wy = parseInt(bid / 4);
    box[bid] = -1;
}

function update() {
    for(var i = 0; i < 4; i++)
        for (var j = 0; j < 4; j++)
            if ((Math.abs(i - wx) + Math.abs(j - wy)) == 1)
                pieces[box[i+j*4]].className = "puzzlepiece movablepiece";
            else if (box[i+j*4] != -1)
                pieces[box[i+j*4]].className = "puzzlepiece";
}

function pieClick() {
    if (this.className == "puzzlepiece movablepiece") {
        moveP(this.bId);
        var i = 0;
        for (i = 0; i < 15 && box[i] == i; i++);
        if (i == 15) win();
        else update();
    }
}

function win() {
    alert("You Win!");
    for (i = 0; i < 15; i++) pieces[i].className = "puzzlepiece";
}
