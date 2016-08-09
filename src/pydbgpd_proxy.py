# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import sys
import re
import base64
import logging
from pydbgpd import *

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='pydbgpd_proxy.log',
        filemode='w')
        
class output_redirction:
    _out = None
    _data = ""
    def __init__(self):
        self._out = sys.stdout

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
        
        logging.debug(self._data + end_ch)
        #data = self._data + end_ch
        self._out.write(data)
        #self._out.write(self._data)
        self._data = "" 
        self._out.flush()
    
class pydbgpd_proxy:
    def __init__(self):
        out = output_redirction()
        sys.stdout = out
        sys.stderr = out
        sys.exit(main([0]))

if __name__ == "__main__":
    a = pydbgpd_proxy()