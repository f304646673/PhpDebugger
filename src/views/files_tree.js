/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


function files_tree_build() {
    $("#files_tree").empty();
    $('#files_tree').tree({
        url:'files_tree?action=build',
        //url:'/files/data.json',
        method:'get',
        loadFilter:lazeloadfilestree
    });
    function lazeloadfilestree(data, parent){
        var state = $.data(this, 'tree');

        function setData(){
            var serno = 1;
            var todo = [];
            for(var i=0; i<data.length; i++){
                todo.push(data[i]);
            }
            while(todo.length){
                var node = todo.shift();
                if (node.id == undefined){
                    node.id = '_node_' + (serno++);
                }
                if (node.children){
                    node.state = 'closed';
                    node.children1 = node.children;
                    node.children = undefined;
                    todo = todo.concat(node.children1);
                }
            }
            state.tdata = data;
        }
        function find(id){
            var data = state.tdata;
            var cc = [data];
            while(cc.length){
                var c = cc.shift();
                for(var i=0; i<c.length; i++){
                    var node = c[i];
                    if (node.id == id){
                        return node;
                    } else if (node.children1){
                        cc.push(node.children1);
                    }
                }
            }
            return null;
        }

        setData();

        var t = $(this);
        var opts = t.tree('options');
        opts.onBeforeExpand = function(node){
            var n = find(node.id);
            if (n.children && n.children.length){return}
            if (n.children1){
                var filter = opts.loadFilter;
                opts.loadFilter = function(data){return data;};
                t.tree('append',{
                    parent:node.target,
                    data:n.children1
                });
                opts.loadFilter = filter;
                n.children = n.children1;
            }
        };
        return data;
    }
    
    $('#files_tree').tree({
        onClick: function(node){
            if(!$('#files_tree').tree('isLeaf',node.target)) {
                $('#files_tree').tree(node.state === "closed" ? "expand" : "collapse", node.target);
            }
            else {
                openFiles(node.text, node.attributes.path, node.attributes.id);
                //alert(node.attributes.path);
            }
        }
    });
}

function floder_add_dlg_open() {
    $('#add_floder_dlg').dialog('open').dialog('center').dialog('setTitle','Add Floder');
    $('#add_floder_dlg_fm').form('clear');
}

function floder_add_dlg_close() {
    $('#add_floder_dlg_fm').form('clear');
    $('#add_floder_dlg').dialog('close');
}

function floder_add_request() {
    path = $('#add_floder_dlg_fm div .textbox .textbox-value').val();
    path_en = base64_encode(path);
    $.get("files_tree", {"action":"add", "param":path_en},
        function(data){
        console.log(data);
    }, "json");
    
    files_tree_build();
    $('#add_floder_dlg').dialog('close')
}

function floder_reload() {
    files_tree_build();
}

function floder_remove() {
    var node = $('#files_tree').tree('getSelected');
    if (node){
        path_en = base64_encode(node.attributes.path);
         $.get("files_tree", {"action":"remove", "param":path_en},
            function(data){
            console.log(data);
        }, "json");
    }
    files_tree_build();
}