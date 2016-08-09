# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import ConfigParser
import base64
import json

class ide_config:
    def __init__(self):
        pass
        
    def add_floder(self,path):
        floders = self.get_floders()
        if path in floders:
            return
        floders.append(path)
        print floders
        self._set_floders(floders)
        return floders
        
    def remove_floder(self,path):
        floders = self.get_floders()
        if path not in floders:
            return
        floders.remove(path)
        self._set_floders(floders)
        return floders
    
    def get_floders(self):
        config = ConfigParser.ConfigParser()
        with open('ide.cfg','r') as cfgfile: 
            config.readfp(cfgfile) 
        
        if False == config.has_section("floders"):
            return []

        if "data" not in config.options("floders"):
            return []
            
        output_data = config.get("floders", "data")
        temp = base64.b64decode(output_data)
        data = json.loads(temp)
        if isinstance(data,list):
            return data
        else:
            return []
        
    def _set_floders(self, data):
        config_r = ConfigParser.ConfigParser()
        config_r.read('ide.cfg')
        if False == config_r.has_section("floders"):
            config_r.add_section("floders")
        
        input_data = base64.b64encode(json.dumps(data))
        config_r.set("floders", "data", input_data)
        with open('ide.cfg', 'wb') as configfile:
            config_r.write(configfile)
        
if __name__ == "__main__":
    ide = ide_config()
    
    ide.remove_floder(6)
    print ide.get_floders()
    #return
    #ide.set_floders([1,2,3,4])