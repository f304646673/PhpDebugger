<html>
    <head>
        <link rel="stylesheet" type="text/css" href="/files/third/jquery-easyui-1.4.5/themes/default/easyui.css">
        <link rel="stylesheet" type="text/css" href="/files/third/jquery-easyui-1.4.5/themes/icon.css">
        <link rel="stylesheet" href="/files/third/highlight/styles/tomorrow-night-eighties.css"></link>
        <link rel="stylesheet" type="text/css" href="/files/themes/debugger.css">
        
        <script src="/files/third/jquery3_1/jquery-3.1.0.js" type="text/javascript"></script>
        
        <script type="text/javascript" src="/files/status.js"></script>
        <script type="text/javascript" src="/files/console.js"></script>
        <script type="text/javascript" src="/files/variables.js"></script>
        <script type="text/javascript" src="/files/call_stack.js"></script>
        <script type="text/javascript" src="/files/breakpoint.js"></script>
        <script type="text/javascript" src="/files/files_watch.js"></script>
        <script type="text/javascript" src="/files/variables_watch.js"></script>
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
            //$.ajaxSetup({
            //    async: false,
            //    cache:false
            //});
  
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
                <div data-options="region:'north',split:false"style="height:60px;width:100%;min-height:60px;min-width:800px;">
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
                    </div>
                </div>
                <div data-options="region:'south',split:true" style="height:200px;min-height:40px;">
                    <div class="easyui-tabs" id="botton_tab" data-options="fit:true,border:false,plain:true,tabWidth:135,">
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
                <div  title="Folders" style="width:15%;min-width:200px" data-options="region:'west',iconCls:'icon-folder',split:true,tools:[{
                            iconCls:'icon-folder-explore',
                            handler:function(){folder_reload();}
                        },{
                            iconCls:'icon-folder-add',
                            handler:function(){add_folder_dlg_open();}
                        },{
                            iconCls:'icon-folder-del',
                            handler:function(){folder_remove();}
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
        
        <div id="add_folder_dlg" class="easyui-dialog" style="width:400px;height:150px;padding:10px 20px"
            closed="true" buttons="#add_folder_dlg_buttons" data-options="iconCls:'icon-folder-add',resizable:false,modal:true">
            <label>Folder Path:</label>
            <input name="add_folder_dlg_folder_path" class="easyui-textbox" style="width:350px;" required="true">
        </div>
                        
        <div id="add_folder_dlg_buttons">
            <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="folder_add_request();" style="width:90px">Save</a>
            <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel" onclick="add_folder_dlg_close();" style="width:90px">Cancel</a>
        </div>                        
        
        <div id="add_files_watch_dlg" class="easyui-dialog" style="width:400px;height:150px;padding:10px 20px"
            closed="true" buttons="#add_files_watch_dlg_buttons" data-options="iconCls:'icon-add'">
            <label>Files Path:</label>
            <input id="add_files_watch_add_dlg_file_name" type="text" class="easyui-textbox" style="width:340px;">    
        </div>
                        
        <div id="add_files_watch_dlg_buttons">
            <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="add_file_watch_request();" style="width:90px">Save</a>
            <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel" onclick="add_files_watch_dlg_close();" style="width:90px">Cancel</a>
        </div>    
                        
        <div id="add_variables_watch_dlg" class="easyui-dialog" style="width:400px;height:150px;padding:10px 20px"
            closed="true" buttons="#add_variables_watch_dlg_buttons" data-options="iconCls:'icon-variables-watch-add'">
            <label>Variable Name:</label>
            <input id="add_variables_watch_add_dlg_variable_name" type="text" class="easyui-textbox" style="width:340px;">        
        </div>
                          
        <div id="add_variables_watch_dlg_buttons">
            <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="add_variable_watch_by_dialg();" style="width:90px">Save</a>
            <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel" onclick="add_variables_watch_dlg_close();" style="width:90px">Cancel</a>
        </div>    
        
        <div id="tools_memu_content" style="width:150px;">
            <div data-options="iconCls:'icon-breakpoint-add'" onclick="add_breakpoint_dlg_open();">Add Breakpoint</div>
            <div class="menu-sep"></div>
            <div id="tools_memu_content_run" data-options="iconCls:'icon-run',disabled:true" onclick="run();">Run</div>
            <div id="tools_memu_content_step_over" data-options="iconCls:'icon-step-over',disabled:true" onclick="step_over();">Step Over</div>
            <div id="tools_memu_content_step_in" data-options="iconCls:'icon-step-in',disabled:true" onclick="step_in();">Step In</div>
            <div id="tools_memu_content_step_out" data-options="iconCls:'icon-step-out',disabled:true" onclick="step_out();">Step Out</div>
            <div class="menu-sep"></div>
            <div data-options="iconCls:'icon-add'" onclick="add_files_watch_dlg_open();">Add File Watch</div>
            <div class="menu-sep"></div>
            <div data-options="iconCls:'icon-variables-watch-add'" onclick="add_variables_watch_dlg_open();">Add Variable Watch</div>
            <div class="menu-sep"></div>
            <div data-options="iconCls:'icon-folder-add'" onclick="add_folder_dlg_open();">Add Folder</div>
        </div>
                        
        <div id="help_memu_content" style="width:100px;">
            <div onclick=" window.open('https://github.com/f304646673/PhpDebugger');">Help</div>
            <div onclick=" window.open('https://github.com/f304646673/PhpDebugger');">Source Code</div>
        </div>
                        
        <div id="about_memu_content" class="menu-content" style="background:#f0f0f0;padding:10px;text-align:left">
            <img src="/files/themes/img/about.png" style="width:437px;height:131px">
            <p style="font-size:14px;color:#444;">https://github.com/f304646673/PhpDebugger.git</p>
        </div>
                        
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

        <div id="variables_treegrid_contextmenu" class="easyui-menu" style="width:160px;">
            <div onclick="show_variable_in_dialog_from_menucontent()" data-options="iconCls:'icon-search'">Show</div>
            <div onclick="add_variable_watch_in_dialog_from_menucontent()" data-options="iconCls:'icon-variables-watch-add'">Add Variable Watch</div>
            <div class="menu-sep"></div>
            <div onclick="variables_treegrid_contextmenu_collapse()">Collapse</div>
            <div onclick="variables_treegrid_contextmenu_expand()">Expand</div>
        </div>
                        
        <div id="ft" style="padding:5px;">Footer Content.</div>
        
        <div id="variables_show" class="easyui-dialog" title="Variable" data-options="iconCls:'icon-search',resizable:false,modal:true" style="width:800px;height:600px;padding:10px" closed="true">
            <pre id="variables_show_json-renderer"></pre>
        </div>
        
        <div id="breakpoint_add_dialog" class="easyui-dialog" title="Add Breakpoint" style="width:600px;height:256px;" closed="true" 
                data-options="iconCls:'icon-breakpoint-add',resizable:false,modal:true">
            <div class="easyui-layout" style="width:100%;height:100%;" border="false">
                <div data-options="region:'north',split:false" style="height:180px;width:100%;" border="false">
                    <div id="breakpoint_add_dialog_tabs" class="easyui-tabs" style="width:100%;height:100%;" border="false">
                        <div title="Line" id ="breakpoint_add_dialog_tabs_line" style="padding:20px;display:none;">
                            <table style="width:100%;">
                                <tr>
                                    <td style="width:20%;">Filepath:</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_line_filename" class="easyui-textbox" name="path" style="width:100%;height:50px;" data-options="multiline:true,required:true"/>
                                    </td>
                                </tr>

                                <tr>
                                    <td style="width:20%;">Line_no:</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_line_lineno" class="easyui-textbox" name="lineno" style="width:100%" data-options="required:true"/>
                                    </td>
                                </tr>
                            </table>
                        </div>
                        <div title="Call" id ="breakpoint_add_dialog_tabs_call" style="padding:20px;display:none;">
                            <table style="width:100%;">
                                <tr>
                                    <td style="width:25%;">Function Name:</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_call_function" class="easyui-textbox" name="function" style="width:100%" data-options="required:true"/>
                                    </td>
                                </tr>
                            </table>
                        </div>
                        <div title="Return" id ="breakpoint_add_dialog_tabs_return" style="padding:20px;display:none;">
                            <table style="width:100%;">
                                <tr>
                                    <td style="width:25%;">Function Name:</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_return_function" class="easyui-textbox" name="function" style="width:100%" data-options="required:true"/>
                                    </td>
                                </tr>
                            </table>
                        </div>
                        <div title="Exception"  id ="breakpoint_add_dialog_tabs_exception" style="padding:20px;display:none;">
                            <table style="width:100%;">
                                <tr>
                                    <td style="width:25%;">Exception Name:</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_exception_exception_name" class="easyui-textbox" name="exception" style="width:100%" data-options="required:true"/>
                                    </td>
                                </tr>
                            </table>
                        </div>
                        <div title="Condition"  id ="breakpoint_add_dialog_tabs_condition"  style="padding:20px;display:none;">
                            <table style="width:100%;">
                                <tr>
                                    <td style="width:20%;">Filepath:</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_condition_filename" class="easyui-textbox" name="path" style="width:100%;height:50px;" data-options="multiline:true,required:true"/>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="width:20%;">Line_no:</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_condition_lineno" class="easyui-textbox" name="lineno" style="width:100%" data-options="required:true"/>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="width:20%;">Expression:</td>
                                    <td>
                                        <input id="breakpoint_add_dialog_condition_expression" class="easyui-textbox" name="expression" style="width:100%" data-options="required:true"/>
                                    </td>
                                </tr>
                            </table>
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
        
        <div id="right_click_line_menu" class="easyui-menu" style="width:200px;">
            <div id="right_click_line_menu_add_line_breakpoint" onclick="add_line_breakpoint_by_menu();">Add Line Breakpoint</div>
            <div id="right_click_line_menu_add_conditional_breakpoint" onclick="add_conditional_breakpoint_by_menu();">Add Condition Breakpoint</div>
        </div>
        
                
        <div id="right_click_src_menu" class="easyui-menu" style="width:280px;" data-options="onShow:save_selected_text">
            <div id="right_click_src_menu_add_variable_watch" data-options="iconCls:'icon-variables-watch-add'" onclick="add_variable_watch_by_menu();">Add Variable Watch</div>
            <div id="right_click_src_menu_add_exception_breakpoint" onclick="add_breakpoint_exception_by_menu();">Add Exception Breakpoint</div>
            <div id="right_click_src_menu_add_function_call_breakpoint" onclick="add_breakpoint_call_by_menu();">Add Function Call Breakpoint</div>
            <div id="right_click_src_menu_add_function_return_breakpoint" onclick="add_breakpoint_return_by_menu();">Add Function Return Breakpoint</div>
        </div>
        
    </body>
</html>