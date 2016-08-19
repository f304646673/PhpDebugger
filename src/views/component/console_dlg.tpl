<div id="console_dlg" class="easyui-dialog" title="Debug Console" style="width:900px;height:800px;padding:10px" data-options="iconCls:'icon-search',resizable:true,modal:true" closed="true">
    <div id="console_dlg_div" style="width:100%;height:100%;">
        <div data-options="region:'center'" style="width:100%;">
            <div style="margin:0px 0;width:100%;height:100%">
                <textarea id="console_dlg_view" style="width:100%;height:100%;" readonly="true"></textarea>
            </div>
        </div>
        <div data-options="region:'south'" style="height:26px;width:100%;">
            <div style="margin:0px 0;width:100%;height:100%">
                <input id="console_dlg_cmd" class="easyui-textbox" data-options="multiline:false" value="" style="width:100%;height:100%">
            </div>
        </div>
    </div>
</div>
