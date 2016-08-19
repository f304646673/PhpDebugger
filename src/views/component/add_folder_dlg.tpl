<div id="add_folder_dlg" class="easyui-dialog" style="width:400px;height:150px;padding:10px 20px"
    closed="true" buttons="#add_folder_dlg_buttons" data-options="iconCls:'icon-folder-add',resizable:false,modal:true">
    <label>Folder Path:</label>
    <input id="add_folder_dlg_folder_path" class="easyui-textbox" style="width:340px;" required="true">
</div>

<div id="add_folder_dlg_buttons">
    <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="folder_add_request();" style="width:90px">Save</a>
    <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel" onclick="add_folder_dlg_close();" style="width:90px">Cancel</a>
</div>
