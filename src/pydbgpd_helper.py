# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import re
import os
import md5
import json
import base64
import math
from threading import Thread
from pydbgpd_stub import pydbgpd_stub
from debugger_exception import debugger_exception

class pydbgpd_helper:
    _pydbgpd = None
    _listening = False
    
    def __init__(self):
        self._context_names_pattern = re.compile("(\d+): (\w+)")
        self._stack_get_pattern = re.compile("frame: (\d+) (.+)\((\d+)\) file ([{\w}]+)")
        self._context_get_pattern = re.compile("name: (\$[\d\w_]+) type: (\w+) value: (.*)")
        self._sessions_info_pattern = re.compile("(\d+):<dbgp.server.application instance at 0x(.+)>")
        
    def _get_status(self):
        if self._pydbgpd.is_session():
            return self._pydbgpd.query('status')
        else:
            return self._pydbgpd.query('sessions')            

    def get_file_src(self):
        if False == self._pydbgpd.is_session():
            return ""
        src = self._pydbgpd.query('source')
        if "(u'stack depth invalid', 301)" in src:
            return ""
        return src
        
    def get_info(self):
        info = {}
        info["status"] = self._get_status()
        info["context"] = self._get_all_variables()
        info["stack"] = self._get_stack_info()
        return info
     
    def check_con(self, param): 
        self.select_first_conn()
        if self._pydbgpd.is_session():
            self._pydbgpd.query("step")
            return {"ret":1}
        else:
            return {"ret":0}

    def set_line_breakpoint(self, param):
        param_de = base64.b64decode(param)
        param_json = json.loads(param_de)
        lineno = param_json['lineno']
        filename = param_json['path']
        filename = base64.b64decode(filename)
        query = "breakpoint_set -t line -f " +  filename + " -n " + lineno
        #<dbgp.server.breakpoint: id:11900002 type:line filename:file:///var/www/html/index.php lineno:8 function: state:enabled exception: expression: temporary:0 hit_count:0 hit_value:None hit_condition:None>
        data = self._pydbgpd.query(query)
        pattern = re.compile("<dbgp.server.breakpoint: id:(\d+) type:(\w+) filename:(.+) lineno:(\d*) function:([\w\d_]*) state:(\w+) exception:([\w\d_]*) expression:(.*) temporary:(\d+) hit_count:(\d+) hit_value:([\w\d]+) hit_condition:([\w\d]+)>")
        try:
            res = pattern.search(data).groups()
            ret = 1
        except Exception,errinfo:
            print errinfo, "set_line_breakpoint error:" + data + "\n"
            ret = 0
        return {"ret":ret}
    
    def remove_line_breakpoint(self,param):
        param_de = base64.b64decode(param)
        param_json = json.loads(param_de)
        lineno = param_json['lineno']
        filename = param_json['path']
        filename = base64.b64decode(filename)
        params = {"filename":filename, "lineno":lineno}
        id = self._get_breakpoint_id('line', params)
        ret = 0
        if -1 <> id and None <> id:
            query = "breakpoint_remove -d " + str(id)
            q_ret = self._pydbgpd.query(query)
            if "breakpoint removed" in q_ret:
                ret = 1
        return {"ret":ret}
    
    def _get_breakpoint_id(self, type, param):
        data = self.breakpoint_list('')
        if type == "line":
            filename = param['filename']
            lineno = param['lineno']
            for item in data:
                if item['filename'] == filename and item['type'] == type and item['lineno'] == str(lineno):
                    return item['id']
        else:
            return -1 
        
    def get_last_frame_info(self,param):
        data = self._get_stack_info()
        if 0 == len(data):
            return {"ret":0}
        else:
            return {"ret":1, "data":data[0]}

