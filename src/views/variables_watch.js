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
}

function getVariablesWatch() {
    
}
