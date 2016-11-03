/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function get_breakpoint_list() {
    $('#breakpoint_add_dialog_tabs').tabs("select", "Breakpoint");
    $('#breakpoint_datagrid').datagrid('loadData',[]);
    $.post("do", {"action":"breakpoint_list", "param":""},
        function(data){
            if (data.ret == 0) {
                return;
            }
            $.each(data, function(n,value){
                var del_html = "<button onclick='remove_breakpoint(\""+ value.itemid + "\");' style='width:100%;heigth:100%;'>delete</button>";
                
                var expression_de = value.expression;
                if (value.expression != undefined) {
                    expression_de = base64_decode(value.expression);
                }
                
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
                        expression:expression_de,
                        temporary:value.temporary,
                        hit_count:value.hit_count,
                        hit_value:value.hit_value,
                        hit_condition:value.hit_condition,
                        operation:del_html,
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
    } else if (tab_id == "breakpoint_add_dialog_tabs_exception") {
        add_breakpoint_exception_by_dialog();
    } else if (tab_id == "breakpoint_add_dialog_tabs_condition") {
        add_breakpoint_condition_by_dialog();
    }
}

function add_breakpoint_line_by_dialog() {
    var filename = $("#breakpoint_add_dialog_line_filename").textbox("getText");
    var lineno = $("#breakpoint_add_dialog_line_lineno").textbox("getText");
    if (0 == filename.length || 0 == lineno.length) {
        alert("filename or lineno is empty!");
        return;
    }

    add_breakpoint_line(filename, lineno);
}

function add_breakpoint_line(filename, lineno) {
    var param = '{"filename":"' + base64_encode(filename) + '", "lineno":"' + lineno + '", "type":"line"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"add_breakpoint", "param":param_en},
        function(data){
            if (data.ret == 1) {
                add_breakpoint_dlg_close();
            }
            update_cur_selected_tab_info();
            update_cur_open_file_breakpoint_display();
            console.log(data);
    }, "json");
}

function add_breakpoint_call_by_dialog() {
    var function_name = $("#breakpoint_add_dialog_call_function").textbox("getText");
    if (0 == function_name.length) {
        alert("function is empty!")
        return;
    }
    add_breakpoint_call(function_name);
}

function add_breakpoint_call(function_name) {
    var param = '{"function":"' + function_name + '", "type":"call"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"add_breakpoint", "param":param_en},
        function(data){
            if (data.ret == 1) {
                add_breakpoint_dlg_close();
            }
            update_cur_selected_tab_info();
            console.log(data);
    }, "json");
    
}

function add_breakpoint_return_by_dialog() {
    var function_name = $("#breakpoint_add_dialog_return_function").textbox("getText");
    if (0 == function_name.length) {
        alert("function is empty!");
        return;
    }
    add_breakpoint_return(function_name);
}

function add_breakpoint_return(function_name) {
    var param = '{"function":"' + function_name + '", "type":"return"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"add_breakpoint", "param":param_en},
        function(data){
            if (data.ret == 1) {
                add_breakpoint_dlg_close();
            }
            update_cur_selected_tab_info();
            update_cur_open_file_breakpoint_display();
            console.log(data);
    }, "json");
}

function add_breakpoint_exception_by_dialog() {
    var exception_name = $("#breakpoint_add_dialog_exception_exception_name").textbox("getText");
    if (0 == exception_name.length) {
        alert("exception is empty!");
        return;
    }
    add_breakpoint_exception(exception_name);
}

function add_breakpoint_exception(exception_name) {
    var param = '{"exception":"' + exception_name + '", "type":"exception"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"add_breakpoint", "param":param_en},
        function(data){
            if (data.ret == 1) {
                add_breakpoint_dlg_close();
            }
            update_cur_selected_tab_info();
            update_cur_open_file_breakpoint_display();
            console.log(data);
    }, "json");
    
}

function add_breakpoint_condition_by_dialog() {
    var filename = $("#breakpoint_add_dialog_condition_filename").textbox("getText");
    var lineno = $("#breakpoint_add_dialog_condition_lineno").textbox("getText");
    var expression = $("#breakpoint_add_dialog_condition_expression").textbox("getText");
    if (0 == filename.length || 0 == lineno.length || 0 == expression.length) {
        alert("filename\lineno\expression is empty!");
        return;
    }
    add_breakpoint_condition(filename, lineno, expression);
}

