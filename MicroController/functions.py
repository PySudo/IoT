from machine import Pin
from network import WLAN
try:
    from requests import get
except:
    from urequests import get

def ConnectToNetwork(SSID, Password):
    sta_if = WLAN(WLAN.IF_STA)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(SSID, Password)
        while not sta_if.isconnected():
            pass

class ManagePins:
    def __init__(self, API_URL, API_KEY):
        self.API = API_URL if API_URL[-1] == '/' else API_URL+'/'
        self.KEY = API_KEY
        self.pins = dict()

    def AddPin(self, GPIO):
        Pin(GPIO, Pin.OUT)
        self.pins[GPIO] = 0
    
    def RemovePin(self, GPIO):
        del self.pins[GPIO]
        Pin(GPIO).off()

    def ChangeValue(self, GPIO, value=False):
        Pin(GPIO).value(value)
        self.pins[GPIO] = value

    def GetPinsFromAPI(self):
        try:
            check_list = list()
            result = get(self.API+'GetPins?key='+self.KEY).json()
            print(result)
            if result['ok']:
                for GPIO, value in result['result'].items():
                    GPIO = int(GPIO)
                    check_list.append(GPIO)

                    if not GPIO in self.pins:
                        self.AddPin(GPIO)
                        self.ChangeValue(value)
                    elif self.pins[GPIO] != value:
                        self.ChangeValue(GPIO, value)

                for i in [i for i in self.pins if not i in check_list]:
                    self.RemovePin(i)
        except:
            pass
