/**
 * 
 * @Author  : ValenW
 * @Link    : https://github.com/ValenW
 * @Email   : ValenW@qq.com
 * @Date    : 2015-01-08 12:49:27
 * @Last Modified by:   ValenW
 * @Last Modified time: 2015-01-11 09:45:20
 */
$(document).ready(function() {
    $(".alert-warning").each(function() {$(this).hide();});
    $('#datetimepicker6').datetimepicker({ language: 'zh' });
    $("#submit").click(function() {
        $(".alert-warning").each(function() {$(this).hide();});
        if      ($("#name").val() == '')                $(".nameAlert").show();
        else if ($("#datetimepicker6").val() == '')     $(".timeAlert").show();
        else if ($("#content").val() == '')             $(".contentAlert").show();
        else {
            $.ajax({
                type: "POST",
                url: "/redi",
                data: "name=" + $("#name").val() + "&time=" + $("#datetimepicker6").val() + "&content=" + $("#content").val(),
                success: function(msg) {
                    if (msg == '1') { window.location.href="/" }
                }
            });
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
});
