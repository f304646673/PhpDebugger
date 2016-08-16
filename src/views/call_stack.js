/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function get_stack_list() {
    $('#breakpoint_add_dialog_tabs').tabs("select", "Stack");
    $.post("do", {"action":"stack_get", "param":""},
        function(data){
            if (data.ret == 1) {
                rebuild_statck_info(data.data);
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