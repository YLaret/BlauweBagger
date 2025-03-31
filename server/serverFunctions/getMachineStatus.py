def getMachineStatus(machineStatus,programs,stages):
    programID = int(machineStatus[0]["ProgramID"])
    pause = int(machineStatus[0]["Pause"])
    programRunTime = machineStatus[0]["ProgramRunTime"]
    ### FIND CURRENT STAGE
    # currentStage variable (0 if no stage => full stop)
    currentStage = 0
    nextStageName = '-'
    totalProgramTime = 0
    totalStageTime = 0
    prevStageTime = 0
    
    # if program paused allow manual control
    if pause == 1:
        # special manual stage
        currentStage = 1
    # else if program running normally
    elif pause == 0:
        # calculate currentStage based on run time
        pstages = [int(item) for item in programs[programID-1]["StageIDS"].split(',')]
        stageTime = 0
        found = 0
        for i,stage in enumerate(pstages):
            stageTime = stageTime + stages[pstages[i]-1]["Time"]
            if stageTime > programRunTime and found == 0:
                currentStage = pstages[i]
                if i < len(pstages):
                    nextStageName = stages[pstages[i+1]]["Name"]
                found = 1
                prevStageTime = stageTime - stages[pstages[i]-1]["Time"]
                totalStageTime = stages[pstages[i]-1]["Time"]
            # continue to find the total program time
            totalProgramTime = stageTime
    
    # calculate current stage run time
    stageRunTime = programRunTime - prevStageTime

    ## FIND ACTIVE SWITCHES FOR STAGE
    activeSwitches = []
    if currentStage != 0:
        activeSwitches = [int(item) for item in stages[currentStage-1]["SwitchIDS"].split(',')]
    
    ## OUTPUT DATA
    result = {'pause':pause,'totalProgramTime':totalProgramTime,'totalStageTime':totalStageTime,'programRunTime':programRunTime, 'stageRunTime':stageRunTime, 'programName':programs[programID-1]["Name"],'stageName':stages[currentStage-1]["Name"],'nextStageName':nextStageName,'activeSwitches':activeSwitches}
    return result
    
