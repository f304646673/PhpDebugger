/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function start_debug() {
    $.post("do", {"action":"start_debug", "param":""},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                update_debugger_status();
            } else {
                console.log(data);
            }
        },
    "json");
}

function stop_debug() {
    $.post("do", {"action":"stop_debug", "param":""},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                update_debugger_status();
            } else {
                console.log(data);
            }
        },
    "json");
}

function step_over() {
    $.post("do", {"action":"step_over", "param":""},
        function(data){
            console.log(data);
            update_cur_source_run_line_no();
            update_cur_selected_tab_info();
        }, "json");
}

function step_in() {
    $.post("do", {"action":"step_in", "param":""},
        function(data){
            console.log(data);
            update_cur_source_run_line_no();
            update_cur_selected_tab_info();
        }, "json");
}

function step_out() {
    $.post("do", {"action":"step_out", "param":""},
        function(data){
            console.log(data);
            update_cur_source_run_line_no();
            update_cur_selected_tab_info();
        }, "json");
}

function run() {
    $.post("do", {"action":"run", "param":""},
        function(data){
            console.log(data);
            update_cur_source_run_line_no();
            update_cur_selected_tab_info();
        }, "json");
}

function get_stack_list() {
    $.post("do", {"action":"stack_get", "param":""},
        function(data){
            if (data.ret == 1) {
                rebuild_statck_info(data.data);
            }
            console.log(data);
        }, "json");
}
