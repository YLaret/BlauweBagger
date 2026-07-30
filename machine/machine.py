# local functions
import machineFunctions as mF
# date and time functions
import datetime
# database library
import sqlite3
# sleep library
import time

# loggin
import logging
import os

### ONLY VARS TO CHANGE ###
# time the loop sleeps
snooze = 0.5
# interval between sending data to the tuya switches
# 10s works, 3s not, perhaps 6s works too
switchInterval = 0.5;
meterLogInterval = 1;

# special unloading var
uLoad = 0

# special suspend var (to pause cyclone until kfp is unloaded)
suspend = 0

# initial startTime and switchTime
startTime = datetime.datetime.now()
switchTime = datetime.datetime.now() - datetime.timedelta(seconds=switchInterval)
meterLogTime = datetime.datetime.now() - datetime.timedelta(seconds=switchInterval)

# setup logging
mF.setupLogging()

### CONNECT SWITCHES
switchData = mF.getTable("SWITCH",0)
#switches = mF.connectSwitches(switchData)

###########################
### FORCE STOP ON START ###
###########################
# connect database
db = sqlite3.connect('../data/machine.db', timeout=5)
# force stop status
db.execute('UPDATE MACHINESTATUS SET Pause = 2')
db.commit()
db.close()

#########################
### MAIN MACHINE LOOP ###
#########################
while True:
    ###################
    ### READ PHASE ####
    ###################
    # connect database
    #switchData = mF.getTable("SWITCH",0)
    machineStatusData = mF.getTable("MACHINESTATUS",0)
    programData = mF.getTable("PROGRAM",0)
    deviceData = mF.getTable("DEVICE",0)
    meterData = mF.getTable("METER",0)
    stageData = mF.getTable("STAGE",0)
    forceData = mF.getTable("FORCE",0)
    meterRulesData = mF.getTable("METERRULES",0)
    
    
    ###################
    ### LOGIC PHASE ###
    ###################

    ### GET MACHINE STATUS
    # extract current program
    programID = int(machineStatusData[0]["ProgramID"])
    # extract pause variable from machine status
    pause = int(machineStatusData[0]["Pause"])
    # extract program run time in seconds
    programRunTime = machineStatusData[0]["ProgramRunTime"]

    print("ProgramID: " + str(programID) + " Pause: " + str(pause) + " ProgramRunTime: " + str(programRunTime))

    ### FIND CURRENT STAGE
    # currentStage variable (0 if no stage => full stop)
    currentStage = 0
    # if program paused allow manual control
    if pause == 1:
        # special manual stage
        currentStage = 1
    # else if program running normally
    elif pause == 0:
        # calculate currentStage based on run time
        pstages = [int(item) for item in programData[programID-1]["StageIDS"].split(',')]
        stageTime = 0
        for stage in pstages:
            stageTime = stageTime + stageData[stage-1]["Time"]
            if stageTime > programRunTime:
                currentStage = stage
                break
    elif pause == 14:
        if uLoad == 0:
            # special auto stage
            currentStage = 2
        elif uLoad == 1:
        # calculate currentStage based on run time
            pstages = [int(item) for item in programData[0]["StageIDS"].split(',')]
            stageTime = 0
            for stage in pstages:
                stageTime = stageTime + stageData[stage-1]["Time"]
                if stageTime > programRunTime:
                    currentStage = stage
                    break

    ### READ METERS
    # disable meter reading for dev
    meters = mF.readFlowSensor()
    #meters = [123,456,789,123] # Flow hydro, flow pers, pers druk
    meters.append(mF.getValueGPIO(13)) # Mix Vol
    meters.append(mF.getValueGPIO(12)) # Mix Leeg
    meters.append(mF.getValueGPIO(11)) # Vuil Vol
    meters.append(mF.getValueGPIO(10)) # Vuil Leeg
    meters.append(mF.getValueGPIO(9)) # Schoon Vol
    meters.append(mF.getValueGPIO(8)) # Schoon Leeg
    if meters[5] == 1:
        suspend = 1
    meters.append(suspend)

    print(meters)
    # log meter data
    if (datetime.datetime.now() - meterLogTime).total_seconds() >= meterLogInterval:
        logging.info(f"Meter values: {meters}")
        meterLogTime = datetime.datetime.now()
    
    ### CONTROL SWITCHES
    # if no full stop control turn on/off preferred switches
    activeSwitches = []
    if currentStage != 0 and currentStage != 2:
        activeSwitches = [int(item) for item in stageData[currentStage-1]["SwitchIDS"].split(',')]

    # meterrules for in auto
    if pause == 14:
        if uLoad == 0:
            for meterRule in meterRulesData:
                for meter in meterData:
                    if meterRule["MeterID"] == meter["MeterID"]:
                        if meterRule["MeterThresholdGEQ"]:
                            if meter["Value"] >= meterRule["MeterThreshold"]:
                                #pause = meterRule["Stage"]
                                if meterRule["SwitchBool"]:
                                    if meterRule["SwitchID"] not in activeSwitches:
                                        activeSwitches.append(meterRule["SwitchID"])
                                    if meterRule["SwitchID"] == -14:
                                        uLoad = 1
                                        programRunTime = 0
                                        pstages = [int(item) for item in programData[0]["StageIDS"].split(',')]
                                        stageTime = 0
                                        for stage in pstages:
                                            stageTime = stageTime + stageData[stage-1]["Time"]
                                            if stageTime > programRunTime:
                                                currentStage = stage
                                                break
                                else:
                                    if meterRule["SwitchID"] in activeSwitches:
                                        activeSwitches.remove(meterRule["SwitchID"])
                        else:
                            if meter["Value"] <= meterRule["MeterThreshold"]:
                                #pause = meterRule["Stage"]
                                if meterRule["SwitchBool"]:
                                    if meterRule["SwitchID"] not in activeSwitches:
                                        activeSwitches.append(meterRule["SwitchID"])
                                else:
                                    if meterRule["SwitchID"] in activeSwitches:
                                        activeSwitches.remove(meterRule["SwitchID"])
        elif uLoad == 1:
            activeSwitches = [int(item) for item in stageData[currentStage-1]["SwitchIDS"].split(',')]
            

    
    # send data to switches
    if (datetime.datetime.now() - switchTime).total_seconds() >= switchInterval:
        if currentStage == 0:
            print("Turning off all switches")
            mF.shutDownSwitchesGPIO(switchData)
        else:
            for i,switch in enumerate(switchData):
                if switchData[i]["SwitchID"] in activeSwitches:
                    print("Turning on switch: " + str(switchData[i]["SwitchID"]))
                    mF.setSwitchGPIO(switch["GPIO"],1)
                else:
                    print("Turning off switch: " + str(switchData[i]["SwitchID"]))
                    mF.setSwitchGPIO(switch["GPIO"],0)
        switchTime = datetime.datetime.now()
        # log switch data if controlled
        logSwitchIDS = activeSwitches
        if 0 in logSwitchIDS:
            logSwitchIDS.remove(0)
        logging.info(f"Active SwitchIDS: {logSwitchIDS}")
    
    ### CALCULATE LOOP TIME
    loopTime = (datetime.datetime.now() - startTime).total_seconds()
    startTime = datetime.datetime.now()
   
    ###################
    ### WRITE PHASE ###
    ###################
    # connect database
    db = sqlite3.connect('../data/machine.db', timeout=5)
    # update pause (changed by sensor)
    db.execute('UPDATE MACHINESTATUS SET Pause = ' + str(pause))
    # check if program finished
    if (pause == 0):
        if stageTime < programRunTime:
            print("Finished program!")
            db.execute('UPDATE MACHINESTATUS SET Pause = 2')
        else:
            db.execute('UPDATE MACHINESTATUS SET ProgramRunTime = ' + str(programRunTime + loopTime))
    elif (pause == 14):
        if activeSwitches:
            db.execute('UPDATE STAGE SET SwitchIDS="'+','.join(map(str,activeSwitches))+'" WHERE STAGE.StageID = 2')
        if uLoad == 1:
            if stageTime < programRunTime:
                print("Finished Unloading!")
                uLoad = 0
                suspend = 0
            else:
                db.execute('UPDATE MACHINESTATUS SET ProgramRunTime = ' + str(programRunTime + loopTime))
    # update meters
    for i,meter in enumerate(meterData):
        db.execute('UPDATE METER SET Value = ' +str(meters[i]) +' WHERE MeterID = '+str(meter["MeterID"]))
    db.execute('UPDATE FORCE SET SwitchIDS = 0')
    
    # if cyclone on
    if 4 in activeSwitches:
        db.execute('UPDATE CONTROL SET cyclOn=1 WHERE ControlID = 1')
    else:
        db.execute('UPDATE CONTROL SET cyclOn=0 WHERE ControlID = 1')
    
    db.commit()
    db.close()
    
    ###################
    ### SLEEP PHASE ###
    ###################
    time.sleep(snooze)
