# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import sys
import time
import base64
import subprocess
import threading
from threading  import Thread

globe_signal = True

class pydbgpd_stub:
    
    _process = None
    _exc_cmd = ""
    _out_read_thread = None
    _write_ready = False
    _stop_thread = False
    _out_data = ""
    _is_session = False
    
    _session_cmd = [
        "spawnpoint_disable",
        "breakpoint_disable",
        "breakpoint_enable",
        "spawnpoint_remove",
        "breakpoint_remove",
        "spawnpoint_get",
        "breakpoint_get",
        "spawnpoint_set",
        "breakpoint_set",
        "property_value",
        "context_names",
        "property_get",
        "property_set",
        "stack_depth",
        "feature_get",
        "feature_set",
        "interactive",
        "context_get",
        "step over",
        "stack_get",
        "step out",
        "interact",
        "type_map",
        "threads",
        "step in",
        "status",
        "source",
        "select",
        "detach",
        "break",
        "help",
        "step",
        "stop",
        "eval",
        "exit",
        "run",]
        
    _no_session_cmd = [
        "errorlevel",
        "proxyinit",
        "proxystop",
        "sessions",
        "listen",
        "select",
        "help",
        "stop",
        "quit",
        "exit",
        "key",]
    
    def __init__(self):
        self._exc_cmd = "python -i pydbgpd_proxy.py"
        self._lock_excute = threading.Lock() 
        
    def _is_cmd_valid(self, cmd, cmd_list):
        for item in cmd_list:
            if cmd.startswith(item):
                return True
        return False
        
    def start(self):
        if (self._exc_cmd == None):
            raise NameError("exc_cmd is none")
        self._process = subprocess.Popen(self._exc_cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr =subprocess.STDOUT, shell = False)
        self._out_read_thread = Thread(target=self._read_stdout_thread)
        self._out_read_thread.daemon = True # thread dies with the program
        self._out_read_thread.start()
        data = self._listenData()
        return data
        
    def stop(self):
        if not self._out_read_thread:
            while self._out_read_thread.is_alive():
                self._stop_thread = True
                time.sleep(0.01)

            self._out_read_thread = None
        
        if not self._process:
            raise NameError("subprocess is none")
        else:
            self._process.terminate()
            self._process.kill()
            self._process = None

    def is_session(self):
        self._lock_excute.acquire()
        is_session = self._is_session
        self._lock_excute.release()
        return is_session
    
    def query(self, query_cmd):
        self._lock_excute.acquire()
        data = ""
        if self._is_session:
            if not self._is_cmd_valid(query_cmd, self._session_cmd):
                data = "invalid cmd"
        else:
            if not self._is_cmd_valid(query_cmd, self._no_session_cmd):
                data = "invalid cmd"
        
        if not len(data):
            self._query(query_cmd)
            data = self._listenData()
            data = data[:-1]
            
        self._lock_excute.release()
        return data
        
    def _query(self, query_cmd):
        if not self._process:
            raise NameError("subprocess is none")
        
        query_cmd += "\n"
        self._out_data = ""
        
        self._write_ready = False
        self._process.stdin.flush()
        self._process.stdin.write(query_cmd)
        self._write_ready = True
        
                
    def _listenData(self):
        self._write_ready = True
        while True:
            if self._stop_thread:
                break
            if len(self._out_data) > 0:
                ret = ""
                if self._out_data[-3] == "@":
                    ##print "Switch to Session \n"
                    self._is_session = True
                    try:
                        ret = base64.b64decode(self._out_data[:-3])
                    except Exception,errinfo:
                        print "_listenData Session error" + self._out_data + "\n"
                    return ret
                elif self._out_data[-3] == ":":
                    self._is_session = False
                    #print "Switch to No Session \n"
                    try:
                        ret = base64.b64decode(self._out_data[:-3])
                    except Exception,errinfo:
                        print "_listenData No Session error" + self._out_data + "\n"
                    return ret
            time.sleep(0.01) 
    
    def _read_stdout_thread(self):
        while True:
            if self._stop_thread:
                break
            if False == self._write_ready or not self._process:
                time.sleep(0.01) 
                continue
            line = self._process.stdout.readline()
            #print line
            if len(line) != 0:
                self._out_data = self._out_data + line
            
    
if __name__ == "__main__":
    sub = pydbgpd_stub()
    sub.start()
    sub.query('')
    print "Key   " + sub.query('key netbeans-xdebug')
    #print "Listen   " + sub.query('listen -p 192.168.41.1:9000 start')
    print "Listen   " + sub.query('listen -p localhost:9010 start')
    print "Help   " + sub.query('help')
    #sub._listenData()
    
    time.sleep(20)
    sub.stop()
