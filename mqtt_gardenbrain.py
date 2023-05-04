import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
import random
import json
import botbrain_config


class Mqtt:

    def __init__(self, glog, api):
        self.glog = glog
        self.api = api
        wlan = network.WLAN(network.STA_IF)
        
        glog.message("MQTT is waiting for network")
        while wlan.active() == False:
            glog.message("Waiting for AP to become active...")
            time.sleep(1)
            pass
        glog.message("MQTT now has network access")
        time.sleep(1)
        glog.message("Now sending message")
        self.send_message()
        
    def OFFsend_message(self):
        client = MQTTClient(botbrain_config.MQTT_CLIENT_ID, botbrain_config.MQTT_BROKER, keepalive=botbrain_config.MQTT_KEEPALIVE)
        client.connect()

        current_time = f"{time.localtime()[0]}-{time.localtime()[1]}-{time.localtime()[2]:02d} {time.localtime()[3]:02d}:{time.localtime()[4]:02d}:{time.localtime()[5]:02d}"

        r = random.randint(1,1000)
        dictionary = {"temperature": r, "name": "current_temp", "time": current_time}
        d = {"Sensor1" : dictionary}
        j=json.dumps(d)
        client.publish("house/main-light", j)
        
        if botbrain_config.MQTT_SHUTDOWN_AFTER_SEND:
            self.glog.message("Going to LPM0")
            self.glog.message(f"LMP0 Time {time.localtime()[0]}-{time.localtime()[1]}-{time.localtime()[2]} {time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}")
            time.sleep(1)
            sensor = Pin(19, Pin.OUT)
            sensor.value(1)
            

    def send_message(self):
        client = MQTTClient(botbrain_config.MQTT_CLIENT_ID, botbrain_config.MQTT_BROKER, keepalive=botbrain_config.MQTT_KEEPALIVE)
        client.connect()

        current_time = f"{time.localtime()[0]}-{time.localtime()[1]}-{time.localtime()[2]:02d} {time.localtime()[3]:02d}:{time.localtime()[4]:02d}:{time.localtime()[5]:02d}"
        prtg_results = {}

        for channel in botbrain_config.PINS.keys():
            if botbrain_config.PINS[channel]["type"] == "digital":
                print(f"Now testing {channel}")
                result = self.api.action_checkdigitalsensor(botbrain_config.PINS[channel]["channel"])
                
                print (f"{channel} is {botbrain_config.PINS[channel]['name']} at pin {botbrain_config.PINS[channel]['channel']} and {result['human_readable']}")
                
                p_result = {}
                p_result["channel"] = f"{channel}-{botbrain_config.PINS[channel]['name']}"
                p_result["value"] = result["value"]
                p_result["time"] = current_time
          
                prtg_results[channel] = p_result
                print(prtg_results)
            
                j=json.dumps(prtg_results)
                client.publish("Gardenbrain/digital_sensors", j, True, 1)
        
        if True:
            self.glog.message("Going to LPM0")
            self.glog.message(f"LMP0 Time {time.localtime()[0]}-{time.localtime()[1]}-{time.localtime()[2]} {time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}")
            time.sleep(1)
            sensor = Pin(19, Pin.OUT)
            sensor.value(1)
