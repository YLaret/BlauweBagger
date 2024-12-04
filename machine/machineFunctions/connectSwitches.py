# tuya library
import tinytuya
# database package
import sqlite3

def connectSwitches():
	# connect to database
	db = sqlite3.connect('../data/machine.db')

	# get the switch data
	switchdata = db.execute('SELECT * FROM switches').fetchall()

	# connect to the tuya switches
	switches = []
	for switch in switchdata:
		switches.append(tinytuya.OutletDevice(dev_id=switch[0],address=switch[1],local_key=switch[2], version=3.3)

	return switches
