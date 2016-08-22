/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function edit_request_dlg_open(name) {
    $('#edit_request_dlg_url_input').textbox('clear');
    $("#edit_request_dlg_request_name").html(name);
    $("#edit_request_dlg_get_table_body tr").remove();
    $("#edit_request_dlg_post_table_body tr").remove();
    $("#edit_request_dlg_post_mode_radio").removeAttr("checked");
    $("#edit_request_dlg_get_mode_radio").removeAttr("checked");
    
    $('#edit_request_dlg').dialog('open').dialog('center').dialog('setTitle','Edit Request And Send (' + name + ")");
    var name_en = base64_encode(name);
    $.get("request", {"action":"get_data", "param":name_en},
    function(data){
        console.log(data);
        if (data.ret == 1) {
            build_request_dlg(data.data);
        }
    },
    "json");
}

function edit_request_dlg_close() {
    $('#edit_request_dlg_url_input').textbox('clear');
    $('#edit_request_dlg').dialog('close');
}

function build_request_dlg(data_json) {
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
        $("#edit_request_dlg_url_input").textbox("setText", data_json.url);
    }
    if (undefined != data_json.mode) {
        if ("get" == data_json.mode) {
            $("#edit_request_dlg_get_mode_radio").prop("checked",'checked');
        }
        else if ("post" == data_json.mode) {
            $("#edit_request_dlg_post_mode_radio").prop("checked",'checked');
        }
    }
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

    var item_td_value = $('<td style="width:80%;height:40px;"/>').addClass(td_value_class_name);
    var item_td_value_textarea = $('<textarea style="width:100%;height:40px;" rows=2/>').addClass(td_value_textarea_class_name);
    item_td_value_textarea.html(value);
    item_td_value.append(item_td_value_textarea);
    
    var item_td_del = $('<td style="width:10%;height:40px;"/>');
    var item_td_del_button = $('<button type="button" style="width:100%;height:20px;"/>');
    item_td_del_button.html("del");
    item_td_del.append(item_td_del_button);
    item_td_del_button.click(function(){
        $(item_tr).remove();
    });
    
    item_tr.append(item_td_name);
    item_tr.append(item_td_value);
    item_tr.append(item_td_del);
    $("#edit_request_dlg_" + mode + "_table_body").append(item_tr);
}

function save_request_data() {
    var data = get_request_data_from_ui();
    if (undefined == data["mode"]) {
        alert("Select Mode!");
        return;
    }

    var json_data = JSON.stringify(data);
    var name = $("#edit_request_dlg_request_name").text();
    var params = new Object();
    params['name'] = base64_encode(name);
    params['value'] = base64_encode(json_data);

    var request_de = JSON.stringify(params);
    var request_en = base64_encode(request_de);
    $.get("request", {"action":"update_data", "param":request_en},
        function(data){
            if (data.ret) {
                edit_request_dlg_close();
                reload_request(name);
            }
            console.log(data);
            return;
        }, "json");
}

function get_request_data_from_ui() {
    var mode = "";
    mode = $("#edit_request_dlg_get_mode_radio:checked").val();
    if (undefined == mode) {
        mode = $("#edit_request_dlg_post_mode_radio:checked").val();
    }

    var ret_data = new Object();
    ret_data["get"] = get_mode_param("get");
    ret_data["post"] = get_mode_param("post");
    ret_data["url"] = $("#edit_request_dlg_url_input").textbox("getText");
    ret_data["mode"] = mode;
    return ret_data;
}

function get_mode_param(mode) {
    var body_name = "";
    if ("get" == mode) {
        body_name = "edit_request_dlg_get_table_body";
    } else if ("post" == mode) {
        body_name = "edit_request_dlg_post_table_body";
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
    var data = get_request_data_from_ui();
    if (undefined == data["mode"]) {
        alert("Select Mode!");
        return;
    }

    if (data["url"].length == 0) {
        alert("Input Url")
        return;
    }

    var url = data["url"];
    url += "?";
    var first_param = true;
    $.each(data["get"],function(key,value) {
        var single = "";
        if (first_param) {
            single = key + "=" + value;
            first_param = false;
        } else {
            single = "&" + key + "=" + value;
        }
        url += single;
    })

    if (data["mode"] == "get") {
        window.open(url);
    } else if (data["mode"] == "post") {
        var post_params_info = new Object();
        post_params_info["url"] = base64_encode(url);
        post_params_info["post_data"] = base64_encode(JSON.stringify(data["post"]));
        var param_de = JSON.stringify(post_params_info);
        var param_en = base64_encode(param_de);
        var url_new = "request?action=post_data&param=" + param_en;
        window.open(url_new);
    }
}
