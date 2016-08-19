<div id="save_request_dlg" class="easyui-dialog" style="width:400px;height:150px;padding:10px 20px"
    closed="true" buttons="#save_request_dlg_buttons" data-options="iconCls:'icon-save-request',resizable:false,modal:true">
    <label>Request Name:</label>
    <input id="save_request_dlg_request_name" class="easyui-textbox" style="width:340px;" required="true">
</div>

<div id="save_request_dlg_buttons">
    <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="save_request();" style="width:90px">Save</a>
    <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel" onclick="save_request_dlg_close();" style="width:90px">Cancel</a>
</div>
