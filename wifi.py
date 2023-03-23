import network
import machine
import botbrain_config
import time

class Wifi:

    def __init__(self):

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
            time.sleep(1)
            pass

        led = machine.Pin("LED", machine.Pin.OUT)
        led.on()

        print("Access Point is established")
        time.sleep(5)
        print(self.ap.ifconfig())

    def get_ifconfig(self):
        return self.ap.ifconfig()

