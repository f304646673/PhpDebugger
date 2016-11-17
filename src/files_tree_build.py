# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os
import json
import base64
import md5
import platform

class files_tree_build:
    
    _html_text = ""
    root_path = []
    
    def __init__(self):
        pass
    
    def add_root_path(self,path):
        self.root_path.append(path)
    
    def build(self):
        self._html_text= ""
        for item in self.root_path:
            if os.path.isdir(item):
                self._build_dir_start(item.split(os.sep)[-1],item)
                self.walk(item)
        return base64.b64encode(self._html_text)
    
    def walk(self,filepath):
        files = os.listdir(filepath)
        for fi in files:
            files_temp = []
            fi_d = os.path.join(filepath,fi)            
            if os.path.isdir(fi_d):
                self._build_dir_start(fi_d.split(os.sep)[-1],fi_d)
                self.walk(fi_d)
                self._build_dir_end()
            else:
                files_temp.append([fi,os.path.join(filepath,fi_d)])
            for item in files_temp:
                self._build_file(item[0],item[1])

    def _build_dir_start(self,name,path):
        dir_ele = "<li><span><a href='#' onclick='sel_dir(\"" + base64.b64encode(path) +"\")'>" + name + "</a></span>";
        self._html_text += dir_ele;
        self._html_text += "<ul>"
    
    def _build_dir_end(self):
        self._html_text += "</li></ul>"
    
    def _build_file(self,name,path):
        file_ele = "<li><span><a href='#' onclick='sel_file(\"" + base64.b64encode(path) +"\")'>" + name + "</a></span></li>";
        self._html_text += file_ele

class files_tree_build_json:
    
    root_path = []
    files_info = {}
    
    def __init__(self):
        pass
    
    def set_root_path(self,paths):
        if False == isinstance(paths,list):
            return
        self.root_path = paths
    
    def build(self):
        self.files_info = []
        for item in self.root_path:
            if False == isinstance(item, basestring):
                continue
            if os.path.isdir(item):
                self.files_info.append(self.walk(item))
        #return base64.b64encode(json.dumps(self.files_info))
        return self.files_info
    
    def walk(self,filepath):
        sub_files_info = {}
        files_info = {}
        folder_path_modify = filepath.replace('\\', '/')
        if "Windows" == platform.system():
            folder_path_modify = "file:///" + folder_path_modify
        else:
            folder_path_modify = "file://" + folder_path_modify
        files_info = self.build_folder_info(folder_path_modify.split('/')[-1], folder_path_modify)
        for (k,v) in files_info.items():
            sub_files_info[k] = v
            
        sub_files_info["children"] = []
        files_temp = []
        
        files = os.listdir(filepath)
        for fi in files:
            fi_d = os.path.join(filepath,fi)            
            if os.path.isdir(fi_d):
                sub_files_info["children"].append(self.walk(fi_d))
            else:
                file_path_modify = os.path.join(filepath, fi_d)
                file_path_modify = file_path_modify.replace('\\', '/')
                if "Windows" == platform.system():
                    file_path_modify = "file:///" + file_path_modify
                else:
                    file_path_modify = "file://" + file_path_modify
                files_temp.append([fi, file_path_modify])
                
        for item in files_temp:
            sub_files_info["children"].append(self.build_file_info(item[0],item[1]))
            
        return sub_files_info
                
    def build_folder_info(self, folder_name, folder_path):
        folder_info = {}
        folder_info["text"] = folder_name
        folder_info["state"] = "closed"
        m1 = md5.new()   
        m1.update(folder_path) 
        folder_info["attributes"] = {"path":folder_path , "id": m1.hexdigest()}
        return folder_info
    
    def build_file_info(self, file_name, file_path):
        flle_info = {}
        flle_info["text"] = file_name
        m1 = md5.new()   
        m1.update(file_path) 
        flle_info["attributes"] = {"path":file_path, "id": m1.hexdigest()}
        return flle_info

if __name__ == "__main__":
    sub = files_tree_build_json()
    sub.set_root_path(["D:\\fangliang\\Documents\NetBeansProjects\\PhpDebugServer\\src\\bin"])
    print sub.build()