function add_breakpoint_condition(filename, lineno, expression) {
    var param = '{"filename":"' + base64_encode(filename) + '", "lineno":"' + lineno + '", "expression":"' + base64_encode(expression) +  '", "type":"conditional"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"add_breakpoint", "param":param_en},
        function(data){
            if (data.ret == 1) {
                add_breakpoint_dlg_close();
            }
            update_cur_selected_tab_info();
            update_cur_open_file_breakpoint_display();
            console.log(data);
    }, "json"); 
}

var breakpoint_input_ids = [
        "breakpoint_add_dialog_line_filename",
        "breakpoint_add_dialog_line_lineno",
        "breakpoint_add_dialog_call_function",
        "breakpoint_add_dialog_return_function",
        "breakpoint_add_dialog_exception_exception_name",
        "breakpoint_add_dialog_condition_filename",
        "breakpoint_add_dialog_condition_lineno",
        "breakpoint_add_dialog_condition_expression"];
        
function add_breakpoint_dlg_open() {
    var i = breakpoint_input_ids.length;
    while (i--) {
        $("#" +breakpoint_input_ids[i]).textbox("clear");
    }
    $('#breakpoint_add_dialog').dialog('open');
}

function add_breakpoint_dlg_close() {
    $('#breakpoint_add_dialog').dialog('close');
}

function set_line_breakpoint(path,lineno) {
    var param = '{"filename":"' + path + '", "lineno":"' + lineno + '", "type":"line"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"add_breakpoint", "param":param_en},
        function(data){
            update_cur_selected_tab_info();
            update_cur_open_file_breakpoint_display();
            console.log(data);
        }, "json");
}

function remove_breakpoint(id) {
    var param = '{"itemid":"' + id + '"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"remove_breakpoint", "param":param_en},
        function(data){
          //alert(data.name);
          update_cur_selected_tab_info();
          update_cur_open_file_breakpoint_display();
          console.log(data);
        }, "json");
}

function remove_line_breakpoint(path, lineno) {
    var param = '{"filename":"' + path + '", "lineno":"' + lineno + '", "type":"line"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"remove_breakpoint", "param":param_en},
        function(data){
          //alert(data.name)
          update_cur_selected_tab_info();
          update_cur_open_file_breakpoint_display();
          console.log(data);
        }, "json");
}

function add_breakpoint_call_by_menu() {
    add_breakpoint_dlg_open();
    $('#breakpoint_add_dialog_tabs').tabs('select', 'Call');
    $("#breakpoint_add_dialog_call_function").textbox("setText", selected_text);
}

function add_breakpoint_return_by_menu() {
    add_breakpoint_dlg_open();
    $('#breakpoint_add_dialog_tabs').tabs('select', 'Return');
    $("#breakpoint_add_dialog_return_function").textbox("setText", selected_text);
}

function add_breakpoint_exception_by_menu() {
    add_breakpoint_dlg_open();
    $('#breakpoint_add_dialog_tabs').tabs('select', 'Exception');
    $("#breakpoint_add_dialog_exception_exception_name").textbox("setText", selected_text);
}

function add_line_breakpoint_by_menu() {
    add_breakpoint_dlg_open();
    $('#breakpoint_add_dialog_tabs').tabs('select', 'Line');
    $("#breakpoint_add_dialog_line_filename").textbox("setText", base64_decode(rigth_click_file_path));
    $("#breakpoint_add_dialog_line_lineno").textbox("setText", rigth_click_line_no);
}

function add_conditional_breakpoint_by_menu() {
    add_breakpoint_dlg_open();
    $('#breakpoint_add_dialog_tabs').tabs('select', 'Condition');
    $("#breakpoint_add_dialog_condition_filename").textbox("setText", base64_decode(rigth_click_file_path));
    $("#breakpoint_add_dialog_condition_lineno").textbox("setText", rigth_click_line_no);
}