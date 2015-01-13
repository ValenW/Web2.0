/**
 * 
 * @Author  : ValenW
 * @Link    : https://github.com/ValenW
 * @Email   : ValenW@qq.com
 * @Date    : 2015-01-12 19:18:30
 * @Last Modified by:   ValenW
 * @Last Modified time: 2015-01-13 09:26:43
 */
$(document).ready(function() {
    $("#bs-example-navbar-collapse-1 li").click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    });
    $("#alert div").hide();
    $(".toRedi").click(redi);
    $(".toHot").click(function() {location.href="http://valenw.sinaapp.com?key=hot"});
    $(".toUp").click(function() {location.href="http://valenw.sinaapp.com?key=up"});
    $(".toDown").click(function() {location.href="http://valenw.sinaapp.com?key=down"});
    $(".toMain").click(function() {location.href="http://valenw.sinaapp.com"});
    $("#loginBtn").click(function() {
        $.ajax({
            type: "POST",
            url: "/login",
            data: "name=" + $("#name").val() + "&password=" + $("#password").val(),
            success: function(msg) {
                if (msg == '1') {
                    $("#alert div").hide();
                    $("#alert div.login.alert-success").show();
                    location.reload();
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
                        location.reload();
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
                location.reload();
            }
        })
    });
    $(".redis").on('click', 'button', vote);
    $('#cmt').keydown(function(event) {
        if(event.which == 13) {
            var com = $(this).val()
            if (com.length <= 0) $(this).attr("placeholder", "你还什么都没说呦~")
            else if ($('button[data-target="#logoutModal"]')[0]) {
                $.ajax({
                    type: "POST",
                    url: location.href,
                    data: "comment=" + com,
                    success: function(msg) {
                        if (msg == "1") {
                            location.reload();
                        }
                    }
                });
            } else {
                $("#alert div").hide();
                $("#alert div.login.alert-info").show();
                $("#loginModal").modal()
            }
        }
    });
});

function vote() {
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
    event.stopPropagation();
}

function redi() {
    if ($('button[data-target="#logoutModal"]')[0]) {
        location.href="/redi"
    } else {
        $("#alert div").hide();
        $("#alert div.login.alert-info").show();
        $("#loginModal").modal()
    }
}
