from botweb_server import BotwebServer
from api_handler_gardenbrainv2 import Api_handler_gardenbrain
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
import sys

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

def mqtt_thread(bootstats):
    mqtt = Mqtt(glog, api, bootstats)


def main_thread():
    try:
        #wifi = Wifi(glog)
        #webserver = BotwebServer(glog, api)
        print("Main thread")
    except Exception as e:
        print("Exception thrown resetting")
        print(e.message)
        machine.reset()

def bootstats():
    s = os.statvfs('/')
    bootstat = {}
    bootstat["mem_alloc"] = f"{gc.mem_alloc()} bytes"
    bootstat["mem_free"] = f"{gc.mem_free()} bytes"
    bootstat["storage_free"] = f"{s[0]*s[3]/1024} KB"
    bootstat["cpu_freq"] = f"{machine.freq()/1000000}Mhz"
    #bootstat["sys_implementation"] = sys.implementation
    bootstat["sys_version"] = sys.version
    
    wl_cs = machine.Pin(25) # WiFi chip SDIO_DATA3 / gate on FET between VSYS divider (FET drain) and GPIO29 (FET source)
    wl_cs.init(mode=machine.Pin.OUT, value=1)
    pin = machine.ADC(29)
    adc_reading  = pin.read_u16()
    adc_voltage  = (adc_reading * 3.3) / 65535
    vsys_voltage = adc_voltage * 3
    
    bootstat["adc_reading"] = adc_reading
    bootstat["adc_voltage"] = adc_voltage
    bootstat["vsys_voltage"] = vsys_voltage

    wl_cs.init(mode=machine.Pin.ALT, pull=machine.Pin.PULL_DOWN)#, alt=31)#try to restore initial WL_CS state
    return bootstat
    
    #glog.message(f"Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used.")
    #glog.message(f"Free storage: {s[0]*s[3]/1024} KB")
    #glog.message(f"CPU Freq: {machine.freq()/1000000}Mhz")


if __name__ == "__main__":

    glog = GardenLog()
    glog.message("Now initializing")

    bootstats = bootstats()


    api = Api_handler_gardenbrain(glog)
    wifi = Wifi(glog)
    mqtt_thread(bootstats)
    #second_thread = _thread.start_new_thread(mqtt_thread, ())
 
    #main_thread()
    
