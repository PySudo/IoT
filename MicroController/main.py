from functions import *
from time import sleep

SSID     = '...'
Password = '...'
API_URL  = '...'
API_KEY  = '...'

ConnectToNetwork(SSID, Password)

pin = ManagePins(API_URL, API_KEY)
while not sleep(1):
    pin.GetPinsFromAPI()