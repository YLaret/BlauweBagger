# websever
from flask import Flask, render_template, redirect

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
    
    ### MESSY PART ###
    db = sqlite3.connect('../data/machine.db', timeout=5)
    programData = db.execute('SELECT * FROM PROGRAM').fetchall()
    stageData = db.execute('SELECT * FROM STAGE').fetchall()
    db.close()
    
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
    activeSwitches = []
    if currentStage not 0:
        activeSwitches = [int(item) for item in stageData[currentStage-1][2].split(',')]
    return render_template('overview.html',machineStatus=machineStatus,programs=programs,switches=switches)
    
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
