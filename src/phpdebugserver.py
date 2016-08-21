# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from bottle import route, run
from bottle import static_file
from bottle import template
from bottle import request, response, get, post

from dbgp.client import *

import os
import json
import md5
from debugger import debugger
from ide_config import ide_config
from request_db import request_db
from files_watch import files_watch
from pydbgpd_helper import pydbgpd_helper
from files_tree_build import files_tree_build_json
from variables_tree_build import variables_tree_build

debugger = debugger()
#sub = pydbgpd_helper()
#sub.start()

files_tree = files_tree_build_json()
  
request_key = ["cmd", "result"]

@route('/index')
def main_page():
    #os.system("python bin/pydbgp.py -d localhost:9000")
    #return static_file('index.html', root='D:\\fangliang\\Documents\\NetBeansProjects\\PhpDebugServer\\src\\phpdebugserver\\', mimetype='text/html')
    
    #info = {
    #"context":{'Locals':[{'name':'$a', 'type':'string', 'value':'1'}],'Superglobals':[{'name':'$b', 'type':'int', 'value':1}], 'User defined constants':[{'name':'$c', 'type':'string', 'value':'2'}]},
    #"status": {},
    #"stack":{'frame':0, 'path':'file:///var/www/html/index.php', 'line_no':8, 'function_name':'main'}
    #}
    #encodedjson = json.dumps(info)
    #request.forms.append('info', encodedjson)
    return template('index', **request.forms)

@route('/files/<filepath:path>')
def highlight_file(filepath):
    return static_file(filepath, root='views')

@route('/frame', method='Get')
def request_cmd_get():
    return template('frame', **request.forms)

@route('/cmd', method='POST')
def request_cmd_post():
    cmd = request.forms.get("cmd")
    global sub
    data = sub.query(cmd)
    return data

@route('/do', method='POST')
def request_do_post():
    action = request.forms.get("action")
    if None == action or len(action) == 0:
        return template('index')
    param = request.forms.get("param")
    global debugger
    (ret,type) = debugger.do(action, param);
    if type == "json":
        #print ret
        return json.dumps(ret)
    else:
        return template('index', **request.forms)
    
@route('/files_tree', method='get')
def request_files_tree():
    action = request.query.action
    folder_en = request.query.param
    folder_de = base64.b64decode(folder_en);
    ide_cfg = ide_config()
    print folder_de, action
    
    if "build" == action:
        folders = ide_cfg.get_folders()
        files_tree.set_root_path(folders)
        data = files_tree.build()
        return json.dumps(data)
    elif "add" == action:
        folders = ide_cfg.add_folder(folder_de)
        ret = {"ret":1}
        return json.dumps(ret)
    elif "remove" == action:
        folders = ide_cfg.remove_folder(folder_de)
        ret = {"ret":1}
        return json.dumps(ret)
    
@route("/files_watch", method='get')
def request_files_watch():
    action = request.query.action
    filepath_en = request.query.param
    filepath_de = base64.b64decode(filepath_en);
    ide_cfg = ide_config()
    print filepath_en, action
    
    if "get_list" == action:
        files = ide_cfg.get_watch_file()
        files_info = []
        for item in files:
            item_info = {}
            m1 = md5.new()   
            m1.update(item)
            item_info["id"] = m1.hexdigest()
            item_info["path"] = base64.b64encode(item)
            item_info["name"] = os.path.basename(item)
            files_info.append(item_info)
        ret = {"ret":1, "list":files_info}
        return json.dumps(ret)
    elif "add" == action:
        files = ide_cfg.add_watch_file(filepath_de)
        ret = {"ret":1}
        return json.dumps(ret)
    elif "remove" == action:
        files = ide_cfg.remove_watch_file(filepath_de)
        ret = {"ret":1}
        return json.dumps(ret)
    elif "get_file" == action:
        fw = files_watch()
        return fw.get_file_content(filepath_de, 50)
    
@route("/request", method='get')
def request_action():
    action = request.query.action
    request_name_en = request.query.param
    request_name_de = base64.b64decode(request_name_en);
    rdb = request_db()
    
    if "get_list" == action:
        name_list = rdb.get_names()
        return {"ret":1, "list":name_list}
    elif "get_data" == action:
        data = rdb.get_request(request_name_de)
        return {"ret":1, "data":data}
    elif "save_data" == action:
        pass
    elif "remove_data" == action:
        rdb.remove_request(request_name_de)
        return {"ret":1}
    elif "edit_data" == action:
        data = {"url":"http://www.baidu.com","get":{"x1":"y1","x2":"y2"},"post":{"a1":"b1", "a2":"b2"}}
        return template('component/edit_request', data = data)
        pass
    
@route("/variables_watch", method='get')
def request_variables_watch():
    action = request.query.action
    variable_name_en = request.query.param
    variable_name_de = base64.b64decode(variable_name_en);
    ide_cfg = ide_config()
    
    if "get_list" == action:
        variable_names = ide_cfg.get_watch_variable()
        variable_names_info = []
        for item in variable_names:
            item_info = {}
            m1 = md5.new()   
            m1.update(item)
            item_info["id"] = m1.hexdigest()
            item_info["name"] = os.path.basename(item)
            variable_names_info.append(item_info)
        ret = {"ret":1, "list":variable_names_info}
        return json.dumps(ret)
    elif "add" == action:
        variable_names = ide_cfg.add_watch_variable(variable_name_de)
        ret = {"ret":1}
        return json.dumps(ret)
    elif "remove" == action:
        variable_names = ide_cfg.remove_watch_variable(variable_name_de)
        ret = {"ret":1}
        return json.dumps(ret)
    elif "get_variable" == action:
        pass
    
@route('/getfile', method='POST')
def getFile():
    path = request.forms.get("path")
    if path.startswith("file:///"):
        path = path.replace("file:///", "")
    fo = open(path)
    try:
         text = fo.read()
    finally:
         fo.close( )
    type = path.split('.')[-1]
    data = base64.b64encode(text)
    ret_info = {"ret":1, "type":type, "data":data}
    return json.dumps(ret_info)
    
@route('/variables', method='POST')
def request_variables():
    global debugger
    (ret,type) = debugger.do("get_variables", "");
    if type == "json":
        if ret["ret"] == 1:
            vrb = variables_tree_build()
            variables_tree_data = vrb.build(ret["data"])
            ret_new = {"ret":1, "data": variables_tree_data}
            return json.dumps(ret_new)
        else:
            return json.dumps({"ret":0});

if __name__ == "__main__":
    try:
        run(host='localhost', port=8085, debug=True)
    except Exception as e:
        print e