# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import ConfigParser
import base64
import json
import os

class request_db:
    _db_name = 'request.db'
    
    def __init__(self):
        if not os.path.exists(self._db_name):
            f = open(self._db_name, 'w')
            f.close()
        
    def add_request(self,name,value):
        config_r = ConfigParser.ConfigParser()
        config_r.read(self._db_name)
        if False == self.is_request_name_exist(name):
            config_r.add_section(name)
        
        input_data = base64.b64encode(json.dumps(value))
        config_r.set(name, "data", input_data)
        with open(self._db_name, 'wb') as configfile:
            config_r.write(configfile)
    
    def is_request_name_exist(self,name):
        config = ConfigParser.ConfigParser()
        with open(self._db_name,'r') as cfgfile: 
            config.readfp(cfgfile) 
        
        return config.has_section(name)
    
    def remove_request(self,name):
        cfgfile = ConfigParser.ConfigParser()
        cfgfile.write(open(self._db_name, "w"))
        cfgfile.remove_section(name)
        
    def get_request(self,name):
        config = ConfigParser.ConfigParser()
        with open(self._db_name,'r') as cfgfile: 
            config.readfp(cfgfile) 
        
        if False == config.has_section(name):
            return {}

        if "data" not in config.options(name):
            return {}
            
        output_data = config.get(name, "data")
        temp = base64.b64decode(output_data)
        data = json.loads(temp)
        if isinstance(data,object):
            return data
        else:
            return {}
        
    def get_names(self):
        config = ConfigParser.ConfigParser()
        with open(self._db_name,'r') as cfgfile: 
            config.readfp(cfgfile) 
        names = config.sections()
        return names

if __name__ == "__main__":
    db = request_db()
    db.add_request("xxx",{"Get":"yyyy"})
    print db.get_names()
    print db.get_request("xxx")
    db.remove_request("xxx")