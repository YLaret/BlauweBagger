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
    programID = int(machineStatusData[0]["ProgramID"])
    # extract pause variable from machine status
    pause = int(machineStatusData[0]["Pause"])
    # extract program run time in seconds
    programRunTime = machineStatusData[0]["ProgramRunTime"]

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
        pstages = [int(item) for item in programs[programID-1]["StageIDS"].split(',')]
        stageTime = 0
        for stage in pstages:
            stageTime = stageTime + stages[stage-1]["Time"]
            if stageTime > programRunTime:
                currentStage = stage
                break
              
    ### READ METERS
    #*#* TO DO *#*#
    
    ### CONTROL SWITCHES
    # if no full stop control turn on/off preferred switches
    activeSwitches = []
    if currentStage != 0:
        activeSwitches = [int(item) for item in stages[currentStage-1]["SwitchIDS"].split(',')]
    if currentStage == 0:
        #mF.shutDownSwitches()
        print("Turning off all switches")
    else:
        for i,switch in enumerate(switches):
            if i+1 in activeSwitches:
                #switch.turn_on()
                print("Turning on switch: " + str(i+1))
            else:
                #switch.turn_off()
                print("Turning off switch: " + str(i+1))
   
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
            
        

    
    
    
    
    
    
    