####################################################################################   
    def do(self, action, param):
        actions = {"start_listen":self.start_listen,
                    "stop_listen":self.stop_listen,
                    "get_cur_stack_info":self.get_cur_stack_info,
                    
                    "run":self.run,
                    "step_over":self.step_over,
                    "step_in":self.step_in,
                    "step_out":self.step_out,
                    "get_variables":self.get_variables,
                    "stack_get":self.stack_get,
                    "add_breakpoint":self.add_breakpoint,
                    "remove_breakpoint":self.remove_breakpoint,
                    "source":self.source,
                    
                    "sessions":self.sessions,
                    "select":self.select,
                    "status":self.status,
                    "quit":self.quit,
                    "stop":self.stop,
                    "exit":self.exit,
                    
                    "set_line_breakpoint":self.set_line_breakpoint,
                    "remove_line_breakpoint":self.remove_line_breakpoint,
                    "select_first_session":self.check_con,
                    "get_last_frame_info":self.get_last_frame_info,
                    "breakpoint_list":self.breakpoint_list,
                    }
                    
        if not self._pydbgpd:
            return {"ret":0}
            
        return actions[action](param)
        
    def start_debugger(self):
        if self._pydbgpd:
            return {"ret":1}
        self._pydbgpd = pydbgpd_stub()
        self._pydbgpd.start()
        #self._pydbgpd.query('')
        self._pydbgpd.query('key netbeans-xdebug')
        #self._pydbgpd.query('listen -p 192.168.41.1:9000 start')

    def stop_debugger(self):
        if self._pydbgpd:
            self._pydbgpd.stop()
            del self._pydbgpd
            self._pydbgpd = None
            
    def is_session(self):
        if not self._pydbgpd:
            return False
        return self._pydbgpd.is_session()
    
##################################################################################################
    def query(self, cmd):
        return self._pydbgpd.query(cmd)
    
    def source(self,param):
        src = self._pydbgpd.query("source")
        if "(u'stack depth invalid', 301)" in src:
            return {"ret": 0}
        return {"ret": 1, "data": src}
    
    def add_breakpoint(self,breakpointinfo):
        #breakpoint_set_keys = ["type", "filename", "lineno", "function", "state", "exception", "expression", "temporary", "hit_count", "hit_value", "hit_condition"]
        breakpoint_set_type_keys = {
            "line" : {"filename":"-f","lineno":"-n"},
            "call" : {"function":"-m"},
            "return" : {"function":"-m"},
            "exception" : {"exception":"-x"},
            "conditional" : {"filename":"-f","lineno":"-n","expression":"-c"},
            "watch" : {},
        }
        
        query = "breakpoint_set -t " + breakpointinfo["type"]
        for (key,value) in breakpoint_set_type_keys[breakpointinfo["type"]].items():
            if value == "-c":
                expression_de = base64.b64decode(breakpointinfo[key])
                query = query + " " + value + " '" + expression_de + " '"       #maybe bug if expression_de has '
            else:
                query = query + " " + value + " " + breakpointinfo[key]

        data = self._pydbgpd.query(query)
        iteminfo = self._parse_breakpoint_info(data)
        if not iteminfo:
            ret = 0
        else:
            ret = 1
        return {"ret":ret, "breakpoint":iteminfo}
    
    def remove_breakpoint(self,breakpointid):
        query = "breakpoint_remove -d " + breakpointid
        data = self._pydbgpd.query(query)
        if "breakpoint removed" in data:
            ret = 1
        else:
            ret = 0
        return {"ret":ret}
  
    def start_listen(self, param):
        if False == self._listening:
            data = self._pydbgpd.query('listen -p localhost:9000 start')
            #ERROR: dbgp.server: the debugger could not bind on port 9000.
            if "ERROR" in data:
                return {"ret":0}
            self._listening = True
        return {"ret":1}
    
    def stop_listen(self, param):
        if True == self._listening:
            data = self._pydbgpd.query('listen stop')
            if 0 != len(data):
                return {"ret":0}
            self._listening = False
        return {"ret":1}
    
    def get_cur_stack_info(self,param):
        data = self._get_stack_info("0")
        if 0 == len(data):
            return {"ret":0}
        else:
            return {"ret":1, "data":data[0]}
        
    def breakpoint_list(self, param):
        data = self._pydbgpd.query("breakpoint_list")
        #data ="""<dbgp.server.breakpoint: id:11900002 type:line filename:file:///var/www/html/index.php lineno:8 function: state:enabled exception: expression: temporary:0 hit_count:0 hit_value:None hit_condition:None>
