#garden_log.py
import random
import os
import time
import ntptime
import botbrain_config
import socket

class GardenLog:
    
    def __init__(self):
        self.logcount = 0
        try:
            filesize = os.stat("debug.log")
        except:
            filesize = [0,0,0,0,0,0,0]
        
        if filesize[6] < 1000000:     
            self.log = open("debug.log", "a")
        else:
            self.log = open("debug.log", "w")
            
        print("initialized")
        
    def message(self, message):
        
        #We'll migrate to this once I have NTP working
        #r = random.randint(1,65535)
        #r = time.localtime()
        #self.log.write(f"{self.logcount} - {message} [{r[0]}-{r[1]}-{r[2]}-{r[3]}-{r[4]}]\n")
        
        r = random.randint(1,65535)
        if botbrain_config.LOG_TO_DISK:
            self.log.write(f"{self.logcount} - {message} [{r}]\n")
            self.log.flush()
        print(message)
        self.logcount += 1
    
    def close(self):
        self.log.close()
        
    def display(self):
        #This function has a challenge in that it will exhaust memory. So I'm just reading the last 2KB
        self.log.flush()
        
        debuglog = open("debug.log", "r")
        debuglog.seek(-2000,2)
        last_lines = debuglog.read()
        debuglog.close()
            
        return last_lines
    
    def syslog_message(self, message):
        try:
            MESSAGE = b'<165>%s' % message
            sock =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = socket.getaddrinfo(botbrain_config.SYSLOG_HOST, botbrain_config.SYSLOG_PORT) [0][-1]
            sock.settimeout(1.0)
            sock.connect(addr)
            sock.send(MESSAGE)
        except:
            print(f"Unable to send: {message}")
