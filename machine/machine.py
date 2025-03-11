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
#########################
### MAIN MACHINE LOOP ###
#########################
while True:
    ###################
    ### READ PHASE ####
    ###################
    
    # connect database
    db = sqlite3.connect('../data/machine.db', timeout=5)
    switchData = db.execute('SELECT * FROM SWITCH').fetchall()
    db.close()
    machineStatusData = mF.getTable("MACHINESTATUS",0)
    programData = mF.getTable("PROGRAM",0)
    deviceData = mF.getTable("DEVICE",0)
    meterData = mF.getTable("METER",0)
    stageData = mF.getTable("STAGE",0)
    
    
    ###################
    ### LOGIC PHASE ###
    ###################
    ### CONNECT SWITCHES
    switches = mF.connectSwitches(switchData)

    ### GET MACHINE STATUS
    # extract current program
    programID = int(machineStatusData[0])
    # extract pause variable from machine status
    pause = int(machineStatusData[1])
    # extract program run time in seconds
    programRunTime = machineStatusData[2]

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
        stages = [int(item) for item in programData[programID-1][3].split(',')]
        stageTime = 0
        for stage in stages:
            stageTime = stageTime + stageData[stage-1][3]
            if stageTime > programRunTime:
                currentStage = stage
                break
              
    ### READ METERS
    #*#* TO DO *#*#
    
    ### CONTROL SWITCHES
    # if no full stop control turn on/off preferred switches
    if currentStage == 0:
        mF.shutDownSwitches()
    else:
        for i,switch in enumerate(switches):
            if i+1 in [int(item) for item in stageData[currentStage-1][2].split(',')]:
                switch.turn_on()
            else:
                switch.turn_off()
   
    ### CALCULATE LOOP TIME
    loopTime = (datetime.datetime.now() - startTime).total_seconds()
    startTime = datetime.datetime.now()
   
    ###################
    ### WRITE PHASE ###
    ###################
    # connect database
    db = sqlite3.connect('../data/machine.db', timeout=5)
    db.execute('UPDATE MACHINESTATUS SET ProgramRunTime = ' + str(programRunTime + loopTime))
    db.commit()
    db.close()
    
    ###################
    ### SLEEP PHASE ###
    ###################
    time.sleep(0.5)
            
        

    
    
    
    
    
    
    