#<dbgp.server.breakpoint: id:11900003 type:line filename:file:///var/www/html/index.php lineno:9 function: state:enabled exception: expression: temporary:0 hit_count:0 hit_value:None hit_condition:None>"""
        info = []
        arr = data.split('\n') 
        
        for item in arr:
            if not len(item):
                continue
            iteminfo = self._parse_breakpoint_info(item)
            if iteminfo:
                info.append(iteminfo)
        return info
    
    def _parse_breakpoint_info(self, info):
        iteminfo = {}
        try:
            iteminfo = self.parse_breakpoint_info(info)
        except Exception,errinfo:
            print errinfo, "_parse_breakpoint_info error:" + info + "\n"
        return iteminfo
    
    def get_variables(self,param):
        return self._get_all_variables()
    
    def step_over(self, param):
        return self._step_cmd("step over")
    
    def step_in(self, param):
        return self._step_cmd("step in")
    
    def step_out(self, param):
        return self._step_cmd("step out")
    
    def run(self, param):
        return self._step_cmd("run")
    
    def _step_cmd(self,cmd):
        if False == self._pydbgpd.is_session():
            return {}
        data = self._pydbgpd.query(cmd)
        if len(data):
            return {"ret":0}
        else:
            return {"ret":1}
        
    def stack_get(self,param):
        return {"ret":1, "data":self._get_stack_info()}
    
    def _get_stack_info(self, frame = ""):
        if False == self._pydbgpd.is_session():
            return []
        query = 'stack_get ' + frame
        data = self._pydbgpd.query(query)
        #data = "frame: 0 file:///var/www/html/index.php(8) file {main}"
        
        frame_list = []
        arr = data.split('\n')
        
        for item in arr:
            if not len(item):
                continue
            try:
                res = self._stack_get_pattern.search(item).groups()
                info = {}
                info['frame'] = res[0]
                info['filename'] = res[1]
                #info['path'] = info['path'].replace('/', os.sep)
                info['filename_last'] = info['filename'].split('/')[-1]
                info['lineno'] = res[2]
                info['function'] = res[3]
                m1 = md5.new()   
                m1.update(info['filename']) 
                info['file_id'] = m1.hexdigest()
                frame_list.append(info)
            except Exception,errinfo:
                print errinfo, "stack_get error:" + data + "\n"
                
        return frame_list
    
    #0 out of session 1 starting 2 break 3 stopping 4 stopped 5 waiting
    def status(self,param):
        if not self._pydbgpd.is_session():
            return {"ret":1, "status":0}
        
        data = self._pydbgpd.query('status')
        out_of_sesion_status = "invalid cmd"
        starting_status = "Current Status: status [starting] reason[ok]"
        break_status = "Current Status: status [break] reason[ok]"
        stopping_status = "Current Status: status [stopping] reason[ok]"
        stopped_status =  "command sent after session stopped"
        waiting_status = "session timed out while waiting for response"
        
        status = -1
        
        status_map = {
            out_of_sesion_status:0,
            starting_status:1,
            break_status:2,
            stopping_status:3,
            stopped_status:4,
            waiting_status:5 };
            
        for (key,value) in status_map.items():
            if key in data:
                status = value
                break
                
        if not len(data):
            status = 0
            
        return {"ret":1,"status":status}
    
    def quit(self,param):
        return self._step_cmd("quit")
    
    def stop(self,param):
        return self._step_cmd("stop")
    
    def exit(self,param):
        return self._step_cmd("exit")    
           
    #2344:<dbgp.server.application instance at 0x025839E0>
    def select_first_conn(self):
        if self._pydbgpd.is_session():
            return "None"
        else:
            data = self._pydbgpd.query('sessions')
            #data = "#2344:<dbgp.server.application instance at 0x025839E0>"
            if len(data) == 0:
                return "None"
            pattern = re.compile("(\d+):<dbgp.server.application instance at 0x(.+)>")
            res = pattern.search(data).groups()
            select_cmd = "select " + res[0]
            ret = self._pydbgpd.query(select_cmd)
            return ret
    
    def sessions(self,param):
        data = self._pydbgpd.query('sessions')
        sessions = []
        arr = data.split('\n')
        #data = "#2344:<dbgp.server.application instance at 0x025839E0>"
        for item in arr:
           try:
               if not len(item):
                   continue
               res = self._sessions_info_pattern.search(item).groups()
               sessions.append(res[0])
           except Exception,errinfo:
               print errinfo, "sessions error:" + data + "\n"
                
        return sessions
    
    def select(self,param):
        select_cmd = "select " + param
        ret = self._pydbgpd.query(select_cmd)
        if self.is_session():
            return {"ret":1}
        return {"ret":0}
    
    def _get_all_variables(self):
        all_data = self._get_stack_variables()
        return {"ret":1, "data":all_data}
    
    def _get_context_variables(self, depth_id):
        data = self._pydbgpd.query('context_names')
