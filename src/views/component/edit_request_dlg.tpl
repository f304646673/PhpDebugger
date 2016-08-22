<div id="edit_request_dlg" class="easyui-dialog" style="width:600px;height:800px;padding:10px 20px"
    closed="true" buttons="#save_request_dlg_buttons" data-options="iconCls:'icon-save-request',resizable:false,modal:true">
    <input id="edit_request_dlg_request_name" type="text" hidden="true" value=""></imput>
    <div class="easyui-panel" style="width:100%;heigth:100%;">
        <div class="easyui-accordion" style="width:100%;heigth:100%">
            <div title="Action" data-options="collapsed:false,collapsible:false" style="height:100px;">
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
                                <input id="edit_request_dlg_url_input" class="easyui-textbox" data-options="prompt:'Input Url...'" style="width:100%;height:100%;" multiline="true">
                            </td>
                        </tr>
                        <tr>
                            <td>Mode</td>
                            <td>
                                <input id="edit_request_dlg_post_mode_radio" type="radio" name="mode" value="post">Post</input>
                            </td>
                            <td>
                                <input id="edit_request_dlg_get_mode_radio" type="radio" name="mode" value="get">Get</input>
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
                        <th style="width:80%;height:20px;">Param Value</th>
                        <th style="width:10%;height:20px;">Action</th>
                    </tr>
                    <tbody id="edit_request_dlg_get_table_body">

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
                            <th style="width:80%;height:20px;">Param Value</th>
                            <th style="width:10%;height:20px;">Action</th>
                        </tr>
                    </tbody>
                    <tbody id="edit_request_dlg_post_table_body">

                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
