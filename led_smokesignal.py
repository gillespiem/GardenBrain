import machine
import time
import random

class LEDSmokeSignal:

    def __init__(self, glog):
        self.glog = glog

    def blink_eyes(self):
        left_red = machine.Pin(13, machine.Pin.OUT)
        left_blue = machine.Pin(14, machine.Pin.OUT)
        left_green = machine.Pin(15, machine.Pin.OUT)
        
        right_red = machine.Pin(16, machine.Pin.OUT)
        right_blue = machine.Pin(17, machine.Pin.OUT)
        right_green = machine.Pin(18, machine.Pin.OUT)

        for i in range(0, 50):
            red = random.randint(0,1)
            blue = random.randint(0,1)
            green = random.randint(0,1)

            self.glog.message("Blinking eyes")
            left_red.value(red)
            left_blue.value(blue)
            left_green.value(green)

            right_red.value(red)
            right_blue.value(blue)
            right_green.value(green)
            time.sleep(0.25)

            self.glog.message("Closing eyes")
            left_red.on()
            left_blue.on()
            left_green.on()

            right_red.on()
            right_blue.on()
            right_green.on()
        


    def blink(self, delay = 0.25, count = 10):
        led = machine.Pin("LED", machine.Pin.OUT)
        for i in range (0,count):
            self.glog.message("Blink on")
            led.on()
            time.sleep(delay)
            led.off()
            time.sleep(delay)
            self.glog.message("Blink off")
        self.blink_eyes()

    def on(self):
        led = machine.Pin("LED", machine.Pin.OUT)
        led.on()
        
    def off(self):
        led = machine.Pin("LED", machine.Pin.OUT)
        led.off()