#data='''0: Locals
#1: Superglobals
#2: User defined constants'''
        
        info = {}
        arr = data.split('\n')
                
        for item in arr:
            if not len(item):
                continue
            try:
                res = self._context_names_pattern.search(item).groups()
                iteminfo = self._get_context(depth_id, res[0])
                info[res[1]] = iteminfo
            except Exception,errinfo:
                print errinfo, "context_names error:" + item + "\n"
        
        return info
    
    def _get_stack_variables(self):
        info = {}
        data = self._pydbgpd.query('stack_depth')
        #'Stack Depth: 3'
        pattern = re.compile("Stack Depth: (\d+)")
        try:
            res = pattern.search(data).groups()
            for index in range(0, int(res[0])):
                iteminfo = self._get_context_variables(index)
                key = "Frame " + str(index)
                info[key] = iteminfo
        except Exception,errinfo:
            print errinfo, "_get_stack_variables error:" + data + "\n"
            
        return info
            
    def _get_context(self, depth_id, context_id):
        query = 'context_get -d ' + str(depth_id) + ' -c ' + str(context_id)
            
        data = self._pydbgpd.query(query)
        #data = '''name: $a type: string value: 123
#name: $b type: int value: 234'''

        info = []
        arr = data.split('\n')
        
        for item in arr:
            if not len(item):
                continue
            try:
                res = self._context_get_pattern.search(item).groups()
                iteminfo = {}
                iteminfo["name"] = res[0]
                iteminfo["type"] = res[1]
                iteminfo["value"] = res[2]
                info.append(iteminfo)
            except Exception,errinfo:
                print errinfo, "context_get error:" + item + "\n"
                
        return info    
    
    #data = "<dbgp.server.breakpoint: id:65920004 type:conditional filename:file:///D:/nginx-1.11.3/html/index.php lineno:30 function: state:enabled exception: expression:$i ==6 temporary:0 hit_count:0 hit_value:None hit_condition:None>"
    def parse_breakpoint_info(self, data):
        breakpoint_info = {}
        keys = ["id","type","filename","lineno","function","state","exception","expression","temporary","hit_count","hit_value","hit_condition"]
        data_end = data.rfind(">")
        for key_index in range(0, len(keys)):
            search_key = " " + keys[key_index] + ":"
            index_start = data.find(search_key) + len(search_key)
            if -1 == index_start:
                raise debugger_exception("parse_breakpoint_info error: no keys" + keys[key_index] )
            if key_index < len(keys) - 1:
                next_key_index = key_index + 1
                search_key = " " + keys[next_key_index] + ":"
                index_end = data.find(search_key)
                if -1 == index_end:
                    raise debugger_exception("parse_breakpoint_info error: no keys" + keys[index_end] )
            else:
                index_end = data_end
            breakpoint_info[keys[key_index]] = data[index_start:index_end]
        return breakpoint_info
    
if __name__ == "__main__":
    pass
    #sub = pydbgpd_helper()
    #sub.start()
    #sub.select_first_conn()
    #sub._get_stack_info()
    #sub.breakpoint_list()
    #print sub.remove_line_breakpoint(8)
