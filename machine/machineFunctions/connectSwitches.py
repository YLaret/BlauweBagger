# tuya library
import tinytuya
# database package
import sqlite3

def connectSwitches(switchData):
    # connect to the tuya switches
    switches = []
    for switch in switchData:
        switches.append(tinytuya.OutletDevice(dev_id=switch[2],address=switch[3],local_key=switch[4], version=switch[5]))
        switches.append(switch)
    # return the tuya connected switches
    return switches
