from botweb_server import BotwebServer
from api_handler_gardenbrain import Api_handler_gardenbrain
from wifi import Wifi
from machine import Pin
import time
import led_smokesignal
import _thread



def watchdog_thread():
    wdt = machine.WDT(timeout=8000)
    while True:
        print("Petting the dog")
        wdt.feed()
        time.sleep(5)

def main_thread():
    wifi = Wifi()
    api = Api_handler_gardenbrain()
    webserver = BotwebServer(api)    

if __name__ == "__main__":
    second_thread = _thread.start_new_thread(watchdog_thread, ())
    main_thread()
    #thread_two()