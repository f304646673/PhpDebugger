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
