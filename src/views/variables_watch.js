/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

$(document).ready(function(){
    $("#variables_watch_tabs").tabs({
        onBeforeClose:function(title,index) {
            return remove_variable_watch(index);
        }
    });
    
    $("#variables_watch_tabs").tabs({
        onSelect:function(title,index) {
            get_variable_last_content_by_index(index);
        }
    });
    
});

function add_variables_watch_dlg_open() {
    $('#add_variables_watch_dlg').dialog('open').dialog('center').dialog('setTitle','Add Variable Watch');
    $('#add_variables_watch_add_dlg_variable_name').textbox('clear');  
}

function add_variables_watch_dlg_close() {
    $('#add_variables_watch_add_dlg_variable_name').textbox('clear');
    $('#add_variables_watch_dlg').dialog('close');
}

function add_variable_watch_by_dialg() {
    var variable_name_de = $('#add_variables_watch_add_dlg_variable_name').textbox("getText");
    add_variable_watch_request(variable_name_de);
}

function add_variable_watch_request(variable_name_de) {
    var variable_name_en = base64_encode(variable_name_de);
    $.get("variables_watch", {"action":"add", "param":variable_name_en},
        function(data){
            get_variables_watch();
            console.log(data);
        }, 
        "json");
    
    $('#add_variables_watch_dlg').dialog('close')
}

function check_variable_watch_tab_exist(id) {
    var items = $('#variables_watch_tabs').find('#' + id);
    if (items.length>0) {
        return true;
    }
    return false;
}

function get_variables_watch() {
    $('#breakpoint_add_dialog_tabs').tabs("select", "Variable Watch");
    $.get("variables_watch", {"action":"get_list", "param":""},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                for (var index = 0; index < data.list.length; index++) {
                    var item = data.list[index];
                    if (!check_variable_watch_tab_exist(item.id)) {
                        $("#variables_watch_tabs").tabs('add',{
                        id:item.id,
                        title:item.name,
                        content:"",
                        closable:true,
                        tools:[{
                            iconCls:'icon-mini-refresh',
                            handler:function(){
                                get_variable_last_content(item.id,item.name);
                            }
                            }]
                        });
                    }
                    $("#variables_watch_tabs").find('#' + item.id).attr("name",item.name);
                    get_variable_last_content(item.id, item.name);
                }
            }
        },
        "json");
}

function make_variable_watch_content_id(id) {
    return "variable_watch_show_" + id;
}

function make_variable_watch_content_pre_id(id) {
    return make_variable_watch_content_id(id) + "_pre";
}

function make_variable_watch_content_cur_id(id) {
    return make_variable_watch_content_id(id) + "_cur";
}

function update_variable_tab_panel_data(tab_id, data) {
    if (null == data) {
        return;
    }
        
    update_variable_content_outside(tab_id);
    update_variable_content_pre_cur(tab_id);
    
    //$('#' + make_variable_watch_content_cur_id(tab_id)).emtpy();
    var options = {
        collapsed: $('#collapsed').is(':checked'),
        withQuotes: $('#with-quotes').is(':checked')
    };
    
    if (null != data.cur) {
        $('#' + make_variable_watch_content_cur_id(tab_id)).jsonViewer(data.cur.value, options);
    }
    
    if (null != data.pre) {
        $('#' + make_variable_watch_content_pre_id(tab_id)).jsonViewer(data.pre.value, options);
    }
    
    return 
}

function update_variable_content_outside(id) {
    if ($("#"+make_variable_watch_content_id(id)).length > 0)
        return;
    var tab_t = $('#variables_watch_tabs').find('#' + id);
    if (tab_t.length != 0) {
        var html_text = "<div id='" + make_variable_watch_content_id(id) + "' style='width:100%;height:100%'></div>";
        $("#variables_watch_tabs").tabs('update',{tab:tab_t, options:{content:html_text}});
    }
}

function update_variable_content_pre_cur(id) {
    if ($('#' + make_variable_watch_content_pre_id(id)).length == 0) {
        var pre = $('<pre/>').attr("id", make_variable_watch_content_pre_id(id));
        var div = $('<div/>').attr("style","display:inline-block;width:50%;height:100%;");
        div.append(pre);
        $("#"+make_variable_watch_content_id(id)).append(div);
    }
    if ($('#' + make_variable_watch_content_cur_id(id)).length == 0) {
        var cur = $('<pre/>').attr("id", make_variable_watch_content_cur_id(id));
        var div = $('<div/>').attr("style","display:inline-block;width:50%;height:100%;");
        div.append(cur);
        $("#"+make_variable_watch_content_id(id)).append(div);
    }     
}

function get_variable_last_content(tab_id,variable_name) {
    var variable_name_en = base64_encode(variable_name);
    $.post("do", {"action":"get_variable_watch", "param":variable_name_en},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                update_variable_tab_panel_data(data.id, data.data)
            } 
        }, "json");
}

function get_variable_last_content_by_index(tab_index) {
    var tab_id = $("#variables_watch_tabs").tabs('getTab',tab_index).panel('options').id;
    var variable_name_en = $("#variables_watch_tabs").tabs('getTab',tab_index).attr("name");
    get_variable_last_content(tab_id, variable_name_en);
}

function remove_variable_watch(tab_index) {
    var variable_name_de = $("#variables_watch_tabs").tabs('getTab',tab_index).panel('options').title; //base64encode
    var variable_name_en = base64_encode(variable_name_de);
    $.get("variables_watch", {"action":"remove", "param":variable_name_en},
      function(data){
            console.log(data);
            if (data.ret == 1) {
            }
            });
    return true;
}

function add_variable_watch_by_menu(){
    add_variables_watch_dlg_open();
    $("#add_variables_watch_add_dlg_variable_name").textbox("setText", selected_text);
}

function add_variable_watch_in_dialog_from_menucontent() {
    var node = $('#variables_treegrid').treegrid('getSelected');
    if (node && node.type != ""){
        add_variables_watch_dlg_open();
        $('#add_variables_watch_add_dlg_variable_name').textbox("setText", node.name);
    }
}