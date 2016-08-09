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

function set_line_breakpoint(path,lineno) {
    var param = '{"filename":"' + path + '", "lineno":"' + lineno + '", "type":"line"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"add_breakpoint", "param":param_en},
        function(data){
          console.log(data);
        }, "json");
}

function remove_line_breakpoint(path, lineno) {
    var param = '{"filename":"' + path + '", "lineno":"' + lineno + '", "type":"line"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"remove_breakpoint", "param":param_en},
        function(data){
          //alert(data.name);
          console.log(data);
        }, "json");
}

function excute_console_cmd(cmd) {
    var param = '{"cmd":"' + cmd + '"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"query", "param":param_en},
        function(data){
            append_debug_view(cmd);
            append_debug_view(data);
            console.log(data);
        }, "");
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

function getStack() {
    $.post("do", {"action":"stack_get", "param":""},
        function(data){
            if (data.ret == 1) {
                rebuild_statck_info(data.data);
            }
            console.log(data);
        }, "json");
}

function getBreakpoint() {
    $('#breakpoint_datagrid').datagrid('loadData',[]);
    $.post("do", {"action":"breakpoint_list", "param":""},
        function(data){
            $.each(data, function(n,value){
                $('#breakpoint_datagrid').datagrid('insertRow',{
                    index: n,	// index start with 0
                    row: {
                        id: value.id,
                        type: value.type,
                        filename: value.filename,
                        lineno: value.lineno,
                        state: value.state,
                        function: value.function,
                        exception:value.exception,
                        expression:value.expression,
                        temporary:value.temporary,
                        hit_count:value.hit_count,
                        hit_value:value.hit_value,
                        hit_condition:value.hit_condition,
                    }
                });
                console.log(value)
            });
            console.log(data);
        }, "json");
}

function add_breakpoint() {
    var tab = $('#breakpoint_add_dialog_tabs').tabs('getSelected');
    var tab_id = tab.panel('options').id;
    if (tab_id == "breakpoint_add_dialog_tabs_line") {
        add_breakpoint_line_by_dialog();
    } else if (tab_id == "breakpoint_add_dialog_tabs_return") {
        add_breakpoint_return_by_dialog();
    } else if (tab_id == "breakpoint_add_dialog_tabs_call") {
        add_breakpoint_call_by_dialog();
    }
}

function add_breakpoint_line_by_dialog() {
    var filename = $("#breakpoint_add_dialog_line_filename").textbox("getText");
    var lineno = $("#breakpoint_add_dialog_line_lineno").textbox("getText");
    if (0 == filename.length || 0 == lineno.length) {
        alert("filename or lineno is empty!");
        return;
    }

    var param = '{"filename":"' + base64_encode(filename) + '", "lineno":"' + lineno + '", "type":"line"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"add_breakpoint", "param":param_en},
        function(data){
            if (data.ret == 1) {
                $('#breakpoint_add_dialog').dialog('close');
            }
            console.log(data);
    }, "json");
}

function add_breakpoint_call_by_dialog() {
    var function_name = $("#breakpoint_add_dialog_call_function").textbox("getText");
    if (0 == function_name.length) {
        alert("function is empty!")
        return;
    }

    var param = '{"function":"' + function_name + '", "type":"call"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"add_breakpoint", "param":param_en},
        function(data){
            if (data.ret == 1) {
                $('#breakpoint_add_dialog').dialog('close');
            }
            console.log(data);
    }, "json");
}

function add_breakpoint_return_by_dialog() {
    var function_name = $("#breakpoint_add_dialog_return_function").textbox("getText");
    if (0 == function_name.length) {
        alert("function is empty!");
        return;
    }

    var param = '{"function":"' + function_name + '", "type":"return"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"add_breakpoint", "param":param_en},
        function(data){
            if (data.ret == 1) {
                $('#breakpoint_add_dialog').dialog('close');
            }
            console.log(data);
    }, "json");
}