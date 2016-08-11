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
from pydbgpd_helper import pydbgpd_helper
from files_tree_build import files_tree_build_json
from ide_config import ide_config
from debugger import debugger
from files_watch import files_watch

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

@route('/cmd', method='Get')
def request_cmd_get():
    return template('index', **request.forms)

@route('/test', method='Get')
def request_cmd_get():
    return template('test', **request.forms)

@route('/frame', method='Get')
def request_cmd_get():
    return template('frame', **request.forms)

@route('/cmd1', method='POST')
def request_cmd_post():
    cmd = request.forms.get("cmd")
    if None == cmd or len(cmd) == 0:
        return template('index')
    
    global sub
    data = sub.query(cmd)
    print data
    request.forms.replace("result", data)
    
    info = sub.get_info()
    encodedjson = json.dumps(info)
    request.forms.append('info', encodedjson)
    
    src = sub.get_file_src()
    request.forms.append('src', src)
    
    return template('index', **request.forms)

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
    floder_en = request.query.param
    floder_de = base64.b64decode(floder_en);
    ide_cfg = ide_config()
    print floder_de, action
    
    if "build" == action:
        floders = ide_cfg.get_floders()
        files_tree.set_root_path(floders)
        data = files_tree.build()
        return json.dumps(data)
    elif "add" == action:
        floders = ide_cfg.add_floder(floder_de)
        ret = {"ret":1}
        return json.dumps(ret)
    elif "remove" == action:
        floders = ide_cfg.remove_floder(floder_de)
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
    
@route('/hello')
def hello():
    return "Hello World!"

if __name__ == "__main__":
    try:
        run(host='localhost', port=8085, debug=True)
    except Exception as e:
        print e