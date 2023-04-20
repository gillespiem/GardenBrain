from botweb_server import BotwebServer
from api_handler_gardenbrain import Api_handler_gardenbrain
from wifi import Wifi
from machine import Pin
import time
import _thread
from gardenlog import GardenLog




def watchdog_thread():
    import time
    wdt = machine.WDT(timeout=8000)
    
    pet_count = 0
    while True:
        pet_count += 1
        #Every 30 minutes enter a log entry 360 is the normal value
        if pet_count > 3:
            glog.message("Now petting the dog")
            pet_count = 0
        
        wdt.feed()
        time.sleep(5)

def main_thread():
    try:
        #wifi = Wifi()
        api = Api_handler_gardenbrain(glog)
        webserver = BotwebServer(glog, api)
    except Exception as e:
        print("Exception thrown")
        print(e.message)
    #    webserver = BotwebServer(api)
    #except Exception as e:
    #    print("Exception thrown")
    #    print(e.message)
    #    machine.reset()

if __name__ == "__main__":
    
    glog = GardenLog()
    glog.message("Now initializing")
    
    wifi = Wifi(glog)
    second_thread = _thread.start_new_thread(watchdog_thread, ())
 

#    while True:
#        print("OK")
#        time.sleep(1)

    main_thread()
    #thread_two()