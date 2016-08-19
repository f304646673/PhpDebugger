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
