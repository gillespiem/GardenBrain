import machine
import time

def blink(delay = 0.25, count = 10):
    led = machine.Pin("LED", machine.Pin.OUT)
    for i in range (0,count):
        print("Blink on")
        led.on()
        time.sleep(delay)
        led.off()
        time.sleep(delay)
        print("blink off")

def on():
    led = machine.Pin("LED", machine.Pin.OUT)
    led.on()
    
def off():
    led = machine.Pin("LED", machine.Pin.OUT)
    led.off()
