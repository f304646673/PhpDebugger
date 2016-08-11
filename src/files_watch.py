# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os
import string

class files_watch:
    def __init__(self):
        pass

    def get_file_content(self,path,line):
        data = ""
        file = None
        try: 
            file = open(path, 'r')
            br = BackwardsReader(file)
            for i in range(line):
                data_t = br.readline()
                data = data_t + data
        except IOError as err:  
            print('File Error:'+str(err))
        finally:  
            if file:  
                file.close()  
        
        return data
    
    
class BackwardsReader:
    """Read a file line by line, backwards"""
    BLKSIZE = 4096

    def readline(self):
        while 1:
            newline_pos = string.rfind(self.buf, "\n")
            pos = self.file.tell()
            if newline_pos != -1:
                # Found a newline
                line = self.buf[newline_pos+1:]
                self.buf = self.buf[:newline_pos]
                if pos != 0 or newline_pos != 0 or self.trailing_newline:
                    line += "\n"
                return line
            else:
                if pos == 0:
                    # Start-of-file
                    return ""
                else:
                    # Need to fill buffer
                    toread = min(self.BLKSIZE, pos)
                    self.file.seek(-toread, 1)
                    self.buf = self.file.read(toread) + self.buf
                    self.file.seek(-toread, 1)
                    if pos - toread == 0:
                        self.buf = "\n" + self.buf

    def __init__(self, file):
        self.file = file
        self.buf = ""
        self.file.seek(-1, 2)
        self.trailing_newline = 0
        lastchar = self.file.read(1)
        if lastchar == "\n":
            self.trailing_newline = 1
            self.file.seek(-1, 2)
            
if __name__ == "__main__":
    fw = files_watch()
    print fw.get_file_content("D:\\fangliang\\Documents\\NetBeansProjects\\PhpDebugServer\\src_on_github\\src\\files_watch.py", 100)