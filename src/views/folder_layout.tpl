<div id="folder_layout" title="Folders" style="width:15%;min-width:200px" data-options="region:'west',iconCls:'icon-folder',split:true,tools:[{
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
