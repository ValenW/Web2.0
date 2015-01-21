/**
 * 
 * @Author  : ValenW
 * @Link    : https://github.com/ValenW
 * @Email   : ValenW@qq.com
 * @Date    : 2015-01-06 20:04:37
 * @Last Modified by:   ValenW
 * @Last Modified time: 2015-01-15 13:24:43
 */
$(document).ready(function() {
    $('#scroll').hide();
    $('#scroll').on('click', function() {$("html,body").animate({ scrollTop:0}, 800);});
    $("#bs-example-navbar-collapse-1 li").click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    });
    $("#alert div").hide();
    $(".toRedi").click(redi);
    $(".toHot").click(function() {window.location.href="?key=hot"});
    $(".toUp").click(function() {window.location.href="?key=up"});
    $(".toDown").click(function() {window.location.href="?key=down"});
    $(".toMain").click(function() {window.location.href="/"});
    $("#loginBtn").click(function() {
        $.ajax({
            type: "POST",
            url: "/login",
            data: "name=" + $("#name").val() + "&password=" + $("#password").val(),
            success: function(msg) {
                if (msg == '1') {
                    $("#alert div").hide();
                    $("#alert div.login.alert-success").show();
                    window.location.href="/"
                } else if (msg == '-1') {
                    $("#alert div").hide();
                    $("#alert div.login.alert-danger").show();
                } else {
                    $("#alert div").hide();
                    $("#alert div.login.alert-warning").show();
                }
            }
        });
    });
    $("#signupBtn").click(function() {
        var re = /^[\w\u4E00-\u9FA5\uF900-\uFA2D]{2,15}$/
        if (re.test($("#name").val()) && re.test($("#password").val())) {
            $.ajax({
                type: "POST",
                url: "/signup",
                data: "name=" + $("#name").val() + "&password=" + $("#password").val(),
                success: function(msg) {
                    if (msg == '1') {
                        $("#alert div").hide();
                        $("#alert div.signup.alert-success").show();
                        window.location.href="/"
                    } else if (msg == '-1') {
                        $("#alert div").hide();
                        $("#alert div.signup.alert-danger").show();
                    } else {
                        $("#alert div").hide();
                        $("#alert div.signup.alert-info").show();
                    }
                }
            });
        } else {
            $("#alert div").hide();
            $("#alert div.signup.alert-warning").show();
        }
    });
    $("#logoutBtn").click(function() {
        $.ajax({
            type: "GET",
            url: "/logout",
            success: function() {
                window.location.href="/"
            }
        })
    });
    $(".redis").on('click', 'button', vote);
    $(".redis").on('click', '.redi', coms);
    $("#load").click(function() {
        tload()
        $("#load").text("正在加载...")
        $(window).on('scroll', tload)
    });
    $(window).scroll(function() {
        if($(window).scrollTop() >= 400) $('#scroll').fadeIn(400);
        else $('#scroll').fadeOut(200);
    });
});

function vote(e) {
    if ($('button[data-target="#logoutModal"]')[0]) {
        var rid = parseInt($(this).attr("id").substr(1))
        if ($(this).hasClass('btn-info')) {
            $(this).removeClass('btn-info')
            var oldv = $(this).html().split('<br>')
            var v = parseInt(oldv[0])
            v = v - 1 + '<br>' + oldv[1]
            $(this).html(v)
            $.ajax({
                type: "POST",
                url: "/vote",
                data: "id=" + rid + "&o=r",
                success: function(msg) {

                }
            });
        } else {
            $(this).addClass('btn-info')
            var oldv = $(this).html()
            oldv = oldv.split('<br>')
            var v = parseInt(oldv[0])
            v = v + 1 + '<br>' + oldv[1]
            $(this).html(v)
            $.ajax({
                type: "POST",
                url: "/vote",
                data: "id=" + rid + "&o=p",
                success: function(msg) {

                }
            });
            if ($($($(this).siblings()[0])).hasClass('btn-info')) {
                $($(this).siblings()[0]).removeClass('btn-info')
                var oldv = $($(this).siblings()[0]).html()
                oldv = oldv.split('<br>')
                var v = parseInt(oldv[0])
                v = v - 1 + '<br>' + oldv[1]
                $($(this).siblings()[0]).html(v)
            }
        }
        var v1 = parseInt($(this).html().split('<br>')[0])
        var v2 = parseInt($($(this).siblings()[0]).html().split('<br>')[0])
        if (v1 >= v2) {
            $(this).addClass('voted')
            $($(this).siblings()[0]).removeClass('voted')
        } else {
            $(this).removeClass('voted')
            $($(this).siblings()[0]).addClass('voted')
        }
    } else {
        $("#alert div").hide();
        $("#alert div.login.alert-info").show();
        $("#loginModal").modal()
    }
    var e = e ? e : window.event;
    if (window.event) {
        e.cancelBubble = true;
        e.stopPropagation();
    } else {
        e.stopPropagation();
    }
}

function tload() {
    if ($(document).height() - $(window).height() - $(document).scrollTop() <= 20) {
        var stype = window.location.search.split('=')
        var formId = ""
        if (stype == '') {
            stype = "id"
            fromId = $(".redi:last-child .up").attr("id").substr(1)
        } else {
            stype = stype[1]
            var upn = parseInt($(".redi:last-child .up").html().split('<br>')[0])
            var don = parseInt($(".redi:last-child .down").html().split('<br>')[0])
            if (stype == 'hot') fromId = upn + don;
            else if (stype == 'up') fromId = upn;
            else fromId = don;
        }
        $.ajax({
            url: '/load/' + stype + '/' + fromId,
            dataType: 'json',
            type: 'GET'
        })
        .done(function(msg) {
            var l = msg.length
            for (var i = 0; i < l; i++) {
                var add = 
                "<div class=\"redi container\">\
                  <div class=\"row\">\
                    <div class=\"col btn-group-vertical\">\
                      <button type=\"button\" class=\"up hvr-bounce-to-top btn" + msg[i][8] + "\" id=\"r" + msg[i][0] + "\">" + msg[i][4] + "<br>神预言</button>\
                      <button type=\"button\" class=\"down hvr-bounce-to-bottom btn" + msg[i][9] + "\" id=\"r-" + msg[i][0] + "\">" + msg[i][5] + "<br>什么鬼</button>\
                    </div>\
                    <div class=\"col-md-2 col-xs-8\">\
                      <span class=\"redier\">" + msg[i][1] + "</span> 预言说<br><span class=\"time\">" + msg[i][7] + "天后<br>(" + msg[i][2] + ")</span>\
                    </div>\
                    <p class=\"redititle col-md-8 col-xs-12\">" + msg[i][3] + "</p>\
                  </div>\
                </div>"
                $(".redis").append($(add))
            }
            if (l == 0) {
                $("#load").addClass('loadend')
                $("#load").html("(*/ω＼*) 矮油, 人家被你看光了 <br>快点这里去发预言补偿人家! (˘•ω•˘)")
                $(window).off('scroll', tload)
                $("#load").off('click')
                $("#load").on('click', redi);
            }
            console.log("success");
        })
    }
}

function redi() {
    if ($('button[data-target="#logoutModal"]')[0]) {
        window.location.href="/redi"
    } else {
        $("#alert div").hide();
        $("#alert div.login.alert-info").show();
        $("#loginModal").modal()
    }
}

function coms() {
    var rediId = parseInt($($(this).find('button')[0]).attr('id').substr(1));
    window.location.href="http://valenw.sinaapp.com/com/" + rediId;
}