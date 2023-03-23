from botweb_server import BotwebServer
from api_handler_gardenbrain import Api_handler_gardenbrain
from wifi import Wifi
from machine import Pin
import time




if __name__ == "__main__":
    wifi = Wifi()
    api = Api_handler_gardenbrain()
    webserver = BotwebServer(api)
