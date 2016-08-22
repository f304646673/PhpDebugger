<html>
    <head>
        <link rel="stylesheet" type="text/css" href="/files/third/jquery-easyui-1.4.5/themes/default/easyui.css">
        <link rel="stylesheet" type="text/css" href="/files/third/jquery-easyui-1.4.5/themes/icon.css">
        <link rel="stylesheet" href="/files/third/highlight/styles/tomorrow-night-eighties.css"></link>
        <link rel="stylesheet" type="text/css" href="/files/themes/debugger.css">
        
        <script src="/files/third/jquery3_1/jquery-3.1.0.js" type="text/javascript"></script>
        
        <script type="text/javascript" src="/files/js/edit_request.js"></script>
        <script type="text/javascript" src="/files/js/tools.js"></script>
        <script type="text/javascript" src="/files/js/modify_variable.js"></script>
        <script type="text/javascript" src="/files/js/request.js"></script>
        <script type="text/javascript" src="/files/js/status.js"></script>
        <script type="text/javascript" src="/files/js/console.js"></script>
        <script type="text/javascript" src="/files/js/variables.js"></script>
        <script type="text/javascript" src="/files/js/call_stack.js"></script>
        <script type="text/javascript" src="/files/js/breakpoint.js"></script>
        <script type="text/javascript" src="/files/js/files_watch.js"></script>
        <script type="text/javascript" src="/files/js/variables_watch.js"></script>
        <script type="text/javascript" src="/files/js/debug.js"></script>
        <script type="text/javascript" src="/files/js/files_tree.js"></script>
        <script type="text/javascript" src="/files/js/view.js"></script>
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
            $.ajaxSetup({
                timeout : 1000
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
                %include('top_menu_layout.tpl')
                %include('botton_tab_layout.tpl')             
                %include('folder_layout.tpl')
                %include('source_layout.tpl')
                %include('request_layout.tpl')        
            </div>
        </div>
                     
        <div id="ft" style="padding:5px;">OFF</div>
        
        %include('component/file_menu.tpl')
        %include('component/console_dlg.tpl')
        %include('component/add_folder_dlg.tpl')
        %include('component/edit_request_dlg.tpl')
        %include('component/save_request_dlg.tpl')
        %include('component/variables_show_dlg.tpl')
        %include('component/add_files_watch_dlg.tpl')
        %include('component/modify_variable_dlg.tpl')
        %include('component/breakpoint_add_dialog.tpl')
        %include('component/add_variables_watch_dlg.tpl')
        
    </body>
</html>