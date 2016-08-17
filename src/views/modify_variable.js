/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function modify_variable_dlg_close() {
    $('#modify_variable_dlg_variable_name').textbox('clear');
    $('#modify_variable_dlg_variable_value').textbox('clear');
    $('#modify_variable_dlg').dialog('close');
}

function modify_variable_dlg_open() {
    $('#modify_variable_dlg').dialog('open').dialog('center').dialog('setTitle','Modify Variable');
    $('#modify_variable_dlg_variable_name').textbox('clear'); 
    $('#modify_variable_dlg_variable_value').textbox('clear');
}

function modify_variable_request() {
    var name = $('#modify_variable_dlg_variable_name').textbox("getText");
    var value = $('#modify_variable_dlg_variable_value').textbox("getText");
    var param = '{"name":"' + name + '", "value":"' + base64_encode(value) + '"}';
    var param_en = base64_encode(param)
    $.post("do", {"action":"modify_variable", "param":param_en},
        function(data){
            console.log(data);
            if (data.ret == 1) {
                update_cur_selected_tab_info();
                modify_variable_dlg_close();
            } 
        }, "json");
}

function eval_variable_in_dialog_from_menucontent() {
    var node = $('#variables_treegrid').treegrid('getSelected');
    if (node && node.type != ""){
        modify_variable_dlg_open();
        $('#modify_variable_dlg_variable_name').textbox("setText", node.name);
    }
}
