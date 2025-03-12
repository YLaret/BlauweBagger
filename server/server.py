# websever
from flask import Flask, render_template, redirect, jsonify
import sqlite3

# local functions
import serverFunctions as sF

app = Flask(__name__)

# define table names, this will need something different in the future
tableNames = ["DEVICE","SWITCH","METER","STAGE","PROGRAM","MACHINESTATUS"]

@app.route("/")
def overview():
    machineStatus = sF.getTable("MACHINESTATUS",0)
    programs = sF.getTable("PROGRAM",0)
    switches = sF.getTable("SWITCH",0)
    stages = sF.getTable("STAGE",0)
    meters = sF.getTable("METER",0)
    
    ### MESSY PART ###
    programID = int(machineStatus[0]["ProgramID"])
    pause = int(machineStatus[0]["Pause"])
    programRunTime = machineStatus[0]["ProgramRunTime"]
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
    activeSwitches = []
    if currentStage != 0:
        activeSwitches = [int(item) for item in stages[currentStage-1]["SwitchIDS"].split(',')]
    ###################
    return render_template('overview.html',machineStatus=machineStatus,programs=programs,switches=switches,activeSwitches=activeSwitches,meters=meters)

@app.route("/updatepage")
def updatePage():
    machineStatus = sF.getTable("MACHINESTATUS",0)
    programs = sF.getTable("PROGRAM",0)
    switches = sF.getTable("SWITCH",0)
    stages = sF.getTable("STAGE",0)
    meterData= sF.getTable("METER",0)
    meters = []
    for meter in meterData:
        meters.append(float(meter["Value"]))
    programRunTime = machineStatus[0]["ProgramRunTime"]

    ### MESSY PART ###
    programID = int(machineStatus[0]["ProgramID"])
    pause = int(machineStatus[0]["Pause"])
    programRunTime = machineStatus[0]["ProgramRunTime"]
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
    activeSwitches = []
    if currentStage != 0:
        activeSwitches = [int(item) for item in stages[currentStage-1]["SwitchIDS"].split(',')]
    ###################
    return jsonify({'activeSwitches':activeSwitches,'meters':meters,'programRunTime':programRunTime})

@app.route("/toggleswitch/<switch>")
def toggleSwitch(switch):
    sF.toggleSwitch(switch)
    return redirect("/")

@app.route("/selectprogram/", methods=["POST"])
def selectProgram():
    sF.selectProgram()
    return redirect("/")

@app.route("/start")
def start():
    sF.start()
    return redirect("/")

@app.route("/pause")
def pause():
    sF.pause()
    return redirect("/")
    
@app.route("/stop")
def stop():
    sF.stop()
    return redirect("/")
    
@app.route("/tableview")
def tableview():
    tables = []
    for tableName in tableNames:
        tables.append(sF.getTable(tableName,0))
    return render_template('tableview.html',tables=tables,tableNames=tableNames)

@app.route("/program")
def program():
    tables = []
    for tableName in tableNames:
        tables.append(sF.getTable(tableName,1))
    return render_template('program.html',tables=tables,tableNames=tableNames)

@app.route("/program/<table>", methods=["POST"])
def protramMotors(table):
    sF.updateTable(table)
    return redirect("/tableview")
