from api_handler import Api_handler
import json
from machine import Pin
import machine
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
        machine.reset()

    def action_flashled(self):
        print("Now flashing led for 5 seconds")
    
    def action_checkdigitalsensor(self, channel = 15):
        sensor = Pin(channel, Pin.IN)
        sensor_value = sensor.value()
        gpio_name = f"GPIO{channel:02}"
        
        result = {}
        if (sensor_value):
            result["value"] = sensor_value
            result["human_readable"] = botbrain_config.PINS[gpio_name]["human_readable"][sensor_value]
            print(result)
            return result
        else:
            result["value"] = sensor_value
            result["human_readable"] = botbrain_config.PINS[gpio_name]["human_readable"][sensor_value]
            print(result)
            return result

    def action_checkdigitalsensors_all(self):
        
        prtg_results = {}
        prtg_results["prtg"] = {}
        prtg_results["prtg"]["result"] = []
        
        for channel in botbrain_config.PINS.keys():
            if botbrain_config.PINS[channel]["type"] == "digital":
                print(f"Now testing {channel}")
                result = self.action_checkdigitalsensor(botbrain_config.PINS[channel]["channel"])
                print (f"{channel} is {botbrain_config.PINS[channel]['name']} at pin {botbrain_config.PINS[channel]['channel']} and {result['human_readable']}")
                
                p_result = {}
                p_result["channel"] = f"{channel}-{botbrain_config.PINS[channel]['name']}"
                p_result["value"] = result["value"]
                p_result["integer"] = 1
                prtg_results["prtg"]["result"].append(p_result)
                               
        
        return prtg_results

    def merge_dicts(self, dict1, dict2):
        return (dict2.update(dict1))

    def action_checksensors_all(self):
        digital_results = self.action_checkdigitalsensors_all()
        analog_results = self.action_checktemp_humidity()
        results = self.merge_dicts(digital_results, analog_results)
        print(digital_results)
        print(analog_results)
        print("\n")
        
        #We merged the dicts together...
        return analog_results

    def action_describesensors(self):
            for channel in botbrain_config.PINS.keys():
                print (f"{channel} is {botbrain_config.PINS[channel]['name']} at pin {botbrain_config.PINS[channel]['channel']}")


    def action_checklight(self):
        channel = 11
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
        pin = 12
        
        prtg_results = {}
        prtg_results["prtg"] = {}
        prtg_results["prtg"]["result"] = []
        
        try: 
            sensor = dht.DHT22(Pin(pin)) 
            sensor.measure()
            c_temp = sensor.temperature()
            temp = (c_temp * 1.8) + 32
            hum = sensor.humidity()
            result = "Temperature: {}°F   Humidity: {:.0f}% ".format(temp, hum)
            
            p_result = {}
            p_result["channel"] = f"GPIO12-{botbrain_config.PINS['GPIO12']['name']}-Temp"
            p_result["value"] = temp
            p_result["float"] = 1
            prtg_results["prtg"]["result"].append(p_result)
            
            p_result = {}
            p_result["channel"] = f"GPIO12-{botbrain_config.PINS['GPIO12']['name']}-Humidity"
            p_result["value"] = hum
            p_result["float"] = 1
            prtg_results["prtg"]["result"].append(p_result)
            
        except Exception as e:
            print(e)
            result = "Issue Detected"
            
            prtg_results = {}
            prtg_results["prtg"] = {}
            prtg_results["prtg"]["error"] = 1
            prtg_results["prtg"]["text"] = "Issue detected."
            return prtg_results
            
        
        return prtg_results
        

    def dynamic_call(self, action):
        if hasattr(self, action) and callable(func := getattr(self,action)):
            return func()
        else:
            return False
