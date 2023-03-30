import network
import machine
import botbrain_config
import time
import led_smokesignal


class Wifi:

    def __init__(self):
        
        led_smokesignal.blink(0.05,50)

        if botbrain_config.WIFI_MODE == "ap":
            print("Setting up system as AP")
            self.ap = network.WLAN(network.AP_IF)
            self.ap.active(True)
            self.ap.config(essid=botbrain_config.WIFI_SSID, password=botbrain_config.WIFI_PASSWORD)
        else:
            print("Setting up system as STA")
            self.ap = network.WLAN(network.STA_IF)
            self.ap.active(True)
            self.ap.connect(botbrain_config.WIFI_SSID, botbrain_config.WIFI_PASSWORD)

        while self.ap.active() == False:
            print("Waiting for AP to become active...")
            #led_smokesignal.blink()
            time.sleep(1)
            pass

        
        led_smokesignal.on()

        print("Access Point is established")
        time.sleep(5)
        
        while self.ap.isconnected() == False:
            print("Waiting for connection...")
            led_smokesignal.blink(1, 5)
            ip = self.ap.ifconfig()
            for scan in self.ap.scan():
                rssi = scan[3]
                ssid = scan[0].decode('utf-8')
                print(f"{ssid} has signal {rssi}")
                if ssid == botbrain_config.WIFI_SSID:
                    print("We have found the SSID we are supposed to connect to")
                    led_smokesignal.blink(0.10, 20)
                    time.sleep(1)
                    if abs(rssi) > 90:
                        print("Signal bad")
                        led_smokesignal.blink(2, 1)
                    elif abs(rssi) >70:
                        print("Signal ok")
                        led_smokesignal.blink(2, 2)
                    elif abs(rssi) >50:
                        print("Signal good")
                        led_smokesignal.blink(2, 3)
                    elif abs(rssi) > 0:
                        print("Signal great")
                        led_smokesignal.blink(2, 4)
                    
            led_smokesignal.off()
            time.sleep(5)
            
        print(self.ap.ifconfig())



    def get_ifconfig(self):
        return self.ap.ifconfig()


