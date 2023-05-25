import network
import time
from machine import Pin
import machine
from umqtt.simple import MQTTClient
import random
import json
import botbrain_config


class Mqtt:

    def __init__(self, glog, api, bootstats = False):
        self.glog = glog
        self.api = api
        self.bootstats = bootstats
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
           
        digital_results = self.api.action_checkdigitalsensors_all()
     
        #If we have bootstats, add them to the return and syslog it.
        if self.bootstats:
            digital_results["bootstats"] = self.bootstats
            print(digital_results)
            self.glog.syslog_message(self.bootstats)
        
        temp_results = self.api.action_checktemp_humidity()

        
        prtg_results = digital_results.copy()
        prtg_results.update(temp_results)

        temp_results = self.api.action_get_external_temp()
        prtg_results.update(temp_results)
       
        
        
        j=json.dumps(prtg_results)
        
        client.publish(botbrain_config.MQTT_TOPIC, j, True, botbrain_config.MQTT_QOS)
        client.disconnect()
        
        #print(self.api.action_checktemp_humidity())
        
        if botbrain_config.MQTT_SHUTDOWN_AFTER_SEND:
            self.api.action_lpm0()
            machine.reset()
            


