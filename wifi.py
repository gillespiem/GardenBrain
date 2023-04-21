import network
import machine
import botbrain_config
import time
from led_smokesignal import LEDSmokeSignal

class Wifi:

    def __init__(self, glog):
        
        self.glog = glog
        
        led_smokesignal = LEDSmokeSignal(glog)
        
        led_smokesignal.blink(0.05,50)

        if botbrain_config.WIFI_MODE == "ap":
            self.glog.message("Setting up system as AP")
            self.ap = network.WLAN(network.AP_IF)
            self.ap.active(True)
            self.ap.config(essid=botbrain_config.WIFI_SSID, password=botbrain_config.WIFI_PASSWORD)
        else:
            self.glog.message("Setting up system as STA")
            self.ap = network.WLAN(network.STA_IF)
            self.ap.active(True)
            self.ap.connect(botbrain_config.WIFI_SSID, botbrain_config.WIFI_PASSWORD)

        while self.ap.active() == False:
            self.glog.message("Waiting for AP to become active...")
            #led_smokesignal.blink()
            time.sleep(1)
            pass

        
        led_smokesignal.on()

        self.glog.message("Access Point is established")
        time.sleep(5)
        
        wifi_connect_attempts = 0
        while self.ap.isconnected() == False:
            wifi_connect_attempts += 1
            self.glog.message("Connection attempt #%d" % wifi_connect_attempts)
            if wifi_connect_attempts > 5:
                self.glog.message("Now rebooting myself")
                self.glog.close()
                machine.reset()
            self.glog.message("Waiting for connection...")
            led_smokesignal.blink(1, 5)
            ip = self.ap.ifconfig()
            for scan in self.ap.scan():
                rssi = scan[3]
                ssid = scan[0].decode('utf-8')
                self.glog.message(f"{ssid} has signal {rssi}")
                if ssid == botbrain_config.WIFI_SSID:
                    self.glog.message("We have found the SSID we are supposed to connect to")
                    led_smokesignal.blink(0.10, 20)
                    time.sleep(1)
                    if abs(rssi) > 90:
                        self.glog.message("Signal bad")
                        led_smokesignal.blink(2, 1)
                    elif abs(rssi) >70:
                        self.glog.message("Signal ok")
                        led_smokesignal.blink(2, 2)
                    elif abs(rssi) >50:
                        self.glog.message("Signal good")
                        led_smokesignal.blink(2, 3)
                    elif abs(rssi) > 0:
                        self.glog.message("Signal great")
                        led_smokesignal.blink(2, 4)
                    
            led_smokesignal.off()
            time.sleep(5)
            
        self.glog.message(self.ap.ifconfig())



    def get_ifconfig(self):
        return self.ap.ifconfig()

    def get_status(self):
        return self.ap.isconnected()