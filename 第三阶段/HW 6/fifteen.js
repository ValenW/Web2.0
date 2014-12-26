/**
 * @Author  : ValenW
 * @Link    : https://github.com/ValenW
 * @Email   : ValenW@qq.com
 * @Date    : 2014-12-13 13:03:50
 * @Last Modified by:   ValenW
 * @Last Modified time: 2014-12-26 14:39:53
 */

$(document).ready(function() {
    $("#shufflebutton").click(shuffle);
    wx = wy = 3;
    box = [];
    pieces = $("#puzzlearea > div");
    pieces.each(function(i) {
        this.className = "puzzlepiece";
        this.style.backgroundPosition = "-" + (i % 4)*100 + "px -" + parseInt(i / 4)*100 + "px";
        this.style.top = parseInt(i / 4)*100 + "px";
        this.style.left = (i % 4)*100 + "px";
        this.bId = i;
        this.onclick = pieClick;
        box[i] = i;
    });
});

function shuffle() {
    var t = false;
    var rList = [];
    rList[0] = wy*4 + wx;
    if ($("#windiv")) $("#windiv").remove();
    var diff = prompt('Please enter the random scrambling step (recommended more than 100, 100 by default):', 100);
    if (isNaN(parseInt(diff)) || parseInt(diff) < 0) diff = 100;
    for (var i = 1; i <= diff; i++) {
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
    for (var i = 1; i <= diff; i++) moveP(rList[i], 50);
    update();
}

function moveP(bid, time) {
    if (!time) time = 500;
    $(pieces[box[bid]]).animate({
        top: wy*100 + 'px',
        left: wx*100 + 'px'}, time);
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
                $(pieces[box[i+j*4]]).addClass("movablepiece");
            else if (box[i+j*4] != -1)
                $(pieces[box[i+j*4]]).removeClass("movablepiece");
}

function pieClick() {
    if ($(this).is(".movablepiece")) {
        moveP(this.bId);
        var i = 0;
        for (i = 0; i < 15 && box[i] == i; i++);
        if (i == 15) win();
        else update();
    }
}

function win() {
    $(".puzzlepiece").each(function() {$(this).removeClass("movablepiece")});
    var windiv = $("<div></div>").html(
        "You Win!<br>But you are not the BEST!<br>Becouse...<br>" +
        "<img src='Pml.jpg' width='288' height='480'>").attr("id", "windiv");
    $("#puzzlearea").before(windiv);
}
