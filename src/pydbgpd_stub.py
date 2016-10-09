# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os
import sys
import time
import base64
import platform
import threading
import subprocess
from threading import Thread
from socket_client import socket_client

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
        self._exc_cmd = "python pydbgpd_proxy.py"
        self._lock_excute = threading.Lock()
        self._cmd_client = socket_client()
        
    def _is_cmd_valid(self, cmd, cmd_list):
        for item in cmd_list:
            if cmd.startswith(item):
                return True
        return False
        
    def start(self):
        if (self._exc_cmd == None):
            raise NameError("exc_cmd is none")
        if "Windows" == platform.system():
            self._process = subprocess.Popen(self._exc_cmd, shell = False)
        else:
            self._process = subprocess.Popen(self._exc_cmd, shell = True,  preexec_fn = os.setpgrp)
        time.sleep(2)
        self._cmd_client.Start()
        
    def stop(self):
        self._cmd_client.Stop()
        
        if not self._process:
            raise NameError("subprocess is none")
        else:
            if "Windows" != platform.system():
                pid = self._process.pid
                pgid = os.getpgid(pid)
                os.kill(-pgid, 9)
            self._process.terminate()
            self._process.kill()
            self._process = None

    def is_session(self):
        self._lock_excute.acquire()
        is_session = self._is_session
        self._lock_excute.release()
        return is_session
    
    def query(self, query_cmd):
        data = ""
        if self._is_session:
            if not self._is_cmd_valid(query_cmd, self._session_cmd):
                return "invalid cmd"
        else:
            if not self._is_cmd_valid(query_cmd, self._no_session_cmd):
                return "invalid cmd"
        
        self._lock_excute.acquire()
        data = self._cmd_client.Query(query_cmd)
        self._lock_excute.release()
        
        if len(data) > 1:
            if data[-2] == "@":
                print "Switch to Session \n"
                self._is_session = True
            elif data[-2] == ":":
                self._is_session = False
                print "Switch to No Session \n"
            data = base64.b64decode(data[:-2])
            
        return data  


if __name__ == "__main__":
    sub = pydbgpd_stub()
    sub.start()
    while True:
        cmd = raw_input("CMD: ") 
        print sub.query(cmd)
        if "quitt" == cmd:
            break
    
    sub.stop()
    #return
        
    #print sub.query('help')
    #print "Key   " + sub.query('key netbeans-xdebug')
    #print "Listen   " + sub.query('listen -p 192.168.41.1:9000 start')
    #print "Listen   " + sub.query('listen -p localhost:9000 start')
    #print "Help   " + sub.query('help')
    #sub._listenData()
    
    #time.sleep(20)
