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
from pydbgpd_helper import pydbgpd_helper
from files_tree_build import files_tree_build_json
from ide_config import ide_config
from debugger import debugger

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
        print ret
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
        run(host='localhost', port=8085, debug=False)
    except Exception as e:
        print e