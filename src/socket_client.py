# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os
import time
import socket
import threading
from socket_protocol import socket_protocol

class socket_client:
    def __init__(self):
        self._response_ready = threading.Event()
        self._stop_event = threading.Event()
        self._lock_excute = threading.Lock()
        self._communicate_thread = None
        self._cmd = ""
        self._result = ""
        pass
    
    def __del__(self):
        self.Stop()
        pass
    
    def Query(self,cmd):
        self._lock_excute.acquire()
        self._cmd = cmd
        self._response_ready.clear()
        self._response_ready.wait()
        result = self._result
        self._lock_excute.release()
        return result
    
    def _worker(self):
        self._stop_event.clear()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 9001))
        s_data = socket_protocol()
        while False == self._stop_event.wait(0.1):
            query = ""
            if len(self._cmd) == 0:
                continue
           
            query = self._cmd 
            self._cmd = ""
            
            send_data = s_data.pack_request(query)
            s.sendall(send_data)
            while False == self._stop_event.wait(0.1):
                data = s.recv(1024)
                s_data.input_response(data)
                if s_data.data_valid():
                    self._result = s_data.get_response()
                    s_data.clear()
                    self._response_ready.set()
                    break
        s.close()

    def Start(self):
        if self._communicate_thread:
            return
        self._communicate_thread = threading.Thread(target=self._worker)
        self._communicate_thread.start()
        
    def Stop(self):
        self._stop_event.set()
        while self._communicate_thread.is_alive():
            time.sleep(0.1)
        self._communicate_thread = None
        
if __name__ == "__main__":
    a = socket_client()
    a.Start()
    while True:
        cmd = raw_input("CMD: ") 
        print a.Query(cmd)
        if "quitt" == cmd:
            break
            
    print a.Query("help")
    time.sleep(1)
    
    print a.Query("help")
    time.sleep(2)
    
    print a.Query("help")
    time.sleep(3)
    print 'xxxxxx'