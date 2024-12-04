# local functions
import machineFunctions as mF

# date and time functions
import datetime

# initial connection to switches
switches = mF.connectSwitches()

# notate the starting time of the machine (should be the program, we will get to that)
startTime = datetime.datetime.now()

while True:
	# ensure connection to switches
	switches = mF.connectSwitches()

	# write the preferred state of the switches
	mF.writePrefStateSwitches(switches,startTime)
