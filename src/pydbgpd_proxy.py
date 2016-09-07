# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import re
import sys
import time
import base64
import logging
import threading
from pydbgpd import *
from socket_server import socket_server

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='pydbgpd_proxy.log',
        filemode='w')
        
class input_redirection:
    _data = ""
    def __init__(self):
        self._in = sys.stdin
        self._lock_excute = threading.Lock()
    
    def read(self, size=-1):
        while len(self._data) == 0:
            time.sleep(0.1)
        self._lock_excute.acquire()
        ret_data = self._data
        self._data = ""
        self._lock_excute.release()
        return ret_data
    
    def readline(self, size=-1):
        while len(self._data) == 0:
            time.sleep(0.1)
        self._lock_excute.acquire()
        ret_data = self._data
        self._data = ""
        self._lock_excute.release()
        return ret_data
    
    def readlines(self, size=-1):
        while len(self._data) == 0:
            time.sleep(0.1)
        self._lock_excute.acquire()
        ret_data = self._data
        self._data = ""
        self._lock_excute.release()
        return ret_data
    
    def write(self, data):
        self._lock_excute.acquire()
        logging.debug("reqeust: " + data)
        self._data = data
        self._lock_excute.release()
    
    def flush(self):
        pass
    
class output_redirction:
    _out = None
    _query_event = None
    _data = ""
    _response = ""
    def __init__(self, query_event):
        self._out = sys.stdout
        self._query_event = query_event

    def write(self, output_stream):
        if re.match('^\[dbgp-', output_stream):
            self._send_data(True)
        elif re.match('^\[dbgp\]', output_stream):
            self._send_data(False)
        else:
            self._data += output_stream
        
    def flush(self):
        pass
        #self._send_data()
        #self._out.flush()
        
    def _send_data(self, is_seesion):
        if (is_seesion):
            end_ch = "@\n"
        else:
            end_ch = ":\n"
            
        data = base64.b64encode(self._data) + end_ch
        logging.debug("response:" + self._data + end_ch)
        self._response = data
        self._query_event.set()
        
        #data = self._data + end_ch
        self._out.write(data)
        #self._out.write(self._data)
        self._data = "" 
        self._out.flush()
        
    def get_reponse(self):
        return self._response

query_event = threading.Event()
out_r = output_redirction(query_event)
in_r = input_redirection()
sys.stdin = in_r
sys.stdout = out_r
sys.stderr = out_r

def Query(cmd):
    logging.debug("query " + cmd)
    query_event.clear()
    in_r.write(cmd)
    query_event.wait()
    return out_r.get_reponse()

if __name__ == "__main__":
    cmd_server = socket_server(Query)
    cmd_server.Start()
    sys.exit(main([0]))