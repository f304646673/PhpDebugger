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
                        get_variables_list()
                    }break;
                case "Stack":{
                        get_stack_list()
                    }break;
                case "Breakpoint":{
                        get_breakpoint_list()
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
    
    $("#botton_tab").tabs({
        onSelect:function(title,index) {
            update_cur_selected_tab_info();
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

function openFiles(name,path,id){
    var exists = $("#files_tab").find('#' + id);
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

function update_cur_selected_tab_info() {
    var tab = $('#botton_tab').tabs('getSelected');
    switch (tab.panel('options').title) {
        case "Variables": {
                get_variables_list();
            }break;
        case "Stack":{
                get_stack_list();
            }break;
        case "Breakpoint":{
                get_breakpoint_list();
            }break;
        case 'Files Watch':{
                get_files_watch();
            }break;   
        case 'Files Watch':{
                get_variables_watch();
            }break; 
    }
}
