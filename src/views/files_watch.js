/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

$(document).ready(function(){
    $("#files_watch_tabs").tabs({
        onBeforeClose:function(title,index) {
            return remove_file_watch(index);
        }
    });
    
    $("#files_watch_tabs").tabs({
        onSelect:function(title,index) {
            get_file_last_content_by_index(index);
        }
    });
    
});

function add_files_watch_dlg_open() {
    $('#add_files_watch_dlg').dialog('open').dialog('center').dialog('setTitle','Add a File Watch');
    $('#add_files_watch_add_dlg_file_name').textbox('clear');
}

function add_files_watch_dlg_close() {
    $('#add_files_watch_add_dlg_file_name').textbox('clear');
    $('#add_files_watch_dlg').dialog('open').dialog('close');
}

function add_file_watch_request() {
    var path = $('#add_files_watch_add_dlg_file_name').textbox("getText");
    var path_en = base64_encode(path);
    $.get("files_watch", {"action":"add", "param":path_en},
        function(data){
            
            get_files_watch();
            console.log(data);
        }, 
        "json");
    
    $('#add_files_watch_dlg').dialog('close')
}

function check_file_watch_tab_exist(id) {
    var items = $('#files_watch_tabs').find('#' + id);
    if (items.length>0) {
        return true;
    }
    return false;
}

function get_files_watch() {
    $.get("files_watch", {"action":"get_list", "param":""},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                for (var index = 0; index < data.list.length; index++) {
                    var item = data.list[index];
                    if (check_file_watch_tab_exist(item.id)) {
                        continue;
                    }
                    $("#files_watch_tabs").tabs('add',{
                        id:item.id,
                        title:item.name,
                        content:"",
                        closable:true,
                        path:item.path,
                        tools:[{
                            iconCls:'icon-mini-refresh',
                            handler:function(){
                                get_file_last_content(item.id, item.path);
                            }
                        }],
                    });
                    $("#files_watch_tabs").find('#' + item.id).attr("path",item.path);
                    get_file_last_content(item.id, item.path);
                }
            }
        },
        "json");
}

function make_file_watch_textarea_id(id) {
    return "file_watch_area_"+id;
}

function make_file_tab_panel_data(tab_id, data) {
    return "<textarea id='" + make_file_watch_textarea_id(tab_id) + "' style='width:100%;height:100%'>" + data + "</textarea>";
}

function get_file_last_content(tab_id,path) {
    $.get("files_watch", {"action":"get_file", "param":path},
        function(data){
            console.log(data);
            var tab_t = $('#files_watch_tabs').find('#' + tab_id);
            var html_text = make_file_tab_panel_data(tab_id,data);
            $("#files_watch_tabs").tabs('update',{tab:tab_t, options:{content:html_text}});
            var area_id = make_file_watch_textarea_id(tab_id);
            var scrollTop = $("#" + area_id )[0].scrollHeight;  
            $("#" + area_id ).scrollTop(scrollTop); 
        });
}

function get_file_last_content_by_index(tab_index) {
    var tab_id = $("#files_watch_tabs").tabs('getTab',tab_index).panel('options').id;
    var path_en = $("#files_watch_tabs").tabs('getTab',tab_index).attr("path");
    get_file_last_content(tab_id,path_en);
}

function remove_file_watch(tab_index) {
    var file_path = $("#files_watch_tabs").tabs('getTab',tab_index).panel('options').path; //base64encode
    $.get("files_watch", {"action":"remove", "param":file_path},
      function(data){
            console.log(data);
            if (data.ret == 1) {
                
            }
            });
    return true;
}