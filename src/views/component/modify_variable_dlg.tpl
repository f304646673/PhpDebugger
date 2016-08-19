<div id="modify_variable_dlg" class="easyui-dialog" style="width:600px;height:650px;padding:10px 20px"
    closed="true" buttons="#modify_variable_dlg_buttons" data-options="iconCls:'icon-pencil',modal:true">
    <label>Variable Name:</label>
    <input id="modify_variable_dlg_variable_name" class="easyui-textbox" class="easyui-textbox" style="width:540px;">
    <label>Variable Value:</label>
    <input id="modify_variable_dlg_variable_value" class="easyui-textbox" data-options="multiline:true" class="easyui-textbox" style="width:540px;height:500px;">  
</div>

<div id="modify_variable_dlg_buttons">
    <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="modify_variable_request();" style="width:90px">Save</a>
    <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel" onclick="modify_variable_dlg_close();" style="width:90px">Cancel</a>
</div>
