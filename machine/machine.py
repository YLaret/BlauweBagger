# local functions
import machineFunctions as mF
# date and time functions
import datetime
# database library
import sqlite3
# sleep library
import time

# initial startTime
startTime = datetime.datetime.now()

switchData = mF.getTable("SWITCH",0)
switches = mF.connectSwitches(switchData)
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
    
    
    ###################
    ### LOGIC PHASE ###
    ###################
    ### CONNECT SWITCHES
    #switches = mF.connectSwitches(switchData)

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
              
    ### READ METERS
    meters = mF.readFlowSensor()
    
    ### CONTROL SWITCHES
    # if no full stop control turn on/off preferred switches
    activeSwitches = []
    if currentStage != 0:
        activeSwitches = [int(item) for item in stageData[currentStage-1]["SwitchIDS"].split(',')]
    if currentStage == 0:
        print("Turning off all switches")
        mF.shutDownSwitches(switches,switchData)
    else:
        for i,switch in enumerate(switches):
            TiD = 1
            if switchData[i]["TuyaVersion"] == 3.3:
                TiD = 1
            elif switchData[i]["TuyaVersion"] == 3.4:
                TiD = 17
            if i+1 in activeSwitches:
                print("Turning on switch: " + str(i+1))
                switch.set_value(TiD,True,nowait=True)
            else:
                print("Turning off switch: " + str(i+1))
                switch.set_value(TiD,False,nowait=True)
   
    ### CALCULATE LOOP TIME
    loopTime = (datetime.datetime.now() - startTime).total_seconds()
    startTime = datetime.datetime.now()
   
    ###################
    ### WRITE PHASE ###
    ###################
    # connect database
    db = sqlite3.connect('../data/machine.db', timeout=5)
    if (pause == 0):
        if stageTime < programRunTime:
            print("Finished program!")
            db.execute('UPDATE MACHINESTATUS SET Pause = 2')
        else:
            db.execute('UPDATE MACHINESTATUS SET ProgramRunTime = ' + str(programRunTime + loopTime))
    for i,meter in enumerate(meterData):
        db.execute('UPDATE METER SET Value = ' +str(meters[i]) +' WHERE MeterID = '+str(meter["MeterID"]))
    
    db.commit()
    db.close()
    
    ###################
    ### SLEEP PHASE ###
    ###################
    time.sleep(0.5)
            
        

    
    
    
    
    
    
    
