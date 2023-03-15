from api_handler import Api_handler
import json
#import RPi.GPIO as GPIO
from machine import Pin
import time

class Api_handler_gardenbrain(Api_handler):
    def __init__(self):
        self.set_name("botbrain")
        print ("Now initiating %s" % self.get_name())
        print(self.get_api_methods())

    def action_lpm0(self):
        print("Going to LPM0")

    def action_lpm1(self):
        print("Going to LPM1")

    def action_lpm2(self):
        print("Going to LPM2")

    def action_lpm3(self):
        print("Going to LPM3")

    def action_reboot(self):
        print("Rebooting")

    def action_flashled(self):
        print("Now flashing led for 5 seconds")
    
    def action_checksoil(self):
        channel = 15
        water_sense = Pin(channel, Pin.IN)
        print(water_sense.value())
        if (water_sense.value()):
            result = "No water is detected"
            print(result)
            return result
        else:
            result = "Water is detected"
            print(result)
            return result

    def dynamic_call(self, action):
        if hasattr(self, action) and callable(func := getattr(self,action)):
            return func()




#import time

#GPIO SETUP
#watersig = digitalio.DigitalInOut(board.GP15)
#watersig.switch_to_input(pull=digitalio.Pull.UP)

#i = 0
#while True:
#        time.sleep(1)
#        #print("%s %d" % (watersig.value, i ))
#        if watersig.value:
#            print("No water detected")
#        else:
#            print("Water is detected")
#        i = i + 1 
