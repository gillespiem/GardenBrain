import machine
import time

class LEDSmokeSignal:

    def __init__(self, glog):
        self.glog = glog

    def blink(self, delay = 0.25, count = 10):
        led = machine.Pin("LED", machine.Pin.OUT)
        for i in range (0,count):
            self.glog.message("Blink on")
            led.on()
            time.sleep(delay)
            led.off()
            time.sleep(delay)
            self.glog.message("Blink off")

    def on(self):
        led = machine.Pin("LED", machine.Pin.OUT)
        led.on()
        
    def off(self):
        led = machine.Pin("LED", machine.Pin.OUT)
        led.off()
