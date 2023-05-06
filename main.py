from botweb_server import BotwebServer
from api_handler_gardenbrain import Api_handler_gardenbrain
from wifi import Wifi
from machine import Pin
import machine
import time
import _thread
from gardenlog import GardenLog
from mqtt_gardenbrain import Mqtt
import gc
import os
import botbrain_config

def watchdog_thread():
    import time
    wdt = machine.WDT(timeout=8000)
    
    pet_count = 0
    while True:
        pet_count += 1
        #Every 30 minutes enter a log entry 360 is the normal value
        # For now, this is actually every 15 seconds
        if pet_count > 3:
            glog.message("Now petting the dog")
            pet_count = 0
        
        wdt.feed()
        time.sleep(5)

def mqtt_thread():
    mqtt = Mqtt(glog, api)


def main_thread():
    try:
        #wifi = Wifi(glog)
        #webserver = BotwebServer(glog, api)
        print("Main thread")
    except Exception as e:
        print("Exception thrown resetting")
        print(e.message)
        machine.reset()

def bootstats(glog):
    s = os.statvfs('/')
    glog.message(f"Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used.")
    glog.message(f"Free storage: {s[0]*s[3]/1024} KB")
    glog.message(f"CPU Freq: {machine.freq()/1000000}Mhz")

if __name__ == "__main__":
    
    #print("Waiting to change CPU freq")
    #time.sleep(10)
    #machine.freq(botbrain_config.CPU_SPEED)
    
    glog = GardenLog()
    glog.message("Now initializing")
    
  
    api = Api_handler_gardenbrain(glog)

    bootstats(glog)
    
    wifi = Wifi(glog)
    second_thread = _thread.start_new_thread(mqtt_thread, ())
 
    main_thread()
    
