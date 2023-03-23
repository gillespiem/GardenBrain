from api_handler import Api_handler
import json
from machine import Pin
import dht
import botbrain_config

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
    
    def action_checkdigitalsensor(self, channel = 15):
        sensor = Pin(channel, Pin.IN)
        sensor_value = sensor.value()
        gpio_name = f"GPIO{channel:02}"
        if (sensor_value):
            result = botbrain_config.PINS[gpio_name]["human_readable"][sensor_value]
            print(result)
            return result
        else:
            result = botbrain_config.PINS[gpio_name]["human_readable"][sensor_value]
            print(result)
            return result

    def action_checkdigitalsensors_all(self):
        for channel in botbrain_config.PINS.keys():
            if botbrain_config.PINS[channel]["type"] == "digital":
                print(f"Now testing {channel}")
                result = self.action_checkdigitalsensor(botbrain_config.PINS[channel]["channel"])
                print(result)
                #print (f"{channel} is {botbrain_config.PINS[channel]['name']} at pin {botbrain_config.PINS[channel]['channel']} with {result}")
        return "OK"

    def action_checksensors_all(self):
        self.action_checkdigitalsensors_all()
        #self.checktemp_humidity()

    def action_describesensors(self):
            for channel in botbrain_config.PINS.keys():
                print (f"{channel} is {botbrain_config.PINS[channel]['name']} at pin {botbrain_config.PINS[channel]['channel']}")


    def action_checklight(self):
        channel = 14
        water_sense = Pin(channel, Pin.IN)
        print(water_sense.value())
        if (water_sense.value()):
            result = "No light is detected"
            print(result)
            return result
        else:
            result = "Light is detected"
            print(result)
            return result

    def action_checktemp_humidity(self):
        pin = 2
        sensor = dht.DHT22(Pin(pin)) 
        sensor.measure()
        c_temp = sensor.temperature()
        temp = (c_temp * 1.8) + 32
        hum = sensor.humidity()
        result = "Temperature: {}°F   Humidity: {:.0f}% ".format(temp, hum)
        print(result)
        return(result)
        

    def dynamic_call(self, action):
        if hasattr(self, action) and callable(func := getattr(self,action)):
            return func()

