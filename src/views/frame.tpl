<html>
    <head>
        <link rel="stylesheet" type="text/css" href="/files/third/jquery-easyui-1.4.5/themes/default/easyui.css">
        <link rel="stylesheet" type="text/css" href="/files/third/jquery-easyui-1.4.5/themes/icon.css">
        <link rel="stylesheet" href="/files/third/highlight/styles/tomorrow-night-eighties.css"></link>
        <link rel="stylesheet" type="text/css" href="/files/themes/debugger.css">
        
        <script src="/files/third/jquery3_1/jquery-3.1.0.js" type="text/javascript"></script>
        
        <script type="text/javascript" src="/files/debug.js"></script>
        <script type="text/javascript" src="/files/files_tree.js"></script>
        <script type="text/javascript" src="/files/view.js"></script>
        <script type="text/javascript" src="/files/third/jquery-easyui-1.4.5/jquery.min.js"></script>
        <script type="text/javascript" src="/files/third/jquery-easyui-1.4.5/jquery.easyui.min.js"></script>
        <script src="/files/third/jquery_timer/jquery.timer.js"></script>
        <script src="/files/third/highlight/highlight.pack.js"></script>
        <script src="/files/third/json-viewer/jquery.json-viewer.js"></script>
        <script>hljs.initHighlightingOnLoad();</script>
        
        <script src="/files/third/jquery_base64_js/jquery.base64.js"></script>
        
        <script type="text/javascript">
            $.ajaxSetup({
                async: false
            });
  
            function base64_decode(data) {
                return $.base64.atob(data, true);
            }
            function base64_encode(data) {
                return $.base64.btoa(data);
            }
            function highlight_code(type, source) {
                return hljs.highlight(type, source);
            }
        </script>
        
        <title>Cmd Shell</title>
    </head>
    <body>
        <div id="php_debugger" class="easyui-window" title="Php Debugger" data-options="iconCls:'icon-sum',footer:'#ft'" style="width:100%;height:900px;min-width:900px;min-height:800px;padding:0px;top:0;">
            <div class="easyui-layout" style="width:100%;height:100%;min-width:800px;padding:0px;">
                <div data-options="region:'north'"style="height:60px;width:100%;min-height:60px;min-width:800px">
                    <div class="easyui-panel" style="padding:0px;" style="width:100%;height:30px;min-height:30px;min-width:800px">
                        <a href="#" class="easyui-linkbutton" data-options="plain:true">Home</a>
                        <a href="#" class="easyui-menubutton" data-options="menu:'#tools_memu_content',iconCls:'icon-tools'">Tools</a>
                        <a href="#" class="easyui-menubutton" data-options="menu:'#help_memu_content',iconCls:'icon-help-fl'">Help</a>
                        <a href="#" class="easyui-menubutton" data-options="menu:'#about_memu_content',iconCls:'icon-about'">About</a>
                        <a href="#" class="easyui-linkbutton" data-options="iconCls:'icon-console',plain:true" onclick="$('#console_dlg').dialog('open')">Console</a>
                    </div>
                    <div class="easyui-panel" style="padding:0px;"  style="width:100%;height:30px;min-height:30px;min-width:800px">
                        <input id="start_stop_debug" class="easyui-switchbutton" style="hight:30px;width:70px">
                        <a href="#" id="run_debug" class="easyui-linkbutton" style="hight:30px;width:30px" data-options="iconCls:'icon-run',plain:true" onclick="run()" disabled></a>
                        <a href="#" id="step_over_debug" class="easyui-linkbutton" style="hight:30px;width:30px" data-options="iconCls:'icon-step-over',plain:true" onclick="step_over()" disabled></a>
                        <a href="#" id="step_in_debug" class="easyui-linkbutton" style="hight:30px;width:30px" data-options="iconCls:'icon-step-in',plain:true" onclick="step_in()" disabled></a>
                        <a href="#" id="step_out_debug" class="easyui-linkbutton" style="hight:30px;width:30px" data-options="iconCls:'icon-step-out',plain:true" onclick="step_out()" disabled></a>
                    </div>
                </div>
                <div data-options="region:'south',split:true" style="height:200px;">
                    <div class="easyui-tabs" id="botton_tab" data-options="fit:true,border:false,plain:true">
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
                        <div title="Stack" style="padding:5px" data-options="tools:'#botton_stack_tab_tools'">
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
                                        <th data-options="field:'hit_value',align:'center'" width="150">Hit_value</th>
                                        <th data-options="field:'hit_condition',align:'center'" width="250">Hit_condition</th>
                                        <th data-options="field:'hit_count',align:'center'" width="80">Hit_count</th>
                                    </tr>
                                </thead>
                            </table>  
                        </div>
                    </div>
                </div>
                <div  title="Floders" style="width:15%;min-width:200px" data-options="region:'west',iconCls:'icon-floder',split:true,tools:[{
                            iconCls:'icon-reload',
                            handler:function(){floder_reload();}
                        },{
                            iconCls:'icon-add',
                            handler:function(){floder_add();}
                        },{
                            iconCls:'icon-remove',
                            handler:function(){floder_remove();}
                        }]">
                    <ul id="files_tree" class="easyui-tree" data-options="animate:true,dnd:true,lines:true">
                    </ul>
                </div>
                <div data-options="region:'center',title:'Source',iconCls:'icon-page'" style="">
                    <div class="easyui-tabs" id="files_tab" data-options="fit:true,border:false,plain:true,tools:'#files_tab_tools'">
                    </div>
                </div>
            </div>
        </div>
        
        <div id="botton_variables_tab_tools">
            <a href="javascript:void(0)" class="icon-mini-refresh" onclick="getVariables()"></a>
        </div>
        
        <div id="botton_stack_tab_tools">
            <a href="javascript:void(0)" class="icon-mini-refresh" onclick="getStack()"></a>
        </div>
        
        <div id="botton_breakpoint_tab_tools">
            <a href="javascript:void(0)" class="icon-mini-add" onclick="javascript:$('#breakpoint_add_dialog').dialog('open')"></a>
            <a href="javascript:void(0)" class="icon-mini-refresh" onclick="getBreakpoint()"></a>
        </div>
        
        <div id="floders_tools">
            <a href="#" class="icon-reload" onclick="floder_reload()"></a>
            <a href="#" class="icon-add" onclick="floder_add()"></a>
            <a href="#" class="icon-remove" onclick="floder_remove()"></a>
        </div>
        
        <div id="add_floder_dlg" class="easyui-dialog" style="width:400px;height:150px;padding:10px 20px"
            closed="true" buttons="#add_floder_dlg_buttons">
            <form id="add_floder_dlg_fm" url="files_tree" method="get" novalidate>
                <div class="fitem">
                    <label>Floder Path:</label>
                    <input name="add_floder_dlg_floder_path" class="easyui-textbox" style="width:350px;" required="true">
                </div>
            </form>
        </div>
                        
        <div id="add_floder_dlg_buttons">
            <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="floder_add_request()" style="width:90px">Save</a>
            <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel" onclick="javascript:$('#add_floder_dlg').dialog('close')" style="width:90px">Cancel</a>
        </div>
        
        <div id="tools_memu_content" style="width:150px;">
            <div data-options="iconCls:'icon-add'" onclick="javascript:$('#breakpoint_add_dialog').dialog('open');">Add Breakpoint</div>
            <div data-options="iconCls:'icon-redo'">Redo</div>
            <div class="menu-sep"></div>
            <div>Cut</div>
            <div>Copy</div>
            <div>Paste</div>
            <div class="menu-sep"></div>
            <div>
                <span>Toolbar</span>
                <div>
                    <div>Address</div>
                    <div>Link</div>
                    <div>Navigation Toolbar</div>
                    <div>Bookmark Toolbar</div>
                    <div class="menu-sep"></div>
                    <div>New Toolbar...</div>
                </div>
            </div>
            <div data-options="iconCls:'icon-remove'">Delete</div>
            <div>Select All</div>
        </div>
                        
        <div id="help_memu_content" style="width:100px;">
            <div onclick=" window.open('https://github.com/f304646673/PhpDebugger');">Help</div>
            <div onclick=" window.open('https://github.com/f304646673/PhpDebugger');">Source Code</div>
        </div>
                        
        <div id="about_memu_content" class="menu-content" style="background:#f0f0f0;padding:10px;text-align:left">
            <img src="/files/themes/img/about.png" style="width:437px;height:131px">
            <p style="font-size:14px;color:#444;">https://github.com/f304646673/PhpDebugger.git</p>
        </div>
        
        <div id="console_dlg" class="easyui-dialog" title="Debug Console" style="width:900px;height:800px;padding:10px" data-options="resizable:true" closed="true">
            <div id="console_dlg_div" style="width:100%;height:100%;">
                <div data-options="region:'center'" style="width:100%;">
                    <div style="margin:0px 0;width:100%;height:100%">
                        <input id="console_dlg_view" class="easyui-textbox" data-options="multiline:true" value="" style="width:100%;height:100%" readonly="true">
                    </div>
                </div>
                <div data-options="region:'south'" style="height:26px;width:100%;">
                    <div style="margin:0px 0;width:100%;height:100%">
                        <input id="console_dlg_cmd" class="easyui-textbox" data-options="multiline:false" value="" style="width:100%;height:100%">
                    </div>
                </div>
            </div>
        </div>           

        <div id="variables_treegrid_contextmenu" class="easyui-menu" style="width:120px;">
            <div onclick="show_variable_in_dialog_from_menucontent()" data-options="iconCls:'icon-search'">Show</div>
            <div class="menu-sep"></div>
            <div onclick="collapse()">Collapse</div>
            <div onclick="expand()">Expand</div>
        </div>
                        
        <div id="ft" style="padding:5px;">Footer Content.</div>
        
        <div id="variables_show" class="easyui-dialog" title="Variable" data-options="iconCls:'icon-search'" style="width:800px;height:600px;padding:10px" closed="true">
            <pre id="variables_show_json-renderer"></pre>
        </div>
        
        <div id="breakpoint_add_dialog" class="easyui-dialog" title="Add Breakpoint" style="width:600px;height:240px;" closed="true" 
                data-options="iconCls:'icon-add',resizable:false,modal:true">
            <div class="easyui-layout" style="width:100%;height:100%;" border="false">
                <div data-options="region:'north',split:false" style="height:164px;width:100%;" border="false">
                    <div id="breakpoint_add_dialog_tabs" class="easyui-tabs" style="width:100%;height:100%;" border="false">
                        <div title="Line" id ="breakpoint_add_dialog_tabs_line" style="padding:20px;display:none;">
                            <table style="width:100%;">
                                <tr>
                                    <td>Filepath</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_line_filename" class="easyui-textbox" name="path" style="width:100%;height:50px;" data-options="multiline:true,required:true"/>
                                    </td>
                                </tr>

                                <tr>
                                    <td>line_no</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_line_lineno" class="easyui-textbox" name="lineno" style="width:100%" data-options="required:true"/>
                                    </td>
                                </tr>
                            </table>
                        </div>
                        <div title="Call" id ="breakpoint_add_dialog_tabs_call" style="padding:20px;display:none;">
                            <table style="width:100%;">
                                <tr>
                                    <td>Function Name</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_call_function" class="easyui-textbox" name="function" style="width:100%" data-options="required:true"/>
                                    </td>
                                </tr>
                            </table>
                        </div>
                        <div title="Return" id ="breakpoint_add_dialog_tabs_return" style="padding:20px;display:none;">
                            <table style="width:100%;">
                                <tr>
                                    <td>Function Name</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_return_function" class="easyui-textbox" name="function" style="width:100%" data-options="required:true"/>
                                    </td>
                                </tr>
                            </table>
                        </div>
                        <div title="Exception"  style="padding:20px;display:none;">
                            Exception
                        </div>
                        <div title="Condition"  style="padding:20px;display:none;">
                            Condition
                        </div>
                        <div title="Watch"  style="padding:20px;display:none;">
                            Watch
                        </div>
                    </div>
                </div>
                <div data-options="region:'center',split:false," style="height:63px;width:100%;" border="false">
                    <div style="text-align:center;padding:5px 0">
                        <a href="javascript:void(0)" class="easyui-linkbutton" onclick="add_breakpoint()" style="width:80px">Submit</a>
                    </div>
                </div>
            </div>
        </div>
        
    </body>
</html>