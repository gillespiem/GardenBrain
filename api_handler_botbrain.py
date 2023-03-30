import json

class Api_handler:
    def __init__(self, name):
        self.set_name(name)
    
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return "%s API " % self.name
    
    def get_api_methods(self):
        method_list = [method for method in dir(self) if method.startswith('__') is False]
        d = {}
        d["available_methods"] = method_list
        return json.dumps(d)


