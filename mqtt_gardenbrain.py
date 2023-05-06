import network
import time
from machine import Pin
import machine
from umqtt.simple import MQTTClient
import random
import json
import botbrain_config


class Mqtt:

    def __init__(self, glog, api):
        self.glog = glog
        self.api = api
        wlan = network.WLAN(network.STA_IF)
        
        self.glog.message("MQTT is waiting for network")
        while wlan.active() == False:
            self.glog.message("Waiting for AP to become active...")
            time.sleep(1)
            pass
        self.glog.message("MQTT now has network access. Sleeping for 20 seconds for stability...")
        time.sleep(20)
        self.glog.message("Now sending message")
        self.send_message()

    def send_message(self):
        client = MQTTClient(botbrain_config.MQTT_CLIENT_ID, botbrain_config.MQTT_BROKER, keepalive=botbrain_config.MQTT_KEEPALIVE)
        
        try:
            client.connect()
        except Exception as e:
            self.glog.syslog_message(f"Issue connecting to MQTT Broker! {e}")
            self.glog.message(f"Waiting 10 seconds before reboot...")
            time.sleep(10)
            machine.reset()
            return

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
        
        client.publish(botbrain_config.MQTT_TOPIC, j, True, botbrain_config.MQTT_QOS)
        client.disconnect()
        
        if botbrain_config.MQTT_SHUTDOWN_AFTER_SEND:
            self.api.action_lpm0()
            
