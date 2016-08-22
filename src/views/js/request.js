/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

$(document).ready(function(){
    $("#request_layout_accordion").accordion({
        onSelect:function(title,index) {
            return reload_request(title);
        }
    });
    
    $.extend(
        $.fn.accordion.methods,{
            addEventParam: function(jq) {   
            return jq.each(function() {
                var that = this;   
                var headers = $(this).find('.panel-header');   
                headers.each(function(i) {   
                    var tools = $(that).accordion('getPanel', i).panel('options').tools;   
                    if (typeof tools != "string") {   
                        $(this).find('.panel-tool a').each(function(j) {
                            if ($(this).attr("class") != "accordion-collapse" 
                                    && $(this).attr("class") != "panel-tool-collapse" 
                                    && $(this).attr("class") != "panel-tool-collapse panel-tool-expand"
                                    && $(this).attr("class") != "accordion-collapse accordion-expand") 
                            {
                                $(this).unbind('click').bind("click", {   
                                    handler: tools[j].handler   
                                }, function(e) {
                                    var name = $(this).parent().parent().find(".panel-title").text();
                                    e.data.handler.call(this, name);   
                                });  
                            }
                        });   
                    }   
                })   
            });   
        }
    });

});

function save_request_dlg_open() {
    $('#save_request_dlg').dialog('open').dialog('center').dialog('setTitle','Save Request');
    $('#save_request_dlg_request_name').textbox('clear'); 
}

function save_request_dlg_close() {
    $('#save_request_dlg_request_name').textbox('clear');
    $('#save_request_dlg').dialog('close');
}

function save_request() {
    var request_name_de = $('#save_request_dlg_request_name').textbox('getText');
    var request_name_en = base64_encode(request_name_de);
    $.post("do", {"action":"save_request", "param":request_name_en},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                edit_request_dlg_close();
                save_request_dlg_close();
                get_request_names();
                reload_request(name);
                return;
            } 
            alert(data.msg);
        }, "json");
}

function get_request_names() {
    $.get("request", {"action":"get_list", "param":""},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                update_request_names_accordion(data.list);
            }
        },
        "json");
}

function update_request_names_accordion(list) {
    var accordion_count = $("#request_layout_accordion .panel").length;
    for (var index = 0; index < accordion_count; index++) {
        var panel = $("#request_layout_accordion").accordion("getPanel",index);
        if (undefined == panel) {
            continue;
        }
        var title = panel.panel("options").title;
        if (0 == $.inArray(title, list)) {
            list.splice($.inArray(title,list),1);
        }
        else {
            $("#request_layout_accordion").accordion("remove",index);
            index--;
        }
    }

    for (var index = 0; index < list.length; index++) {
        var html_begin = "<div style='display:inline-block;width:100%;height:100%;overflow:hidden;'><table  style='width:100%;height:100%;'><tbody>";
        var html_end = "</tbody></table><div>";
        var pre_html = "<tr style='width:100%;height:100%;'><td colspan='2' style='width:100%;height:100%;'><pre></pre></td></tr>";
        
        var html = html_begin + pre_html + html_end;
        $("#request_layout_accordion").accordion("add",{
                title:list[index],
                content:html,
                tools:[{
                    iconCls:'icon-reload',
                    handler:function(x){reload_request(x);}
                },{
                    iconCls:'icon-edit',
                    handler:function(x){edit_request(x);}
                },{
                    iconCls:'icon-remove',
                    handler:function(x){remove_request(x);}
                }],
            });
    }
    
    $('#request_layout_accordion').accordion('addEventParam');
}

function reload_request(name) {
    var name_en = base64_encode(name);
    $.get("request", {"action":"get_data", "param":name_en},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                var options = {
                    collapsed: $('#collapsed').is(':checked'),
                    withQuotes: $('#with-quotes').is(':checked')
                };
                var panel = $("#request_layout_accordion").accordion("getPanel", name);
                if (undefined != panel) {
                    panel.find("pre").jsonViewer(data.data, options);
                }
            }
        },
        "json");
}

function remove_request(name) {
    var name_en = base64_encode(name);
    $.get("request", {"action":"remove_data", "param":name_en},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                get_request_names();
            }
        },
        "json");
}

function edit_request(name) {
    edit_request_dlg_open(name);
}
