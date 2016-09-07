# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

class socket_protocol:
    def __init__(self):
        self.response = ""
        pass
    
    def pack_request(self, request):
        request_len = len(request) + 8
        package = '{:0>8}'.format(request_len)
        package += request
        return package
    
    def input_response(self, data):
        self.response += data
        
    def data_valid(self):
        if len(self.response) < 8:
            return False
        length = self.response[:8]
        if int(length) == len(self.response):
            return True
        else:
            return False
        
    def clear(self):
        self.response = ""
        
    def get_response(self):
        if False == self.data_valid():
            return ""
        return self.response[8:]

    
if __name__ == "__main__":
    a = socket_protocol()    
    a.input_response(a.pack_request("ssss"))
    print a.get_response()