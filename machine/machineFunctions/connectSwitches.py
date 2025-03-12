# tuya library
import tinytuya
# database package
import sqlite3

def connectSwitches(switchData):
    # connect to the tuya switches
    switches = []
    for switch in switchData:
        switches.append(tinytuya.OutletDevice(dev_id=switch["TuyaID"],address=switch["IPAddress"],local_key=switch["LocalKey"], version=switch["TuyaVersion"]))
        switches.append(switch)
    # return the tuya connected switches
    return switches
