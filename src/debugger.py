# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import time
import json
import base64
import md5
import threading
from threading import Thread

from request_db import request_db
from pydbgpd_helper import pydbgpd_helper
from debugger_exception import debugger_exception

class debugger:
    
    _breakpoint_list = {}
    _debugger_helper = None
    _status = -1                 #-1 Uninit 0 Init 1 Listen 2 debug
    _debug_thread = None
    
    _accept_user_action_event = None
    _state_machine_stop_event = None
    
    _pre_variables = {}
    _cur_variables = {}
    
    _breakpoint_type_keys = {
        "line" : ["filename","lineno","type"],
        "call" : ["function","type"],
        "return" : ["function","type"],
        "exception" : ["exception","type"],
        "conditional" : ["filename","lineno","expression","type"],
        "watch" : [],
    }
        
    def __init__(self):
        self._state_machine_stop_event = threading.Event()
        self._state_machine_stop_event.clear()
        self._accept_user_action_event = threading.Event()
        self._accept_user_action_event.set()
        pass
        
    def __del__(self):
        pass
    
    def do(self, action, param):
        actions = {"run":[self.run, "json", True, True],
                    "query":[self.query, "json", True, True],
                    "step_in":[self.step_in, "json", True, True],
                    "step_out":[self.step_out, "json", True, True],
                    "step_over":[self.step_over, "json", True, True],
                    "stack_get":[self.stack_get, "json", True, True],
                    "save_request":[self.save_request, "json", True, True],
                    "get_variables":[self.get_variables, "json", True, True],
                    "modify_variable":[self.modify_variable, "json", True, True],
                    "get_cur_stack_info":[self.get_cur_stack_info, "json", True, True],
                    "get_variable_watch":[self.get_variable_watch, "json", True, True],
                    "select_first_session":[self.select_first_session, "json", True, True],
                    
                    "stop_debug":[self.stop_debug, "json", False, False],
                    "start_debug":[self.start_debug, "json", False, False],
                    "breakpoint_list":[self.breakpoint_list, "json", False, False],
                    "get_debugger_status":[self.get_debugger_status, "json", False, False],
                    "get_file_breakpoint_lineno":[self.get_file_breakpoint_lineno, "json", False, False],
                    
                    "add_breakpoint":[self.add_breakpoint, "json", False, True],
                    "remove_breakpoint":[self.remove_breakpoint, "json", False, True],
                    }
                    
        if action not in actions.keys():
            raise debugger_exception("action:" + action + " is invalid")
        
        if False == isinstance(param,basestring):
            raise debugger_exception("param is invalid")
        
        if actions[action][3] and False == self._accept_user_action_event.isSet():
            return ({"ret":0}, "json")
        
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
            self._state_machine_stop_event.clear()
            self._debug_thread = Thread(target=self._debug_routine)
            self._debug_thread.daemon = True # thread dies with the program
            self._debug_thread.start()
        return {"ret" :1}
            
    def stop_debug(self,param):
        if self._debug_thread:
            while self._debug_thread.is_alive():
                self._state_machine_stop_event.set()
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
        update_keys = ["id", "state", "hit_value", "hit_condition", "hit_count"]
        for (breakpoint_key,breakpoint_value) in self._breakpoint_list.items():
            add_ret = self._debugger_helper.do("add_breakpoint", breakpoint_value)
            if add_ret["ret"] == 1:
                for item in update_keys:
                        if item in add_ret["breakpoint"].keys():
                            self._breakpoint_list[breakpoint_key][item] = add_ret["breakpoint"][item]
            
    def _debug_routine(self):
        while False == self._state_machine_stop_event.isSet():
            time.sleep(0.5)
            sessions = self._debugger_helper.do("sessions", "")
            for session_id in sessions:
                self._debug_session(session_id)
                if self._state_machine_stop_event.isSet():
                    break
        self._debugger_helper.do("quit","")
        self._reset_all_breakpoint()
                
    def _debug_session(self,session_id):
        select_ret = self._debugger_helper.do("select", session_id)
        if select_ret["ret"] == 0:
            print "select error"
            return
        
        self._accept_user_action_event.clear()
        self._reset_all_breakpoint()
        self._add_all_breakpoint()

        status_ret = self._debugger_helper.do("status","")
        while False == self._state_machine_stop_event.isSet():
            if status_ret["ret"] == 0:
                break
            if status_ret["status"] == 1:
                self._accept_user_action_event.set()
                if len(self._breakpoint_list):
                    self._debugger_helper.do("run","")
                else:
                    self._debugger_helper.do("step_over","")
            if status_ret["status"] == 2:
                self._accept_user_action_event.set()
            if status_ret["status"] == 3:
                self._accept_user_action_event.clear()
                self._debugger_helper.do("run","")
            if status_ret["status"] == 4:
                self._accept_user_action_event.clear()
                break
            status_ret = self._debugger_helper.do("status","")
        
        if status_ret["status"] != 0:
            self._debugger_helper.do("exit","")
        self._pre_variables = {}
        self._cur_variables = {}
        
        self._accept_user_action_event.set()
    
    def query(self,param):
        param_de = base64.b64decode(param)
        param_json = json.loads(param_de)
        if "cmd" not in param_json.keys():
            raise debugger_exception("query cmd is needed");
        return self._debugger_helper.query(base64.b64decode(param_json["cmd"]))
  
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
        update_keys = ["id", "state", "hit_value", "hit_condition", "hit_count"]
        param_de = base64.b64decode(param)
        param_json = json.loads(param_de)
        (breakpoint_key, breakpoint_value) = self._get_breakpoint_info(param_json)
        #breakpoint_set_keys = ["type", "filename", "lineno", "function", "state", "exception", "expression", "temporary", "hit_count", "hit_value", "hit_condition"]
        
        if breakpoint_key not in self._breakpoint_list.keys():
            self._breakpoint_list[breakpoint_key] = breakpoint_value
            self._breakpoint_list[breakpoint_key]["state"] = "disable"
            if self._debugger_helper and self._debugger_helper.is_session():
                add_ret = self._debugger_helper.do("add_breakpoint", breakpoint_value)
                print add_ret
                if add_ret["ret"] == 1:
                    for item in update_keys:
                        if item in add_ret["breakpoint"].keys():
                            self._breakpoint_list[breakpoint_key][item] = add_ret["breakpoint"][item]
                    return {"ret":1}
                else:
                    return {"ret":0}
        return {"ret":1}
        
    def get_breakpoint_info_by_param(self,param_json):
        breakpoint_key = ""
        breakpoint_value = {}
        if "itemid" in param_json.keys():
            breakpoint_key = param_json["itemid"]
            if breakpoint_key in self._breakpoint_list.keys():
                breakpoint_value = self._breakpoint_list[breakpoint_key]
        else:
            (breakpoint_key, breakpoint_value_t) = self._get_breakpoint_info(param_json)
            if breakpoint_key in self._breakpoint_list.keys():
                breakpoint_value = self._breakpoint_list[breakpoint_key]
        return (breakpoint_key,breakpoint_value)
            
    def remove_breakpoint(self,param):
        param_de = base64.b64decode(param)
        param_json = json.loads(param_de)
        print self._breakpoint_list
        (breakpoint_key, breakpoint_value) = self.get_breakpoint_info_by_param(param_json)
        print breakpoint_key, breakpoint_value
        if self._debugger_helper and self._debugger_helper.is_session():
            if breakpoint_key in self._breakpoint_list.keys():
                remove_ret = self._debugger_helper.do("remove_breakpoint", breakpoint_value["id"])
                if remove_ret["ret"] == 1:
                    del self._breakpoint_list[breakpoint_key]
                    return {"ret":1}
                else:
                    return {"ret":0}
        else:
            if breakpoint_key in self._breakpoint_list.keys():
                del self._breakpoint_list[breakpoint_key]
            
        return {"ret":1}
    
    def modify_breakpoint(self):
        update_keys = ["id", "state", "hit_value", "hit_condition", "hit_count"]
        for (key, value) in self._breakpoint_list.items():
            add_ret = self._debugger_helper.do("add_breakpoint", value)
            if add_ret["ret"] == 1:
                for item in update_keys:
                    if item in add_ret["breakpoint"].keys():
                        self._breakpoint_list[key][item] = add_ret["breakpoint"][item]
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
        self._pre_variables = self.get_variables("")
        ret = self._debugger_helper.do("step_over", param)
        self._cur_variables = self.get_variables("")
        return ret
    
    def step_in(self,param):
        self._pre_variables = self.get_variables("")
        ret = self._debugger_helper.do("step_in", param)
        self._cur_variables = self.get_variables("")
        return ret

    def step_out(self,param):
        self._pre_variables = self.get_variables("")
        ret = self._debugger_helper.do("step_out", param)
        self._cur_variables = self.get_variables("")
        return ret
   
    def run(self,param):
        self._pre_variables = self.get_variables("")
        ret = self._debugger_helper.do("run", param)
        self._cur_variables = self.get_variables("")
        return ret
    
    def get_variable_watch(self,param):
        param_de = base64.b64decode(param)
        pre_data = self._search_variable(self._pre_variables, param_de)
        cur_data = self._search_variable(self._cur_variables, param_de)
        m1 = md5.new()   
        m1.update(param_de)
        id = m1.hexdigest()
        new_data = {"pre":pre_data,"cur":cur_data}
        return {"ret":1, "id":id, "name":param_de, "data":new_data}
    
    def _search_variable(self,data,name):
        if "ret" not in data.keys():
            return {"type":'uninitialized', "value":"",'name':name}
        if "data" not in data.keys():
            return {"type":'uninitialized', "value":"",'name':name}
        if data["ret"] == 0:
            return {"type":'uninitialized', "value":"",'name':name}
        for (itemk,itemv) in data["data"].items():
            for (itemkk,itemvv) in itemv.items():
                for item in itemvv:
                    if item["name"] == name:
                        return item

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
    
    def get_file_breakpoint_lineno(self,param):
        param_de = base64.b64decode(param)
        param_json = json.loads(param_de)
        if "filename" not in param_json.keys():
            raise debugger_exception("param is invalid")
        
        breakpoint_list_lineno = []
        for (key,value) in self._breakpoint_list.items():
            if "filename" not in value.keys():
                continue
            if param_json["filename"] != value["filename"]:
                continue
            if "lineno" in value.keys():
                breakpoint_list_lineno.append(value["lineno"])
        return {"ret":1, "breakpoint_list_lineno":breakpoint_list_lineno}
    
    def modify_variable(self,param):
        param_de = base64.b64decode(param)
        param_json = json.loads(param_de)
        if "value" not in param_json.keys() or "name" not in param_json.keys():
            return {"ret":0}
        exucte_cmd = param_json["name"] + "=" + base64.b64decode(param_json["value"])
        print exucte_cmd
        data = self._debugger_helper.do("eval", exucte_cmd)
        return data
    
    def save_request(self,param):
        param_de = base64.b64decode(param)
        db = request_db()
        if db.is_request_name_exist(param_de):
            return {"ret":0, "msg":"name exist"}
        
        variables = self.get_variables("")
        get_data_org = self._search_variable(variables, "$_GET")
        post_data_org = self._search_variable(variables, "$_POST")
        
        get_data_new = {}
        if "value" in get_data_org.keys():
            get_data_new = self.generate_get_request_map(get_data_org["value"], "$_GET['", "']")
            
        post_data_new = {}
        if "value" in post_data_org.keys():
            post_data_new = self.generate_get_request_map(post_data_org["value"], "$_POST['", "']")
        
        all_data = {"get":get_data_new, "post":post_data_new, "url":""}
        db.add_request(param_de, all_data)
        return {"ret":1}

    def generate_get_request_map(self, data, start, end):
        json_data = json.loads(data)
        new_data = {}
        for (key,value) in json_data.items():
            real_key = self._get_full_name_varaibles_short_name(key, start, end)
            if len(real_key):
                new_data[real_key] = value
        return new_data

    def _get_full_name_varaibles_short_name(self, data, start, end):
        index = data.find(start)
        if  -1 == index:
            return ""
        index = index + len(start)

        finish = data.rfind(end)
        if -1 == finish:
            finish = len(data)
        return data[index:finish]
    
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