/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function add_variables_watch_dlg_open() {
    $('#add_variables_watch_dlg').dialog('open').dialog('center').dialog('setTitle','Add a Variable Watch');
    $('#add_variables_watch_add_dlg_fm').form('clear');  
}

function add_variables_watch_dlg_close() {
    $('#add_variables_watch_add_dlg_fm').form('clear');
    $('#add_variables_watch_dlg').dialog('close');
}

function add_variable_watch_request() {
    var variable_name_de = $('#add_variables_watch_add_dlg_fm div .textbox .textbox-value').val();
    var variable_name_en = base64_encode(variable_name_de);
    $.get("variables_watch", {"action":"add", "param":variable_name_en},
        function(data){
            getVariablesWatch();
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

function getVariablesWatch() {
    $.get("variables_watch", {"action":"get_list", "param":""},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                for (var index = 0; index < data.list.length; index++) {
                    var item = data.list[index];
                    if (check_variable_watch_tab_exist(item.id)) {
                        continue;
                    }
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
                    $("#variables_watch_tabs").find('#' + item.id).attr("name",item.name);
                    get_variable_last_content(item.id, item.name);
                }
            }
        },
        "json");
}

function make_variable_watch_textarea_id(id) {
    return "variable_watch_area_"+id;
}

function make_variable_tab_panel_data(tab_id, data) {
    return "<textarea id='" + make_variable_watch_textarea_id(tab_id) + "' style='width:100%;height:100%'>" + data + "</textarea>";
}

function get_variable_last_content(tab_id,variable_name) {
    $.get("variables_watch", {"action":"get_variable", "param":variable_name},
        function(data){
            console.log(data);
            var tab_t = $('#variables_watch_tabs').find('#' + tab_id);
            var html_text = make_variable_tab_panel_data(tab_id,data);
            $("#variables_watch_tabs").tabs('update',{tab:tab_t, options:{content:html_text}});
            var area_id = make_variable_watch_textarea_id(tab_id);
            var scrollTop = $("#" + area_id )[0].scrollHeight;  
            $("#" + area_id ).scrollTop(scrollTop); 
        });
}

function get_variable_last_content_by_index(tab_index) {
    var tab_id = $("#variables_watch_tabs").tabs('getTab',tab_index).panel('options').id;
    var variable_name_en = $("#variables_watch_tabs").tabs('getTab',tab_index).attr("name");
    get_variable_last_content(tab_id, variable_name_en);
}

function remove_variable_watch(tab_index) {
    var variable_id = $("#variables_watch_tabs").tabs('getTab',tab_index).panel('options').id; //base64encode
    $.get("variables_watch", {"action":"remove", "param":variable_id},
      function(data){
            console.log(data);
            if (data.ret == 1) {
                
            }
            });
    return true;
}