from api_handler import Api_handler
import json

class Api_handler_botbrain(Api_handler):
    def __init__(self):
        self.set_name("botbrain")
        print ("Now initiating %s" % self.get_name())
        print(self.get_api_methods())

    def action_lpm0(self):
        print("Going to LPM0")

    def action_lpm1(self):
        print("Going to LPM1")

    def action_lpm2(self):
        print("Going to LPM2")

    def action_lpm3(self):
        print("Going to LPM3")

    def action_reboot(self):
        print("Rebooting")

    def action_flashled(self):
        print("Now flashing led for 5 seconds")


#it = Api_handler_botbrain()
#it.action_lpm0()
