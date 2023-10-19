import sys
import botbrain_config
from api_handler_gardenbrain import Api_handler_gardenbrain
from gardenlog import GardenLog
import time

glog = GardenLog()
api = Api_handler_gardenbrain(glog)

prtg_results = {}

current_time = f"{time.localtime()[0]}-{time.localtime()[1]}-{time.localtime()[2]:02d} {time.localtime()[3]:02d}:{time.localtime()[4]:02d}:{time.localtime()[5]:02d}"

for channel in botbrain_config.PINS.keys():
    if botbrain_config.PINS[channel]["type"] == "digital":
        print(f"Now testing {channel}")
        result = api.action_checkdigitalsensor(botbrain_config.PINS[channel]["channel"])
        
        print (f"{channel} is {botbrain_config.PINS[channel]['name']} at pin {botbrain_config.PINS[channel]['channel']} and {result['human_readable']}")
        
        p_result = {}
        p_result["channel"] = f"{channel}-{botbrain_config.PINS[channel]['name']}"
        p_result["value"] = result["value"]
        p_result["time"] = current_time
  
        prtg_results[channel] = p_result
        print(prtg_results)
        
