<html>
    <head>
        <link rel="stylesheet" href="/files/third/dtree/css/dtree.css"></link>
        <link rel="stylesheet" href="/files/third/highlight/styles/tomorrow-night-eighties.css"></link>
        <link href="/files/third/json-viewer/jquery.json-viewer.css" type="text/css" rel="stylesheet"></link>
        <script src="/files/third/jquery3_1/jquery-3.1.0.js" type="text/javascript"></script>
        <script src="/files/third/dtree/js/dtree.js"></script>
        <script src="/files/third/json-viewer/jquery.json-viewer.js"></script>
        <script src="/files/third/highlight/highlight.pack.js"></script>
        <script src="/files/third/jquery_base64_js/jquery.base64.js"></script>
        <script>hljs.initHighlightingOnLoad();</script>
        <style>
             table{
                /* border:solid red 1px;*/
                 border-collapse: collapse;
                 text-align: center;
             }
             td{
                 border:solid green 1px;
                /* padding:5px;*/
             }

            pre {
                position: relative;
                margin-bottom: 24px;
                border-radius: 3px;
                border: 1px solid #C3CCD0;
                background: #FFF;
            }
            
            #current_src {
                width: 800px;
                height: 500px;
                overflow: scroll;
            }

            code {
              display: block;
              padding: 12px 24px;
              overflow-y: auto;
              font-weight: 300;
              font-family: Menlo, monospace;
              font-size: 0.8em;
            }

            code.has-numbering {
                margin-left: 21px;
            }

            .pre-numbering {
                position: absolute;
                top: 0;
                left: 0;
                width: 20px;
                    margin-top: 0px;
                padding: 6px 2px 6px 0;
                border-right: 1px solid #C3CCD0;
                border-radius: 3px 0 0 3px;
                background-color: #EEE;
                text-align: right;
                font-family: Menlo, monospace;
                font-size: 0.8em;
                color: #AAA;
            }
            .pre-numbering li.active {
                background-color: #f00;
                color: #fff;
            }
            .pre-numbering li.run_active {
                background-color: #0f0;
                color: #fff;
            }
            .pre-numbering li.run {
                background-color: #0f0;
                color: #aaa;
            }
            
            .pre#json-renderer {
                border: 1px solid #aaa;
                padding: 0.5em 1.5em;
            }
        </style>
        <script type="text/javascript">
            function modify_highlight() {
                var $numbering;
                $('pre code').each(function(){
                    var lines = $(this).text().split('\n').length;
                    $numbering = $('<ul/>').addClass('pre-numbering');
                    $(this)
                        .addClass('has-numbering')
                        .parent()
                        .append($numbering);
                    for(i=0;i<=lines;i++){
                        $numbering.append($('<li/>').text(i+1));
                    }
                   
                });
                
                $numbering.on('click', 'li', function(e) {
                    var $target = $(e.currentTarget),
                        isactive = $target.hasClass('active'),
                        isrun_active = $target.hasClass('run_active'),
                        isrun = $target.hasClass('run'),
                        line = $target.index() + 1;
                    
                    if (isrun_active) {
                        $target.removeClass('run_active');
                        $target.addClass('run');
                        remove_line_breakpoint(line);
                    }
                    else if (isrun) {
                        $target.removeClass('run');
                        $target.addClass('run_active');
                        set_line_breakpoint(line)
                    }
                    else if(isactive) {
                        $target.removeClass('active');
                        remove_line_breakpoint(line);
                    }
                    else {
                        $target.addClass('active');
                        set_line_breakpoint(line)
                    }
                    
                    console.log(line);
                });
            }  
            
            function set_line_breakpoint(line) {
                $.post("do", {"action":"set_line_breakpoint", "param":line},
                    function(data){
                      //alert(data.name);
                      console.log(data);
                    }, "json");
            }
            
            function remove_line_breakpoint(line) {
                $.post("do", {"action":"remove_line_breakpoint", "param":line},
                    function(data){
                      //alert(data.name);
                      console.log(data);
                    }, "json");
            }
            
            function set_current_run_line_no(line) {
                var $before_target_run = $("#current_src ul li.run:first");
                $before_target_run.removeClass("run");

                var $before_target_run_active = $("#current_src ul li.run_active:first");
                $before_target_run_active.removeClass("run_active").addClass('active');
                
                var index = line - 1;
                var query_line = "#current_src ul li:eq(" + index + ")";
                var $target = $(query_line);
                if ($target.hasClass("run_active"))
                    return;
                else if ($target.hasClass("run"))
                    return;
                else if ($target.hasClass("active"))
                    $target.removeClass("active").addClass("run_active");
                else
                    $target.addClass("run_active");
            }
            
            function check_con() {
                $.post("do", {"action":"check_con", "param":""},
                    function(data){
                      console.log(data);
                      update_cur_source_and_point();
                    }, "json");
            }
            
            function step_over() {
                $.post("do", {"action":"step_over", "param":""},
                    function(data){
                      console.log(data);
                      update_cur_source_and_point();
                    }, "json");
            }
            
            function step_in() {
                $.post("do", {"action":"step_in", "param":""},
                    function(data){
                      console.log(data);
                      update_cur_source_and_point();
                    }, "json");
            }
            
            function step_out() {
                $.post("do", {"action":"step_out", "param":""},
                    function(data){
                      console.log(data);
                      update_cur_source_and_point();
                    }, "json");
            }
            
            function run() {
                $.post("do", {"action":"run", "param":""},
                    function(data){
                      console.log(data);
                      update_cur_source_and_point();
                    }, "json");    
            }
            
            function update_cur_source(line_no) {
                $.post("do", {"action":"source", "param":""},
                    function(data){
                        $("#current_src").empty();                                      // 删除原来代码
                        $("<code class='php hljs'><code/>").appendTo($("#current_src"));     // 新增代码块
                        $("#current_src .php").html(hljs.highlight("php", data["data"]).value);      // 设置代码块内容
                        modify_highlight();
                        set_current_run_line_no(line_no);
                    }, "json");
            }
            
            function update_cur_source_and_point() {
                $.post("do", {"action":"get_last_frame_info", "param":""},
                    function(data){
                        if (data["data"]["path"] != $("#current_src_name").text()) {
                            update_cur_source(data["data"]["line_no"]);
                        }
                        else {
                            set_current_run_line_no(data["data"]["line_no"]);
                        }
                      console.log(data);
                    }, "json");    
            }
            
            function breakpoint_list() {
                $("#breakpoint_list tbody:first .breakpoint_item").remove();
                $.post("do", {"action":"breakpoint_list", "param":""},
                    function(data){
                        var header = ["id","type","filename","lineno","function","state","exception","expression","temporary","hit_count","hit_value","hit_condition"];
                        $.each(data, function(n,value){
                            var tr_item = $("<tr class='breakpoint_item'></tr>").appendTo($("#breakpoint_list tbody:first"));
                            $.each(header,function(m,key_name) {  
                                var td_item = $("<td/>").appendTo(tr_item);
                                td_item.html(value[key_name]);
                                console.log(value[key_name]);
                            });  
                            console.log(value)
                        });
                        console.log(data);
                    }, "json");
            }
            
            function get_variable() {
                $("#json-renderer").empty();
                $.post("do", {"action":"get_variable", "param":""},
                    function(data){
                    var options = {
                      collapsed: $('#collapsed').is(':checked'),
                      withQuotes: $('#with-quotes').is(':checked')
                    };
                    $('#json-renderer').jsonViewer(data, options);
                }, "json");
            }
            
            function dtree_build() {
                $(".dTree").empty();
                $.post("dtree", {"action":"build", "param":""},
                    function(data){
                    $('.dTree').html($.base64.atob(data.data, true));
                    $('.dTree').dTree();
                }, "json");
            }
            
            //debugger;
        </script>
    <title>Cmd Shell</title>
    </head>
    <body>
        <table width="100%" height="100%" border="1" cellspacing="0" cellpadding="0">
            <tr>
                <td width="100%" height="5%" colspan="2">
                    <button id="check_con" onclick="check_con()">Check_con</button>
                    <button id="step_over" onclick="step_over()">Step over</button>
                    <button id="step_in" onclick="step_in()">Step in</button>
                    <button id="step_out" onclick="step_out()">Step out</button>
                    <button id="run" onclick="step_out()">Run</button>
                    <button id="get_variable" onclick="get_variable()">Get variable</button>
                    <button id="breakpoint_list_btn" onclick="breakpoint_list()">Breakpoint_list</button>
                    <button id="dtree_build" onclick="dtree_build()">Dtree Build</button>
                </td>
            </tr>
            <tr>
                <td width="20%" height="70%">
                    <div class="dTree" style="text-align:left" width="100%" height="100%" overflow-x="scroll" overflow-y="scroll">
                    </div>
                </td>
                <td width="80%" height="70%">3</td>
            </tr>
            <tr>
                <td width="100%" height="25%" colspan="2">4</td>
            </tr>
        </table>
        
        <p><h2>Cmd Shell</h2></p>
        <form action="/cmd" method="post">
            Cmd: <input name="cmd" type="text" value="{{get('cmd','')}}"/>
            <input value="excute" type="submit" />
            <br/>
            <h1>Result</h1>
            <textarea name="result" cols=20 rows=2>{{get('result','')}}</textarea>
        </form>
        <h1>File</h1>
        <div id="current_src_name" hidden="true"></div>
        <div id="current_src_line_no" hidden="true"></div>
        <pre id="current_src"></pre>
        <pre id="json-renderer"></pre>
        <table id="breakpoint_list" border="1" cellspacing="0" cellpadding="0">
            <caption>Breakpoint List</caption> 
            <tr id="breakpoint_list_header"> 
                <th>id</th> 
                <th>type</th> 
                <th>filename</th> 
                <th>lineno</th> 
                <th>function</th> 
                <th>state</th> 
                <th>exception</th> 
                <th>expression</th> 
                <th>temporary</th> 
                <th>hit_count</th> 
                <th>hit_value</th> 
                <th>hit_condition</th> 
           </tr> 
        </table>
        <h1>context</h1>
        <textarea name="info" cols=120 rows=40>{{get('info','')}}</textarea>
    </body>
</html>
