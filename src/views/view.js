/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var get_status_timer;

$(document).ready(function(){
    setTimeout(function () { 
        floder_reload();
    }, 100);


    $('#console_dlg_cmd').textbox('textbox').bind('keydown', function(e){
        if (e.keyCode == 13){	// when press ENTER key, accept the inputed value.
            excute_console_cmd($(this).val());
            $('#console_dlg_cmd').textbox('setValue', '');
        }
    });

    $('#console_dlg_div').layout();


    $('#breakpoint_add_line_form').form('submit', {
        url:"do",
        onSubmit: function(param){

        }
    });

    $('#breakpoint_add_call_form').form('submit', {
        url:"do",
        onSubmit: function(param){

        }
    });

    $('#breakpoint_add_return_form').form('submit', {
        url:"do",
        onSubmit: function(param){

        }
    });
    
    $('#botton_tab').tabs({
        onSelect: function(title,index){
            switch (title) {
                case "Variables": {
                        getVariables()
                    }break;
                case "Stack":{
                        getStack()
                    }break;
                case "Breakpoint":{
                        getBreakpoint()
                    }break;
            }
        }
    });
    
    get_status_timer = $.timer(1000, function(){
        update_debugger_status();
    });
    
     $('#start_stop_debug').switchbutton({
        onChange: function(checked){
            if (checked) {
                start_debug();
            }
            else {
                stop_debug();
            }
            console.log(checked);
        }
    });
        
    update_debugger_status();
});

function modify_highlight(id) {
    var $numbering;
    //var ul_id = id + "_pre-numbering";
    $('#'+id).each(function(){
        var lines = $(this).text().split('\n').length;
        $numbering = $('<ul/>').addClass('pre-numbering');
        //$numbering.attr("id", ul_id);
        $(this).append($numbering);
        $('#' + id + " code").addClass('has-numbering')
        for(i=0;i<=lines;i++){
            $numbering.append($('<li/>').text(i+1));
        }
    });

    $numbering.on('click', 'li', function(e) {
        var $target = $(e.currentTarget),
            isactive = $target.hasClass('active'),
            isrun_active = $target.hasClass('run_active'),
            isrun = $target.hasClass('run'),
            lineno = $target.index() + 1;

        file_path = $(this).parents('pre')[0].attributes.path.value;
        if (isrun_active) {
            $target.removeClass('run_active');
            $target.addClass('run');
            remove_line_breakpoint(file_path, lineno);
        }
        else if (isrun) {
            $target.removeClass('run');
            $target.addClass('run_active');
            set_line_breakpoint(file_path, lineno)
        }
        else if(isactive) {
            $target.removeClass('active');
            remove_line_breakpoint(file_path, lineno);
        }
        else {
            $target.addClass('active');
            set_line_breakpoint(file_path, lineno)
        }
        console.log(lineno);
    });
}  

function update_files(id,path) {
    $.post("getfile", {"path":path},
        function(data){
            $("#" + id).empty();                                            // 删除原来代码
            $("<code class='" + data.type + " hljs' style='witdh:100%;height:100%;'><code/>").appendTo($("#" + id));      // 新增代码块
            var context = base64_decode(data.data);

            $("#" + id + " ."+ data.type).html(highlight_code(data.type, context).value);     // 设置代码块内容
            modify_highlight(id);
            update_file_line_breakpoint(id,path);
            update_cur_run_line_no();
        }, "json");
}

function get_cur_file_path() {
    
}

function openFiles(name,path,id){
    var exists = $('#' + id);
    if (exists.length> 0) {
        $("#files_tab pre").each(function(index){
             if ($(this).get(0).id == id) {
                var tab = $('#files_tab').tabs('getSelected');
                var sel_index = $('#files_tab').tabs('getTabIndex',tab);
                if (sel_index != index) {
                    $('#files_tab').tabs('select',index);
                }
                else {
                }
             }
        });
       return;
    }
    $('#files_tab').tabs('add',{
        title: name,
        content: '<pre id="'+  id + '" path="' + base64_encode(path) + '">'+ '</pre>',
        closable: true
    });
    update_files(id,path);
}
 
function remove_run_line_no() {
    var pres = $("#files_tab pre");
    for(var i=0; i < pres.length; i++) {
        var file_id = pres[i].id;
        var sel_pre_query = "#" + file_id;
        var $before_target_run = $(sel_pre_query + " ul li.run:first");
        if (0 != $before_target_run.size()) {
            $before_target_run.removeClass("run");
        }

        var $before_target_run_active = $(sel_pre_query + " ul li.run_active:first");
        if (0 != $before_target_run_active.size()) {
            $before_target_run_active.removeClass("run_active").addClass('active');
        }
    }
}
 
