<div id="setting_dialog" class="easyui-dialog" title="Setting" style="width:600px;height:196px;" closed="true" 
        data-options="iconCls:'icon-cog',resizable:false,modal:true" buttons="#setting_dlg_buttons" >
    <div class="easyui-layout" style="width:100%;height:100%;" border="false">
        <table style="width:100%;">
            <tr>
                <td style="width:40%;">All Stack Parameters</td>
                <td>
                    <input id="setting_dialog_all_statck_parameters" class="easyui-switchbutton" style="hight:30px;width:70px">
                </td>
            </tr>

            <tr>
                <td style="width:40%;">Variables Watch</td>
                <td>
                    <input id="setting_dialog_variable_watch" class="easyui-switchbutton" style="hight:30px;width:70px">
                </td>
            </tr>
            
            <tr>
                <td style="width:20%;">Debug Key</td>
                <td>
                    <input id="setting_dialog_debug_key" class="easyui-textbox" name="lineno" style="width:100%" data-options="required:true"/>
                </td>
            </tr>
        </table>
    </div>
</div>

<div id="setting_dlg_buttons">
    <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="save_setting();" style="width:90px">Save</a>
    <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel" onclick="cancel_setting();" style="width:90px">Cancel</a>
</div>
