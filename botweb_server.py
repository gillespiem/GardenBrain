import time
import socket
import re
import json
import sys
import botbrain_config
from api_handler_gardenbrain import Api_handler_gardenbrain

class BotwebServer:

    def __init__(self, api_handler = False):
        self.api_handler = api_handler
        self.start()        

    def web_page_200(self, http_response):
        r={}
        r["code"] = 200
        r["message"] = "This is botbrain"
        json_response = json.dumps(r)

        #json_response = self.api_handler.get_api_methods()
        #json_response={"response" : http_response["data"]}
        #json_response={"response" : http_response["data"]}
        json_response=json.dumps(http_response["data"])

        response = "HTTP/1.1 200 OK\r\nServer:botbrain-0.1\r\nContent-Type: application/json\r\n\r\n%s" % json_response
        #response = "HTTP/1.1 200 OK\r\nServer:botbrain-0.1\r\nContent-Type: application/json\r\n%s" % json_response
        
        print(response)
        return bytes(response, 'utf-8')

    def web_page_400(self):
        r={}
        r["code"] = 400
        r["message"] = "Invalid payload received"
        json_response = json.dumps(r)
        response ="HTTP/1.1 400 Bad Request\r\nServer:botbrain-0.1\r\nContent-Type: application/json\r\n\r\n%s" % json_response
        return bytes(response, 'utf-8')

    def parse_api_action(self, json_payload):
        print("Payload is %s" % json_payload)
        http_response = {}
        http_response["code"] = False
        http_response["data"] = False

        if json_payload == b'':
            http_response["code"] = 200
            return http_response

        try:
            j = json.loads(json_payload)
            print ("Now triggering action %s " % j["action"])
            
            http_response["data"] = self.api_handler.dynamic_call(j["action"])
            http_response["code"] = 200
        except Exception as e:
            print("This is likely to not be JSON data")
            print(e)
            http_response["code"] = 400
        return http_response


    def parse_request(self, request):
        request_lines = request.splitlines()
        
        #Check the first line for the HTTP verb and URI
        m = re.match(b"(^.*?)\s+(.*?)\s+(.*)", request_lines[0])
        if m:
            print("We have a match")
            print(m.group(1))
            http_verb = m.group(1).upper()
            http_uri = m.group(2)
            http_version = m.group(3)
            http_data = False
            if http_verb == b"GET":
                print("THIS is a GET request")
                #http_data = request_lines[-1]
                #For GET requests, we reform the URI to json
                http_action = { "action" : http_uri[1:] }
                http_data = json.dumps(http_action)
                print(http_data)
                return self.parse_api_action(http_data)
            elif http_verb == b"POST":
                print("THIS is a POST request for %s " % http_uri)
                http_data = request_lines[-1]
                return self.parse_api_action(http_data)
        
        
    def start(self):
        #Establish a listener socket
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((botbrain_config.HOST,botbrain_config.PORT))
                s.listen()
                break
            except OSError as e:
                print("No %s" %e)
                print("Waiting 5 seconds for socket to expire...")
                time.sleep(5)

        #Process incoming requests
        while True:
            print("Now listening.,..")
            conn, addr = s.accept()
            print("Connection from %s " % str(addr))
            request = conn.recv(2048)
            print("Content = %s" % str(request))
            
            http_response = self.parse_request(request)
            
            if http_response["code"] == 200:
                response = self.web_page_200(http_response)
            else:
                response = self.web_page_400()

            conn.send(response)
            conn.close()
