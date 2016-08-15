/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var console_cmd_list = [];
var console_cmd_list_index = 0;

$(document).ready(function(){
    $('#console_dlg_cmd').textbox('textbox').bind('keydown', function(e){
        if (e.keyCode == 13){	// when press ENTER key, accept the inputed value.
            var cmd = $(this).val();
            console_cmd_list.push(cmd);  
            console_cmd_list_index = console_cmd_list.length;
            excute_console_cmd(cmd);
            $('#console_dlg_cmd').textbox('setValue', '');
        } else if (e.keyCode == 38){
            if (console_cmd_list_index > 0) {
                console_cmd_list_index = console_cmd_list_index -1;
                var cmd = console_cmd_list[console_cmd_list_index];
                $('#console_dlg_cmd').textbox('setValue', cmd);
            }
        } else if (e.keyCode == 40){
            if (console_cmd_list_index < console_cmd_list.length - 1) {
                console_cmd_list_index = console_cmd_list_index +1;
                var cmd = console_cmd_list[console_cmd_list_index];
                $('#console_dlg_cmd').textbox('setValue', cmd);
            }
        }
    });

    $('#console_dlg_div').layout();
});

function excute_console_cmd(cmd) {
    var param = '{"cmd":"' + cmd + '"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"query", "param":param_en},
        function(data){
            append_debug_view(cmd);
            append_debug_view(eval(data));
            console.log(data);
        }, "");
}

function append_debug_view(text) {
    var new_text = $('#console_dlg_view')[0].value + "\n" +  text;
    $('#console_dlg_view')[0].value = new_text;
    var scrollTop = $("#console_dlg_view")[0].scrollHeight ;  
    $("#console_dlg_view").scrollTop(scrollTop); 
}