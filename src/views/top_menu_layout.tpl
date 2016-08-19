<div id="top_menu_layout" data-options="region:'north',split:false"style="height:60px;width:100%;min-height:60px;min-width:800px;">
    <div class="easyui-panel" style="padding:0px;" style="width:100%;height:30px;min-height:30px;min-width:800px;border:1px;">
        <a href="#" class="easyui-linkbutton" data-options="plain:true">Home</a>
        <a href="#" class="easyui-menubutton" data-options="menu:'#tools_memu_content',iconCls:'icon-tools'">Tools</a>
        <a href="#" class="easyui-menubutton" data-options="menu:'#help_memu_content',iconCls:'icon-help-fl'">Help</a>
        <a href="#" class="easyui-menubutton" data-options="menu:'#about_memu_content',iconCls:'icon-about'">About</a>
        <a href="#" class="easyui-linkbutton" data-options="iconCls:'icon-console',plain:true" onclick="$('#console_dlg').dialog('open')">Console</a>
    </div>
    <div class="easyui-panel" style="padding:0px;"  style="width:100%;height:30px;min-height:30px;min-width:800px;border:1px;">
        <input id="start_stop_debug" class="easyui-switchbutton" style="hight:30px;width:70px">
        <a href="#" id="run_debug" class="easyui-linkbutton" style="hight:30px;width:30px" data-options="iconCls:'icon-run',plain:true" onclick="run()" disabled></a>
        <a href="#" id="step_over_debug" class="easyui-linkbutton" style="hight:30px;width:30px" data-options="iconCls:'icon-step-over',plain:true" onclick="step_over()" disabled></a>
        <a href="#" id="step_in_debug" class="easyui-linkbutton" style="hight:30px;width:30px" data-options="iconCls:'icon-step-in',plain:true" onclick="step_in()" disabled></a>
        <a href="#" id="step_out_debug" class="easyui-linkbutton" style="hight:30px;width:30px" data-options="iconCls:'icon-step-out',plain:true" onclick="step_out()" disabled></a>
        <a href="#" id="save_request" class="easyui-linkbutton" style="hight:30px;width:30px" data-options="iconCls:'icon-save-request',plain:true" onclick="save_request_dlg_open()" disabled></a>
    </div>
</div>

<div id="tools_memu_content" style="width:150px;">
    <div data-options="iconCls:'icon-breakpoint-add'" onclick="add_breakpoint_dlg_open();">Add Breakpoint</div>
    <div class="menu-sep"></div>
    <div id="tools_memu_content_run" data-options="iconCls:'icon-run',disabled:true" onclick="run();">Run</div>
    <div id="tools_memu_content_step_over" data-options="iconCls:'icon-step-over',disabled:true" onclick="step_over();">Step Over</div>
    <div id="tools_memu_content_step_in" data-options="iconCls:'icon-step-in',disabled:true" onclick="step_in();">Step In</div>
    <div id="tools_memu_content_step_out" data-options="iconCls:'icon-step-out',disabled:true" onclick="step_out();">Step Out</div>
    <div class="menu-sep"></div>
    <div id="tools_memu_content_save_request" data-options="iconCls:'icon-save-request'" onclick="save_request_dlg_open();">Save Request</div>
    <div class="menu-sep"></div>
    <div data-options="iconCls:'icon-pencil'" onclick="modify_variable_dlg_open();">Modify Variable</div>
    <div class="menu-sep"></div>
    <div data-options="iconCls:'icon-add'" onclick="add_files_watch_dlg_open();">Add File Watch</div>
    <div class="menu-sep"></div>
    <div data-options="iconCls:'icon-variables-watch-add'" onclick="add_variables_watch_dlg_open();">Add Variable Watch</div>
    <div class="menu-sep"></div>
    <div data-options="iconCls:'icon-folder-add'" onclick="add_folder_dlg_open();">Add Folder</div>
</div>

<div id="help_memu_content" style="width:100px;">
    <div onclick="open_help_url();">Help</div>
    <div onclick="open_source_code_url();">Source Code</div>
</div>


<div id="about_memu_content" class="menu-content" style="background:#f0f0f0;padding:10px;text-align:left">
    <img src="/files/themes/img/about.png" style="width:437px;height:131px">
    <p style="font-size:14px;color:#444;">https://github.com/f304646673/PhpDebugger.git</p>
</div>