# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import json

class variables_tree_build:
    
    def __init__(self):
        self._id = 0
        pass

    def build(self,variables):
        info = []
        first = True
        for (key,value) in variables.items():
            item = {}
            item["id"] = self._id
            self._id = self._id + 1
            item["name"] = key
            item["type"] = ""
            item["value"] = ""
            if first:
                first = False
            else:
                item["state"] = "closed"
                
            item["children"] = self.build_typs(value)
            info.append(item)
        return info
    
    def build_typs(self,data):
        info = []
        for (key,value) in data.items():
            item = {}
            item["id"] = self._id
            self._id = self._id + 1
            item["name"] = key
            item["type"] = ""
            item["value"] = ""
            if "Superglobals" == key:
                item["state"] = "closed"
            item["children"] = self._build_variables_tree(value)
            info.append(item)
        return info
    
    def _build_variables_tree(self,data):
        items = []
        for single in data:
            item = {}
            item["name"] = single["name"]
            item["type"] = single["type"]
            item["value"] = single["value"]
            item["id"] = self._id
            self._id = self._id + 1
            items.append(item)
        return items
    
if __name__ == "__main__":
    data = {
    "locals":[{"name":"name1", "type":"type1", "value":"value1"},{"name":"name2", "type":"type2", "value":"value2"}],
    "superglobals":[{"name":"name1", "type":"type1", "value":"value1"},{"name":"name2", "type":"type2", "value":"value2"}],
    "user":[{"name":"name1", "type":"type1", "value":"value1"},{"name":"name2", "type":"type2", "value":"value2"}],
    }
    us = variables_tree_build()
    print us.build(data)
    pass    
