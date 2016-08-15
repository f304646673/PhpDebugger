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
    $("#run_debug").linkbutton('disable');
    $("#step_over_debug").linkbutton('disable');
    $("#step_in_debug").linkbutton('disable');
    $("#step_out_debug").linkbutton('disable');
    remove_run_line_no();
}

function debugger_status_listen() {
    $("#start_stop_debug").switchbutton({
        checked:true
    });
    $("#run_debug").linkbutton('enable');
    $("#step_over_debug").linkbutton('enable');
    $("#step_in_debug").linkbutton('enable');
    $("#step_out_debug").linkbutton('enable');
    remove_run_line_no();
}

function debugger_status_debug() {
    $("#start_stop_debug").switchbutton({
        checked:true
    });
    $("#run_debug").linkbutton('enable');
    $("#step_over_debug").linkbutton('enable');
    $("#step_in_debug").linkbutton('enable');
    $("#step_out_debug").linkbutton('enable');
    update_cur_source_run_line_no();
}
