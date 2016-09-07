# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os
import time
import socket
import threading
from socket_protocol import socket_protocol

def deal_data(data):
    send_data = "recv" + data
    return send_data

class socket_server:
    def __init__(self, deal_func = None):
        self._stop_event = threading.Event()
        self._communicate_thread = None
        if deal_func:
            self.deal_func = deal_func
        else:
            self.deal_func = deal_data
        pass
    
    def __del__(self):
        self.Stop()
        pass
    
    def Start(self):
        if self._communicate_thread:
            return
        self._communicate_thread = threading.Thread(target=self._worker)
        self._communicate_thread.start()
        
    def _worker(self):
        self._stop_event.clear()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", 9001))
        s.listen(1)
        con,addr = s.accept()
        s_data = socket_protocol()
        while False == self._stop_event.wait(0.1):
            data = con.recv(1024)
            s_data.input_response(data)
            if s_data.data_valid():
                send_data = self.deal_func(s_data.get_response())
                con.sendall(s_data.pack_request(send_data))
                s_data.clear()
        con.close()
        
    def Stop(self):
        self._stop_event.set()
        while self._communicate_thread.is_alive():
            time.sleep(0.1)
        self._communicate_thread = None
 
if __name__ == "__main__":
    a = socket_server()
    a.Start()