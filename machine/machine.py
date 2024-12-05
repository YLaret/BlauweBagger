# local functions
import machineFunctions as mF

# date and time functions
import datetime

# initial connection to switches
switches = mF.connectSwitches()

# initial startTime
startTime = datetime.datetime.now()

while True:
    # ensure connection to switches
    switches = mF.connectSwitches()

    # run only if the program is started
    if mF.programStart():
        # update startTime if not running already
        startTime = mF.updateStartTime(startTime)

        # write the preferred state of the switches
        mF.writePrefStateSwitches(switches,startTime)
    else:
        print("Machine ready ....")
        
        # shutdown all switches, disabled for test
        #mF.shutDownSwitches(switches)

        # update running status
        mF.updateRunningStop()
