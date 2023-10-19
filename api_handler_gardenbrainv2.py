from api_handler import Api_handler
import json
from machine import Pin
import machine
import onewire
import ds18x20
import dht
import botbrain_config

import time
import ntptime

#This is version 2 of the API handler. It's goal is to abstract the data. We will add a layer to convert from this to PRTG format in the future
class Api_handler_gardenbrain(Api_handler):

    def __init__(self, glog):
        self.set_name("botbrain")
        self.VERSION=2.0
        self.glog = glog
        self.glog.message("Now initiating %s" % self.get_name())
        self.glog.message(self.get_api_methods())

        #Set the LPM0 pin to off.
        self.action_lpm0(False)

    def action_lpm0(self, lpm0_on = True):
        if not lpm0_on:
            self.glog.message("DISABLING LPM0")
            sensor = Pin(19, Pin.OUT)
            sensor.value(0)
        else:    
            self.glog.syslog_message("Going to LPM0")
            self.glog.message(f"LMP0 Time {time.localtime()[0]}-{time.localtime()[1]}-{time.localtime()[2]}-{time.localtime()[3]}-{time.localtime()[4]}-{time.localtime()[5]}")
            time.sleep(1)
            sensor = Pin(19, Pin.OUT)
            sensor.value(1)  

    def action_lpm1(self):
        self.glog.message("Going to LPM1")

    def action_lpm2(self):
        self.glog.message("Going to LPM2")

    def action_lpm3(self):
        self.glog.message("Going to LPM3")

    def action_reboot(self):
        self.glog.syslog_message("Rebooting")
        machine.reset()

    def action_flashled(self):
        self.glog.message("Now flashing led for 5 seconds")
    
    def action_checkdigitalsensor(self, channel = 15):
        sensor = Pin(channel, Pin.IN)
        sensor_value = sensor.value()
        gpio_name = f"GPIO{channel:02}"
        
        result = {}
        if (sensor_value):
            result["value"] = sensor_value
            result["human_readable"] = botbrain_config.PINS[gpio_name]["human_readable"][sensor_value]
            self.glog.message(result)
            return result
        else:
            result["value"] = sensor_value
            result["human_readable"] = botbrain_config.PINS[gpio_name]["human_readable"][sensor_value]
            self.glog.message(result)
            return result

    def action_checkdigitalsensors_all(self):
        
        current_time = f"{time.localtime()[0]}-{time.localtime()[1]}-{time.localtime()[2]:02d} {time.localtime()[3]:02d}:{time.localtime()[4]:02d}:{time.localtime()[5]:02d}"
        prtg_results = {}
        for channel in botbrain_config.PINS.keys():
            if botbrain_config.PINS[channel]["type"] == "digital":
                
                print(f"Now testing {channel}")
                result = self.action_checkdigitalsensor(botbrain_config.PINS[channel]["channel"])
                
                print (f"{channel} is {botbrain_config.PINS[channel]['name']} at pin {botbrain_config.PINS[channel]['channel']} and {result['human_readable']}")
                
                
                p_result = {}
                p_result["channel"] = f"{channel}-{botbrain_config.PINS[channel]['name']}"
                p_result["value"] = result["value"]
                p_result["time"] = current_time
          
                prtg_results[channel] = p_result
        return prtg_results

    def merge_dicts(self, dict1, dict2):
        return (dict2.update(dict1))

    def action_get_external_temp(self, channel):
        print("NOW IN EXT TEMP FUNC")
        prtg_results = {}
        current_time = f"{time.localtime()[0]}-{time.localtime()[1]}-{time.localtime()[2]:02d} {time.localtime()[3]:02d}:{time.localtime()[4]:02d}:{time.localtime()[5]:02d}"
        ds_pin = machine.Pin(channel) 
        ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
        roms = ds_sensor.scan()
        
        if roms:
            self.glog.message('Found DS devices: %s' % roms)
            print("Found DS Devices: ", roms)
            ds_sensor.convert_temp()
            time.sleep_ms(750)
            for rom in roms: 
                print(rom)
                c = ds_sensor.read_temp(rom)
                f = (c * 9/5) + 32
        else:
            self.glog.message("No ROMs found")
            f = -1
        
        p_result = {}
        #p_result["channel"] = f"GPIO{channel:02}-{botbrain_config.PINS['GPIO{channel:02}']['human_readable']}"
        p_result["channel"] = "%s-%s" % (f"GPIO{channel:02}", botbrain_config.PINS[f'GPIO{channel:02}']['human_readable'])
        p_result["value"] = f
        p_result["time"] = current_time
        prtg_results[f"GPIO{channel:02}"] = p_result
        print(prtg_results)
        return prtg_results
         

    def action_checksensors_all(self):
        digital_results = self.action_checkdigitalsensors_all()
        analog_results = self.action_checktemp_humidity()
        external_temp_results = self.action_get_external_temp(22)
        soil_temp_results = self.action_get_external_temp(6)
        
        first_results = self.merge_dicts(digital_results, analog_results)
        second_results = self.merge_dicts(external_temp_results, first_results)
        results = self.merge_dicts(soil_temp_results, second_results)
        
        self.glog.message(digital_results)
        self.glog.message(analog_results)
        
        #We merged the dicts together...
        return analog_results

    def action_describesensors(self):
            for channel in botbrain_config.PINS.keys():
                self.glog.message (f"{channel} is {botbrain_config.PINS[channel]['name']} at pin {botbrain_config.PINS[channel]['channel']}")


    def action_checklight(self):
        channel = 11
        water_sense = Pin(channel, Pin.IN)
        self.glog.message(water_sense.value())
        if (water_sense.value()):
            result = "No light is detected"
            self.glog.message(result)
            return result
        else:
            result = "Light is detected"
            self.glog.message(result)
            return result

    def action_checktemp_humidity(self):
        pin = 12
        
        current_time = f"{time.localtime()[0]}-{time.localtime()[1]}-{time.localtime()[2]:02d} {time.localtime()[3]:02d}:{time.localtime()[4]:02d}:{time.localtime()[5]:02d}"
        
        prtg_results = {}
        prtg_results["GPIO12Temp"] = {}
        prtg_results["GPIO12Humidity"] = {}
        #prtg_results["prtg"]["result"] = []
        
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
            p_result["time"] = current_time
            prtg_results["GPIO12Temp"]= p_result
            
            p_result = {}
            p_result["channel"] = f"GPIO12-{botbrain_config.PINS['GPIO12']['name']}-Humidity"
            p_result["value"] = hum
            p_result["float"] = 1
            prtg_results["GPIO12Humidity"]= p_result
            
        except Exception as e:
            self.glog.message(e)
            result = "Issue Detected"
            
            #prtg_results = {}
            #prtg_results["prtg"] = {}
            #prtg_results["prtg"]["error"] = 1
            #prtg_results["prtg"]["text"] = "Issue detected."
            p_result = {}
            p_result["value"] = -1
            p_result["text"] = "Issue Detected"
            
            prtg_results["GPIO12Temp"] = p_result
            prtg_results["GPIO12Humidity"] = p_result
            return prtg_results
            
        
        return prtg_results
        
    def action_simulated_crash(self):
        raise Exception("Simulated crash")

    def action_pull_logs(self):
       return self.glog.display()

    def action_get_time(self):
        print(time.localtime())

    def dynamic_call(self, action):
        if hasattr(self, action) and callable(func := getattr(self,action)):
            return func()
        else:
            return False