function set_current_run_line_no(file_id, run_line) {
    var sel_pre_query = "#" + file_id;
    var $before_target_run = $(sel_pre_query + " ul li.run:first");
    if (0 != $before_target_run.size()) {
        $before_target_run.removeClass("run");
    }

    var $before_target_run_active = $(sel_pre_query + " ul li.run_active:first");
    if (0 != $before_target_run_active.size()) {
        $before_target_run_active.removeClass("run_active").addClass('active');
    }

    var index = run_line - 1;
    var query_line = sel_pre_query + " ul li:eq(" + index + ")";
    var $target = $(query_line);
    if (0 == $target.size()) {
        return;
    }
    if ($target.hasClass("run_active")) {
        return;
    }
    else if ($target.hasClass("run")) {
        return;
    }
    else if ($target.hasClass("active")) {
        $target.removeClass("active").addClass("run_active");
    }
    else {
        $target.addClass("run");
    }
}

function append_debug_view(text) {
    var new_text = $('#console_dlg_view').textbox("getText") + "\n" +  text;
    $('#console_dlg_view').textbox("setValue",new_text);
}

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

function update_cur_source_run_line_no() {
    $.post("do", {"action":"get_cur_stack_info", "param":""},
        function(data){
            if (data.ret == 1) {
                openFiles(data["data"]["filename_last"], data["data"]["filename"], data["data"]["file_id"]);
                update_file_line_breakpoint(data["data"]["file_id"], data["data"]["filename"])
                set_current_run_line_no(data["data"]["file_id"], data["data"]["lineno"]);
            }
            console.log(data);
        }, "json");
}

function update_cur_run_line_no() {
    $.post("do", {"action":"get_cur_stack_info", "param":""},
        function(data){
            if (data.ret == 1) {
                set_current_run_line_no(data["data"]["file_id"], data["data"]["lineno"]);
            }
            console.log(data);
        }, "json");
}

function update_file_line_breakpoint(fileid,filename) {
    var param = '{"filename":"' + filename + '"}';
    var param_en = base64_encode(param);
    $.post("do", {"action":"get_file_line_breakpoint_lineno", "param":param_en},
        function(data){
            if (data.ret == 1) {
                for (index = 0; index < data.breakpoint_list_lineno.length; index++) {
                    var lineno_index = data.breakpoint_list_lineno[index] - 1;
                    $('#'+fileid + " ul li:eq("+lineno_index+")").addClass('active');
                }
            }
            console.log(data);
        }, "json");
}

function rebuild_statck_info(data) {
    $('#stack_datagrid').datagrid('loadData',[]);
    
    $('#stack_datagrid').datagrid({
        onClickRow: function(index,rowData){
            openFiles(rowData["filename_last"],rowData["filename"],rowData["file_id"]);
        }
    });
    
    $.each(data,function(n,value) {
        $('#stack_datagrid').datagrid('insertRow',{
            index: parseInt(value.frame),	// index start with 0
            row: {
                frame: value.frame,
                filename: value.filename,
                lineno: value.lineno,
                function: value.function,
                file_id: value.file_id,
                filename_last:value.filename_last
            }
        });
    });
}

function getVariables() {
    $('#variables_treegrid').treegrid('loadData', []);
    RegisteVariablesContextMenu();
    RegistVariablesDbClick();
    
    $.post("do", {"action":"get_variables", "param":""},
        function(data){
            if (data.ret == 1) {
                $('#variables_treegrid').treegrid('loadData', data.data);
            }
    }, "json");
}

function RegistVariablesDbClick() {
    $('#variables_treegrid').treegrid({onDblClickCell:function(field,row){
            if (row){
                if (field == "value" && row.type !="") {
                    show_variable_in_dialog(row.name, row.value);
                }
            }
        }
    });
}

function RegisteVariablesContextMenu() {                 
    $('#variables_treegrid').treegrid({onContextMenu:function(e, row){
            if (row){
                e.preventDefault();
                $(this).treegrid('select', row.id);
                $('#variables_treegrid_contextmenu').menu('show',{
                    left: e.pageX,
                    top: e.pageY
                });                
            }
        }
    });
}

function collapse(){
    var node = $('#variables_treegrid').treegrid('getSelected');
    if (node){
        $('#variables_treegrid').treegrid('collapse', node.id);
    }
}

function expand(){
    var node = $('#variables_treegrid').treegrid('getSelected');
    if (node){
        $('#variables_treegrid').treegrid('expand', node.id);
    }
}

function show_variable_in_dialog_from_menucontent() {
    var node = $('#variables_treegrid').treegrid('getSelected');
    if (node){
        show_variable_in_dialog(node.name, node.value);
    }
}

function show_variable_in_dialog(name, data) {
    $('#variables_show_json-renderer').empty();
    var options = {
        collapsed: $('#collapsed').is(':checked'),
        withQuotes: $('#with-quotes').is(':checked')
    };
    eval("var theJsonValue = "+ data); 
    $('#variables_show_json-renderer').jsonViewer(theJsonValue, options);
    $('#variables_show').dialog('open').dialog('center').dialog('setTitle',name);
}

function update_cur_selected_tab_info() {
    var tab = $('#botton_tab').tabs('getSelected');
    switch (tab.panel('options').title) {
        case "Variables": {
                getVariables();
            }break;
        case "Stack":{
                getStack();
            }break;
        case "Breakpoint":{
                getBreakpoint();
            }break;
    }
}