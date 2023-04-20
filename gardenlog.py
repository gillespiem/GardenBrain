#garden_log.py

class GardenLog:
    
    def __init__(self):
        self.logcount = 0
        self.log = open("debug.log", "a")
        print("initialized")
        
    def message(self, message):
        #self.log = open("test.log","a")
        self.log.write(f"{self.logcount} - {message}\n")
        print(message)
        self.logcount += 1
    
    def close(self):
        self.log.close()
        
    def display(self):
        #This function has a challenge in that it will exhaust memory. Maybe we return only the last 25 lines or so...
        debuglog = open("debug.log", "r")
        debuglog.close()
        return "DEMO DATA ONLY"