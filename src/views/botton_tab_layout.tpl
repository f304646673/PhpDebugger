<div id="botton_tab_layout" data-options="region:'south',split:true" style="height:200px;min-height:40px;">
    <div class="easyui-tabs" id="botton_tab" data-options="fit:true,border:false,plain:true,tabWidth:135,">
        <div title="Stack" style="padding:5px;" data-options="tools:'#botton_stack_tab_tools'">
            <table class="easyui-datagrid" id="stack_datagrid" style="width:100%;height:100%" data-options="singleSelect:true">
                <thead>
                    <tr>
                        <th data-options="field:'frame'" style="width:5%">Frame</th>
                        <th data-options="field:'filename'" style="width:75%">File</th>
                        <th data-options="field:'lineno'" style="width:5%">Line</th>
                        <th data-options="field:'function'" style="width:15%">Function</th>
                        <th data-options="field:'file_id'" style="width:0%" hidden="true"></th>
                        <th data-options="field:'filename_last'" style="width:0%" hidden="true"></th>
                    </tr>
                </thead>
            </table>
        </div>
        <div title="Variables" style="padding:5px" data-options="tools:'#botton_variables_tab_tools'">
            <table id="variables_treegrid" class="easyui-treegrid" style="width:100%;height:100%" data-options="idField:'id',treeField:'name'">
                <thead>
                    <tr>
                        <th data-options="field:'name'" style="width:20%">Name</th>
                        <th data-options="field:'type'" style="width:10%">Type</th>
                        <th data-options="field:'value'" style="width:70%">Value</th>
                    </tr>
                </thead>
            </table>
        </div>
        <div title="Breakpoint" style="padding:5px" data-options="tools:'#botton_breakpoint_tab_tools'">
            <table class="easyui-datagrid" id="breakpoint_datagrid" data-options="singleSelect:true,fit:true,fitColumns:true">
                <thead>
                    <tr>
                        <th data-options="field:'itemid',align:'center'" width="60">ID</th>
                        <th data-options="field:'type',align:'center'" width="80">Type</th>
                        <th data-options="field:'state',align:'center'" width="80">State</th>
                        <th data-options="field:'filename',align:'center'" width="180">Filename</th>
                        <th data-options="field:'lineno',align:'center'" width="60">Lineno</th>
                        <th data-options="field:'function',align:'center'" width="180">Function</th>
                        <th data-options="field:'exception',align:'center'" width="150">Exception</th>
                        <th data-options="field:'expression',align:'center'" width="250">Expression</th>
                        <th data-options="field:'hit_value',align:'center'" width="120">Hit_value</th>
                        <th data-options="field:'hit_condition',align:'center'" width="150">Hit_condition</th>
                        <th data-options="field:'hit_count',align:'center'" width="100">Hit_count</th>
                        <th data-options="field:'operation',align:'center'" width="100">Operation</th>
                    </tr>
                </thead>
            </table>  
        </div>
        <div title="Files Watch" style="padding:5px;" data-options="tools:'#botton_files_watch_tab_tools'">
            <div id="files_watch_tabs" class="easyui-tabs" style="width:100%;height:100%;">
            </div>
        </div>

        <div title="Variables Watch" style="padding:5px;" data-options="tools:'#botton_variables_watch_tab_tools'">
            <div id="variables_watch_tabs" class="easyui-tabs" style="width:100%;height:100%;">
            </div>
        </div>
    </div>
</div>


<div id="botton_variables_tab_tools">
    <a href="javascript:void(0)" class="icon-mini-refresh" onclick="get_variables_list();"></a>
</div>

<div id="botton_stack_tab_tools">
    <a href="javascript:void(0)" class="icon-mini-refresh" onclick="get_stack_list();"></a>
</div>

<div id="botton_breakpoint_tab_tools">
    <a href="javascript:void(0)" class="icon-mini-add" onclick="add_breakpoint_dlg_open();"></a>
    <a href="javascript:void(0)" class="icon-mini-refresh" onclick="get_breakpoint_list()"></a>
</div>

<div id="botton_files_watch_tab_tools">
    <a href="javascript:void(0)" class="icon-mini-add" onclick="add_files_watch_dlg_open();"></a>
    <a href="javascript:void(0)" class="icon-mini-refresh" onclick="get_files_watch()"></a>
</div>

<div id="botton_variables_watch_tab_tools">
    <a href="javascript:void(0)" class="icon-mini-add" onclick="add_variables_watch_dlg_open();"></a>
    <a href="javascript:void(0)" class="icon-mini-refresh" onclick="get_variables_watch()"></a>
</div>
                        
<div id="variables_treegrid_contextmenu" class="easyui-menu" style="width:160px;">
    <div onclick="show_variable_in_dialog_from_menucontent()" data-options="iconCls:'icon-search'">Show</div>
    <div onclick="add_variable_watch_in_dialog_from_menucontent()" data-options="iconCls:'icon-variables-watch-add'">Add Variable Watch</div>
    <div onclick="eval_variable_in_dialog_from_menucontent()" data-options="iconCls:'icon-pencil'">Modify Value</div>
    <div class="menu-sep"></div>
    <div onclick="variables_treegrid_contextmenu_collapse()">Collapse</div>
    <div onclick="variables_treegrid_contextmenu_expand()">Expand</div>
</div>