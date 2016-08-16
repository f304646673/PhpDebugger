/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var get_status_timer;

$(document).ready(function(){
    get_status_timer = $.timer(1000, function(){
        update_debugger_status();
    });
     
    update_debugger_status();
});

function update_debugger_status() {
     $.post("do", {"action":"get_debugger_status", "param":""},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                change_debugger_status(data.status);
            }
            else {
                change_debugger_status(-1);
            }
        },
    "json");
}

var cur_status = -1;
//0 Init 1 Listen 2 debug
function change_debugger_status(status) {
    if (cur_status == status)
        return;
    
    switch (status) {
        case -1:
        case 3:
            debugger_status_init();
            break;
        case 0:
            debugger_status_listen();
            break;
        case 2:
            debugger_status_debug();
            break;
    }
    cur_status = status;
}

function debugger_status_init() {
    $("#start_stop_debug").switchbutton({
        checked:false
    });
    dis_en_able_debug_buttons_status(false);
    
    remove_run_line_no();
}

function debugger_status_listen() {
    $("#start_stop_debug").switchbutton({
        checked:true
    });
    dis_en_able_debug_buttons_status(true);
    
    remove_run_line_no();    
}

function debugger_status_debug() {
    $("#start_stop_debug").switchbutton({
        checked:true
    });
    dis_en_able_debug_buttons_status(true);
    
    update_cur_source_run_line_no();
}

function dis_en_able_debug_buttons_status(enable) {
    dis_en_able_linkbuttons(enable);
    dis_en_able_tools_menu_items(enable);
}

function dis_en_able_linkbuttons(enable) {
    var linkbuttons_names = [
        "run_debug",
        "step_over_debug",
        "step_in_debug",
        "step_out_debug"
    ];
    
    var cmd = enable ? 'enable' : 'disable';
    
    for (var index = 0;index < linkbuttons_names.length;index++) {
         $("#"+linkbuttons_names[index]).linkbutton(cmd);
    }
}

function dis_en_able_tools_menu_items(enable) {
    var tools_memu_content_list = [
        "tools_memu_content_run", 
        "tools_memu_content_step_over",
        "tools_memu_content_step_in",
        "tools_memu_content_step_out"];
    
    var cmd = enable ? 'enableItem' : 'disableItem';
    
    for (var index = 0;index < tools_memu_content_list.length;index++) {
        var itemEl = $('#'+tools_memu_content_list[index])[0];
        $("#tools_memu_content").menu(cmd, itemEl);
    }
}

