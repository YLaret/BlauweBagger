# websever
from flask import Flask, render_template, redirect, jsonify, send_from_directory
import sqlite3
import os

# local functions
import serverFunctions as sF

app = Flask(__name__)

# define table names, this will need something different in the future
tableNames = ["DEVICE","SWITCH","METER","STAGE","PROGRAM","MACHINESTATUS","FORCE"]

# log directory
logDir = "../data/log"

@app.route("/")
def overview():
    machineStatus = sF.getTable("MACHINESTATUS",0)
    programs = sF.getTable("PROGRAM",0)
    switches = sF.getTable("SWITCH",0)
    stages = sF.getTable("STAGE",0)
    meters = sF.getTable("METER",0)
    
    # round the meter reading
    for i,meter in enumerate(meters):
        meters[i]["Value"] = round(float(meters[i]["Value"]))
    # current machine status
    CMS = sF.getMachineStatus(machineStatus,programs,stages)
    
    return render_template('overview.html',CMS=CMS,programs=programs,meters=meters,switches=switches)

@app.route("/updatepage")
def updatePage():
    machineStatus = sF.getTable("MACHINESTATUS",0)
    programs = sF.getTable("PROGRAM",0)
    stages = sF.getTable("STAGE",0)
    meterData= sF.getTable("METER",0)
    meters = []
    
    # process meter reading
    for meter in meterData:
        meters.append(round(float(meter["Value"]),1))

    # current machine status
    CMS = sF.getMachineStatus(machineStatus,programs,stages)

    CMS['meters'] = meters

    return jsonify(CMS)

@app.route("/toggleswitch/<switch>")
def toggleSwitch(switch):
    sF.toggleSwitch(switch)
    sF.forceAllSwitches()
    return redirect("/")

@app.route("/selectprogram/", methods=["POST"])
def selectProgram():
    sF.selectProgram()
    return redirect("/")

@app.route("/previous")
def previous():
    machineStatus = sF.getTable("MACHINESTATUS",0)
    programs = sF.getTable("PROGRAM",0)
    stages = sF.getTable("STAGE",0)
    CMS = sF.getMachineStatus(machineStatus,programs,stages)
    sF.setProgramRunTime(CMS['prevStageTime']-0.1)
    return redirect("/")

@app.route("/start")
def start():
    sF.start()
    sF.forceAllSwitches()
    return redirect("/")

@app.route("/pause")
def pause():
    sF.pause()
    sF.forceAllSwitches()
    return redirect("/")
    
@app.route("/stop")
def stop():
    sF.stop()
    sF.forceAllSwitches()
    return redirect("/")
    
@app.route("/next")
def next():
    machineStatus = sF.getTable("MACHINESTATUS",0)
    programs = sF.getTable("PROGRAM",0)
    stages = sF.getTable("STAGE",0)
    CMS = sF.getMachineStatus(machineStatus,programs,stages)
    sF.setProgramRunTime(CMS['nextStageTime']+0.1)
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

@app.route("/log")
def log():
    logs = [f for f in os.listdir(logDir) if os.path.isfile(os.path.join(logDir, f)) and not f.startswith('._')]
    return render_template('log.html',logs=logs)

@app.route('/log/download/<logfile>')
def downloadLog(logfile):
    return send_from_directory(logDir, logfile, as_attachment=True)
