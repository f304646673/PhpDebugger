<html>
    <head>
        <link rel="stylesheet" type="text/css" href="/files/third/jquery-easyui-1.4.5/themes/default/easyui.css">
        <link rel="stylesheet" type="text/css" href="/files/third/jquery-easyui-1.4.5/themes/icon.css">
        <link rel="stylesheet" href="/files/third/highlight/styles/tomorrow-night-eighties.css"></link>
        <link rel="stylesheet" type="text/css" href="/files/themes/debugger.css">
        
        <script src="/files/third/jquery3_1/jquery-3.1.0.js" type="text/javascript"></script>
        <script type="text/javascript" src="/files/third/jquery-easyui-1.4.5/jquery.min.js"></script>
        <script type="text/javascript" src="/files/third/jquery-easyui-1.4.5/jquery.easyui.min.js"></script>
        <script src="/files/third/jquery_timer/jquery.timer.js"></script>
        <script src="/files/third/jquery_base64_js/jquery.base64.js"></script>
        
        <script type="text/javascript">
            $(document).ready(function(){
                var data = "{{data}}";
                var data_str = $('<div/>').html(data).text();
                var data_json = eval('(' + data_str + ')');
                var get_data = data_json.get;
                var post_data = data_json.post;
                
                for(var p in get_data){
                    var key = p;
                    var value = get_data[p];
                    add_get_param(key,value);
                }  
                
                for(var p in post_data){
                    var key = p;
                    var value = post_data[p];
                    add_post_param(key,value);
                }
                
                if (undefined != data_json.url) {
                    $("#url_input").textbox("setText", data_json.url);
                }
                if (undefined != data_json.mode) {
                    if ("get" == data_json.mode) {
                        $("#get_mode_radio").attr("checked",'checked');
                    }
                    else if ("post" == data_json.mode) {
                        $("#post_mode_radio").attr("checked",'checked');
                    }
                }
            });
            
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
            
            function generate_tr_class_name(mode) {
                return mode + "_param_tr";
            }
            
            function generate_td_name_class_name(mode) {
                return mode + "_param_td_name";
            }
            
            function generate_td_name_textarea_class_name(mode) {
                return mode + "_param_name_textarea";
            }
            
            function generate_td_value_class_name(mode) {
                return mode + "_param_td_value";
            }
            
            function generate_td_value_textarea_class_name(mode) {
                return mode + "_param_value_textarea";
            }
            
            function add_get_param() {
                var args = arguments;
                var argsLen = args.length ;
                if(argsLen == 2){
                    add_param("get", args[0], args[1]);
                } else {
                    add_param("get");
                }
            }
            
            function add_post_param() {
                var args = arguments;
                var argsLen = args.length ;
                if(argsLen == 2){
                    add_param("post", args[0], args[1]);
                } else {
                    add_param("post");
                }
            }
            
            function add_param(mode) {
                var key = "";
                var value = "";
                var args = arguments;
                var argsLen = args.length ;
                if(argsLen == 3){
                    key = args[1];
                    value = args[2];
                }
                
                var tr_class_name = generate_tr_class_name(mode);
                var td_name_class_name = generate_td_name_class_name(mode);
                var td_name_textarea_class_name = generate_td_name_textarea_class_name(mode);
                
                var item_tr = $('<tr style="border:1px solid #ff00ff;"/>').addClass(tr_class_name);
                var item_td_name = $('<td style="width:10%;height:40px;"/>').addClass(td_name_class_name);
                var item_td_name_textarea = $('<textarea style="width:100%;height:40px;" rows=2/>').addClass(td_name_textarea_class_name);
                item_td_name_textarea.html(key);
                item_td_name.append(item_td_name_textarea);
                
                var td_value_class_name = generate_td_value_class_name(mode);
                var td_value_textarea_class_name = generate_td_value_textarea_class_name(mode);
                
                var item_td_value = $('<td style="width:90%;height:40px;"/>').addClass(td_value_class_name);
                var item_td_value_textarea = $('<textarea style="width:100%;height:40px;" rows=2/>').addClass(td_value_textarea_class_name);
                item_td_value_textarea.html(value);
                item_td_value.append(item_td_value_textarea);
                
                item_tr.append(item_td_name);
                item_tr.append(item_td_value);
                $("#" + mode + "_table_body").append(item_tr);
            }
            
            function save_request_data() {
                var data = get_request_data_from_ui();
                if (undefined == data ) {
                    return;
                }
                
            }
            
            function get_request_data_from_ui() {
                var mode = "";
                mode = $("#get_mode_radio:checked").val();
                if (undefined == mode) {
                    mode = $("#post_mode_radio:checked").val();
                }
                if (undefined == mode) {
                    alert("Select Mode!");
                    return;
                }
                
                var ret_data = new Object();
                ret_data["get"] = get_mode_param("get");
                ret_data["post"] = get_mode_param("post");
                ret_data["url"] = $("#url_input").textbox("getText");
                ret_data["mode"] = mode;
                var json_data =  JSON.stringify(ret_data);
                return json_data;
            }
            
            function get_mode_param(mode) {
                var body_name = "";
                if ("get" == mode) {
                    body_name = "get_table_body";
                } else if ("post" == mode) {
                    body_name = "post_table_body";
                } else {
                    return;
                }
                var params_info = new Object();
                var td_name_textarea_class_name = generate_td_name_textarea_class_name(mode);
                var td_value_textarea_class_name = generate_td_value_textarea_class_name(mode);
                $.each($("#" + body_name + " tr"),function(n,value) {
                    var $item = $(value);
                    var key = $item.find("." + td_name_textarea_class_name).val();
                    var value = $item.find("." + td_value_textarea_class_name).val();
                    params_info[key] = value;
                });
                return params_info;
            }
            
            function send_request_data() {
                
            }
        </script>
        
        <title>Cmd Shell</title>
    </head>
    <body>
        <h2>Request Edit And Send</h2>
        <div class="easyui-panel" style="height:800px;">
            <div class="easyui-accordion" style="width:100%;heigth:100%">
                <div title="Top Panel" data-options="collapsed:false,collapsible:false" style="height:100px;">
                    <table style="width:100%;height:100%;">
                        <tbody>
                            <tr>
                                <td align="center">
                                    <a href="#" class="easyui-linkbutton" data-options="iconCls:'icon-save'" style="width:200px" onclick="save_request_data();">Save</a>
                                </td>
                                <td align="center">
                                    <a href="#" class="easyui-linkbutton" data-options="iconCls:'icon-tick'" style="width:200px" onclick="send_request_data();">Send</a>
                                </td>
                             </tr>
                        </tbody>
                    </table>
                </div>
                <div title="Base" data-options="selected:true" style="">
                    <table style="width:100%;height:100px;">
                        <tbody>
                            <tr>
                                <td style="width:5px;height:100%;">URL</td>
                                <td style="width:95%;height:100%;" colspan='2'>
                                    <input id="url_input" class="easyui-textbox" data-options="prompt:'Input Url...'" style="width:100%;height:100%;" multiline="true">
                                </td>
                            </tr>
                            <tr>
                                <td>Mode</td>
                                <td>
                                    <input id="post_mode_radio" type="radio" name="mode" value="post">Post</input>
                                </td>
                                <td>
                                    <input id="get_mode_radio" type="radio" name="mode" value="get">Get</input>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div title="Get" style="min-height: 200px" data-options="split:true,tools:[{
                        iconCls:'icon-add',
                        handler:function(){add_get_param();}
                    }]">
                    <table style="width:100%;height:100px;" border="1" bordercolor="#a0c6e5">
                        <tr style="width:100%;height:20px;">
                            <th style="width:10%;height:20px;">Param Name</th>
                            <th style="width:90%;height:20px;">Param Value</th>
                        </tr>
                        <tbody id="get_table_body">
                            
                        </tbody>
                    </table>
                </div>
                <div title="Post" style="min-height: 200px" data-options="split:true,tools:[{
                        iconCls:'icon-add',
                        handler:function(){add_post_param();}
                    }]">
                    <table style="width:100%;height:100px;" border="1" bordercolor="#a0c6e5">
                        <tbody style="width:100%;height:20px;">
                            <tr style="width:100%;height:20px;">
                                <th style="width:10%;height:20px;">Param Name</th>
                                <th style="width:90%;height:20px;">Param Value</th>
                            </tr>
                        </tbody>
                        <tbody id="post_table_body">
                            
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
</html>
