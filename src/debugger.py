# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import time
import json
import base64
import md5
from threading import Thread
from pydbgpd_helper import pydbgpd_helper

class debugger_exception(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class debugger:
    
    _breakpoint_list = {}
    _debugger_helper = None
    _status = -1                 #-1 Uninit 0 Init 1 Listen 2 debug
    _debug_thread = None
    _debug_stop_signal = False
    
    _breakpoint_type_keys = {
        "line" : ["filename","lineno","type"],
        "call" : ["function","type"],
        "return" : ["function","type"],
        "exception" : ["exception","type"],
        "conditional" : ["conditional","type"],
        "watch" : [],
    }
        
    def __init__(self):
        pass
        
    def __del__(self):
        pass
    
    def do(self, action, param):
        
        actions = {"get_debugger_status":[self.get_debugger_status, "json", False],
                    "start_listen":[self.start_listen, "json", True],
                    "stop_listen":[self.stop_listen, "json", True],
                    "select_first_session":[self.select_first_session, "json", True],
                    "get_cur_stack_info":[self.get_cur_stack_info, "json", True],
                    "query":[self.query, "json", True],
                    "breakpoint_list":[self.breakpoint_list, "json", False],
                    "add_breakpoint":[self.add_breakpoint, "json", False],
                    "remove_breakpoint":[self.remove_breakpoint, "json", False],
                    #"set_line_breakpoint":[self.set_line_breakpoint, "json"],
                    #"remove_line_breakpoint":[self.remove_line_breakpoint, "json"],
                    #"check_con":[self.check_con, "json"],
                    "step_over":[self.step_over, "json", True],
                    "step_in":[self.step_in, "json", True],
                    "step_out":[self.step_out, "json", True],
                    "run":[self.run, "json", True],
                    #"get_last_frame_info":[self.get_last_frame_info, "json"],
                    #"source":[self.source, "json"],
                    "get_variables":[self.get_variables, "json", True],
                    "stack_get":[self.stack_get, "json", True],
                    "get_file_line_breakpoint_lineno":[self.get_file_line_breakpoint_lineno, "json", True],
                    "start_debug":[self.start_debug, "json", False],
                    "stop_debug":[self.stop_debug, "json", False],
                    }
                    
        if action not in actions.keys():
            raise debugger_exception("action:" + action + " is invalid")
        
        if False == isinstance(param,basestring):
            raise debugger_exception("param is invalid")
        
        if actions[action][2]:
            if not self._debugger_helper:
                return ({"ret":0}, "json")
        
        return (actions[action][0](param), actions[action][1])
  
    def get_debugger_status(self,param):
        if not self._debugger_helper:
            return {"ret":0}
        return self._debugger_helper.do("status","")
  
    def start_debug(self,param):
        self._reset_all_breakpoint()
        
        if not self._debugger_helper:
            self._debugger_helper = pydbgpd_helper()
            self._debugger_helper.start_debugger()
            listen_ret = self._debugger_helper.do("start_listen", "")
            if listen_ret["ret"] == 0:
                return {"ret" :0}
        
        if not self._debug_thread:
            self._debug_stop_signal = False
            self._debug_thread = Thread(target=self._debug_routine)
            self._debug_thread.daemon = True # thread dies with the program
            self._debug_thread.start()
        return {"ret" :1}
            
    def stop_debug(self,param):
        if self._debug_thread:
            while self._debug_thread.is_alive():
                self._debug_stop_signal = True
                time.sleep(0.5)
            self._debug_thread = None
        
        if self._debugger_helper:
            self._debugger_helper.stop_debugger()
            del self._debugger_helper
            self._debugger_helper = None
     
        self._reset_all_breakpoint()
        return {"ret" :1}
  
    def _reset_all_breakpoint(self):
        for breakpoint_key in self._breakpoint_list.keys():
            if self._breakpoint_list[breakpoint_key]["type"] not in self._breakpoint_type_keys.keys():
                del self._breakpoint_list[breakpoint_key]
                continue
            
            for key in self._breakpoint_list[breakpoint_key].keys():
                if key not in self._breakpoint_type_keys[self._breakpoint_list[breakpoint_key]["type"]]:
                    del self._breakpoint_list[breakpoint_key][key]
                
            self._breakpoint_list[breakpoint_key]["state"] = "disable"
    
    def _add_all_breakpoint(self):
        for (breakpoint_key,breakpoint_value) in self._breakpoint_list.items():
            add_ret = self._debugger_helper.do("add_breakpoint", breakpoint_value)
            if add_ret["ret"] == 1:
                self._breakpoint_list[breakpoint_key] = add_ret["breakpoint"]
            
    def _debug_routine(self):
        while False == self._debug_stop_signal:
            time.sleep(0.5)
            sessions = self._debugger_helper.do("sessions", "")
            for session_id in sessions:
                self._debug_session(session_id)
                if self._debug_stop_signal:
                    break
        self._debugger_helper.do("quit","")
        self._reset_all_breakpoint()
                
    def _debug_session(self,session_id):
        select_ret = self._debugger_helper.do("select", session_id)
        if select_ret["ret"] == 0:
            print "select error"
            return
        self._reset_all_breakpoint()
        self._add_all_breakpoint()
        if len(self._breakpoint_list):
            self._debugger_helper.do("run","")
        else:
            self._debugger_helper.do("step_over","")

        status_ret = self._debugger_helper.do("status","")
        while True:
            if self._debug_stop_signal:
                break
            if status_ret["ret"] == 0:
                break
            if status_ret["status"] == 3:
                self._debugger_helper.do("run","")
            if status_ret["status"] == 4:
                break
            time.sleep(0.5)
            status_ret = self._debugger_helper.do("status","")
            
        if status_ret["status"] != 0:
            self._debugger_helper.do("exit","")

    def start_listen(self,param):
        ret = self._debugger_helper.do("start_listen", param)
        if ret["ret"] == 1:
            self._status = 1
        return ret
    
    def stop_listen(self,param):
        ret =  self._debugger_helper.do("stop_listen", param)
        if ret["ret"] == 1:
            self._status = 0
        return ret
    
    def query(self,param):
        param_de = base64.b64decode(param)
        param_json = json.loads(param_de)
        if "cmd" not in param_json.keys():
            raise debugger_exception("query cmd is needed");
        return self._debugger_helper.query(param_json["cmd"])
  
    def _generate_breakpoint_key(self,breakpoint_info):
        if "type" not in breakpoint_info.keys():
            raise debugger_exception("_generate_breakpoint_key param error: no type");
        
        if breakpoint_info["type"] not in self._breakpoint_type_keys.keys():
            raise debugger_exception("_generate_breakpoint_key param error: type[" + breakpoint_info["type"] + "] is invalid");
        
        breakpoint_info_key = ""
        for item in self._breakpoint_type_keys[breakpoint_info["type"]]:
            breakpoint_info_key = breakpoint_info_key + item + ":" + breakpoint_info[item] + " "
        
        m1 = md5.new()   
        m1.update(breakpoint_info_key)
        return m1.hexdigest()

    def _get_breakpoint_info(self,param_json):
        if "type" not in param_json.keys():
            raise debugger_exception("_get_breakpoint_info param error: no type");
        
        if param_json["type"] not in self._breakpoint_type_keys.keys():
            raise debugger_exception("_get_breakpoint_info param error: type[" + param_json["type"] + "] is invalid");

        breakpoint_info = {}
        for item in self._breakpoint_type_keys[param_json["type"]]:
            if (item == "filename"):
                breakpoint_info[item] = base64.b64decode(param_json[item]) 
            else:
                breakpoint_info[item] = param_json[item]
        breakpoint_info_key = self._generate_breakpoint_key(breakpoint_info)
        return (breakpoint_info_key, breakpoint_info)

    def add_breakpoint(self,param):
        param_de = base64.b64decode(param)
        param_json = json.loads(param_de)
        (breakpoint_key, breakpoint_value) = self._get_breakpoint_info(param_json)
        #breakpoint_set_keys = ["type", "filename", "lineno", "function", "state", "exception", "expression", "temporary", "hit_count", "hit_value", "hit_condition"]
        if self._debugger_helper and self._debugger_helper.is_session():
            if breakpoint_key not in self._breakpoint_list.keys():
                add_ret = self._debugger_helper.do("add_breakpoint", breakpoint_value)
                if add_ret["ret"] == 1:
                    self._breakpoint_list[breakpoint_key] = add_ret["breakpoint"]
                    return {"ret":1}
                else:
                    return {"ret":0}
        else:
            self._breakpoint_list[breakpoint_key] = breakpoint_value
            self._breakpoint_list[breakpoint_key]["state"] = "disable"
        return {"ret":1}
        
    def remove_breakpoint(self,param):
        param_de = base64.b64decode(param)
        param_json = json.loads(param_de)
        (breakpoint_key, breakpoint_value) = self._get_breakpoint_info(param_json)
        if self._debugger_helper and self._debugger_helper.is_session():
            if breakpoint_key not in self._breakpoint_list.keys():
                remove_ret = self._debugger_helper.do("add_breakpoint", breakpoint_value["id"])
                if remove_ret["ret"] == 1:
                    del self._breakpoint_list[breakpoint_key]
                    return {"ret":1}
                else:
                    return {"ret":0}
        else:
            del self._breakpoint_list[breakpoint_key]
            
        return {"ret":1}
    
    def modify_breakpoint(self):
        for (key, value) in self._breakpoint_list.items():
            add_ret = self._debugger_helper.do("add_breakpoint", value)
            if add_ret["ret"] == 1:
                del self._breakpoint_list[key]
                self._breakpoint_list[key] = add_ret["breakpoint"]
            else:
                self._breakpoint_list[key]["state"] = "disable"
    
    def select_first_session(self,param):
        ret = self._debugger_helper.do("select_first_session", param)
        if ret["ret"] == 1:
            self.modify_breakpoint()
            self._status = 2
        return ret
    
    def get_cur_stack_info(self,param):
        return self._debugger_helper.do("get_cur_stack_info", param)
        
    def step_over(self,param):
        return self._debugger_helper.do("step_over", param)
    
    def step_in(self,param):
       return self._debugger_helper.do("step_in", param)   

    def step_out(self,param):
       return self._debugger_helper.do("step_out", param)
   
    def run(self,param):
       return self._debugger_helper.do("run", param)
    
    def stack_get(self,param):
        return self._debugger_helper.do("stack_get", param)
    
    def get_variables(self,param):
        return self._debugger_helper.do("get_variables", param)

    def breakpoint_list(self,param):
        breakpoint_list_info = []
        for (key,value) in self._breakpoint_list.items():
            item = value
            item["itemid"] = key
            breakpoint_list_info.append(item)
        return breakpoint_list_info
    
    def get_file_line_breakpoint_lineno(self,param):
        breakpoint_list_lineno = []
        for (key,value) in self._breakpoint_list.items():
            breakpoint_list_lineno.append(value["lineno"])
        return {"ret":1, "breakpoint_list_lineno":breakpoint_list_lineno}
    
def test_no_action():
    d = debugger()
    d.do("no_action", "")
    
def test_param_invalid():
    d = debugger()
    d.do("add_breakpoint", [])

def test_add_breakpoint_no_type():
    param = {"line":1}
    param_en = base64.b64encode(json.dumps(param))
    d = debugger()
    d.do("add_breakpoint", param_en)

def test_add_breakpoint_type_invalid():
    param = {"type": "no type","line":1}
    param_en = base64.b64encode(json.dumps(param))
    d = debugger()
    d.do("add_breakpoint", param_en)
    
def run_error(f):
    try:
        eval(f)()
    except debugger_exception as e:
        return True
        #print e.value
    return False

if __name__ == "__main__":
    error_handles = ["test_no_action", "test_param_invalid", "test_add_breakpoint_no_type", "test_add_breakpoint_type_invalid"]
    for item in error_handles:
        if False == run_error(item):
            print item + "run error"