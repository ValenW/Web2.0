/* 
* @Author: ValenW
* @Date:   2014-12-11 10:32:49
* @Last Modified by:   ValenW
* @Last Modified time: 2014-12-12 20:45:36
*/

var timer = null;

$(document).ready(function(){
    $("#b1").click(function() {
        if (timer === null) {
            timer = setInterval(timeDe, 500);
        } else {
            clearInterval(timer);
            timer = null;
        }
    });

    $("#b2").click(function() {
        var text = $("textarea").val();
        text = text.toUpperCase();
        text = text.split('.').join('-izzle.');
        $("textarea").val(text);
    });

    $("#b3").click(function() {
        var text = $("textarea").val();
        text = text.split(/\b +\b/);
        for (var i = 0; i < text.length; i++) {
            text[i] = text[i].split(/\b-+\b/);
            for (var j = 0; j < text[i].length; j++)
                if (text[i][j].length > 4) text[i][j] = "Malkovich";
            text[i] = text[i].join("-");
        }
        text = text.join(" ");
        $("textarea").val(text);
    });

    // $("#b4").click(function() {
    //     var text = $("textarea").val();
    //     var re = /^[^aeiouAEIOU]*(?=[aeiouAEIOU])/;
    //     text = text.trim().split(" ");
    //     alert(text);
    //     for (var i = 0; i < text.length; i++) {
    //         if (isNaN(parseInt(text[i]))) {
    //             if (text[i].match(re) == [""]) {
    //                 text[i] = (text[i] + "-ay");
    //             } else {
    //                 var head = text[i].match(re);
    //                 text[i] = text[i].replace(head, "") + head + "-ay";
    //             }
    //         }
    //     }
    //     text = text.join(" ");
    //     $("textarea").val(text);
    // });

    $("#cb1").click(function() {
        if ($("#cb1").is(":checked")) {
            $('textarea').addClass("bling");
            $("body").addClass('bac1');
        } else {
            $('textarea').removeClass("bling");
            $('body').removeClass('bac1');
        }
    });
});

function timeDe() {
    var oldSize = $("textarea").css("font-size");
    size = parseFloat(oldSize, 10);
    unit = oldSize.slice(-2);
    if (unit != "pt") {
        size = parseInt(size/4*3);
        unit = "pt";
    }
    size += 10;
    $("textarea").css("font-size", size + unit);
}
