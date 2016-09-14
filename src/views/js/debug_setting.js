/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function setting_dlg_open() {
    $.get("setting", {"action":"get", "param":''},
        function(data_json){
            if (data_json['all_stack_parameters']) {
                $('#setting_dialog_all_statck_parameters').switchbutton('check')
            }
            else {
                $('#setting_dialog_all_statck_parameters').switchbutton('uncheck')
            }
            
            if (data_json['variable_watch']) {
                $('#setting_dialog_variable_watch').switchbutton('check')
            }
            else {
                $('#setting_dialog_variable_watch').switchbutton('uncheck')
            }
            
            $('#setting_dialog_debug_key').textbox("setText", data_json['ide_key']);
            $('#setting_dialog').dialog('open').dialog('center').dialog('setTitle','Setting');
            $('#add_folder_dlg_folder_path').textbox('clear');
        }, "json");
}

function setting_dlg_close() {
    $('#setting_dialog_debug_key').textbox('clear');
    $('#setting_dialog').dialog('close');
}

function save_setting() {
    var all_stack_parameters = $('#setting_dialog_all_statck_parameters').switchbutton('options').checked;
    var variable_watch = $('#setting_dialog_variable_watch').switchbutton('options').checked;
    var ide_key = $('#setting_dialog_debug_key').textbox("getText");
    
    var params = new Object();
    params['all_stack_parameters'] = all_stack_parameters;
    params['variable_watch'] = variable_watch;
    params['ide_key'] = ide_key;
    var request_de = JSON.stringify(params);
    var request_en = base64_encode(request_de);
    
    $.get("setting", {"action":"set", "param":request_en},
        function(data){
            console.log(data);
            setting_dlg_close();
        });
}

function cancel_setting() {
    setting_dlg_close();
}