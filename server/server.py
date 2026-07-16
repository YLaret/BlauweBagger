# websever
from flask import Flask, render_template, redirect, jsonify, send_from_directory, request
import sqlite3
import os
import csv

# local functions
import serverFunctions as sF

app = Flask(__name__)

# define table names, this will need something different in the future
tableNames = ["STAGE","PROGRAM","METERRULES","MACHINESTATUS","SWITCH","METER","DEVICE","FORCE","CONTROL"]

# log directory
logDir = "../data/log"

@app.route("/control")
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
    
@app.route("/acc")
def acc():
    tables = []
    for tableName in tableNames:
        if tableName == "CONTROL":
            tables.append(sF.getTable(tableName,0))
            print(Kd)
    controls = sF.getTable("CONTROL",0)
    for control in controls:
        LOG_FILE = "control" + str(control["ControlID"])+ "_log.csv"
        with open("../data/control/"+LOG_FILE) as f:
            reader = csv.reader(f)
            control["time"] = []
            control["meas"] = []
            control["ref"] = []
            control["freq"] = []
            for row in reader:
                control["time"].append(row[0])
                control["meas"].append(float(row[1]))
                control["ref"].append(float(row[2]))
                control["freq"].append(float(row[3]))
    
    return render_template('acc.html',controls=controls,tables=tables,tableNames=["CONTROL"])

@app.route("/acc/<controlID>")
def accClear(controlID):
    acclog = "../data/control/control"+str(controlID)+"_log.csv"
    if os.path.exists(acclog):
        os.remove(acclog)
    return redirect("/acc")

@app.route("/")
def hmi():
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
    
    # aggrate meter values
    aM = sF.aggrateMeters(meters)
    
    return render_template('hmi.html',CMS=CMS,programs=programs,meters=meters,switches=switches,aM=aM)

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
    
    # aggrate meter values
    aM = sF.aggrateMeters(meterData)

    # current machine status
    CMS = sF.getMachineStatus(machineStatus,programs,stages)

    CMS['meters'] = meters
    CMS['aM'] = aM
    
    # control
    controls = sF.getTable("CONTROL",0)
    for control in controls:
        LOG_FILE = "control" + str(control["ControlID"])+ "_log.csv"
        with open("../data/control/"+LOG_FILE) as f:
            reader = csv.reader(f)
            control["time"] = []
            control["meas"] = []
            control["ref"] = []
            control["freq"] = []
            for row in reader:
                control["time"].append(row[0])
                control["meas"].append(float(row[1]))
                control["ref"].append(float(row[2]))
                control["freq"].append(float(row[3]))
    CMS['controls'] = controls
    return jsonify(CMS)

@app.route("/toggleswitch/<switch>")
def toggleSwitch(switch):
    sF.toggleSwitch(switch)
    sF.forceAllSwitches()
    return redirect(request.referrer or "/")

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

@app.route("/auto")
def auto():
    sF.auto()
    sF.forceAllSwitches()
    return redirect(request.referrer or "/")

@app.route("/start")
def start():
    sF.start()
    sF.forceAllSwitches()
    return redirect("/")

@app.route("/pause")
def pause():
    sF.pause()
    sF.forceAllSwitches()
    return redirect(request.referrer or "/")
    
@app.route("/stop")
def stop():
    sF.stop()
    sF.forceAllSwitches()
    return redirect(request.referrer or "/")
    
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
def programMotors(table):
    sF.updateTable(table)
    return redirect("/program")
    
@app.route("/acc/<table>", methods=["POST"])
def programControl(table):
    sF.updateTable(table)
    return redirect("/acc")

@app.route("/log")
def log():
    logs = [f for f in os.listdir(logDir) if os.path.isfile(os.path.join(logDir, f)) and not f.startswith('._')]
    return render_template('log.html',logs=logs)

@app.route('/log/download/<logfile>')
def downloadLog(logfile):
    return send_from_directory(logDir, logfile, as_attachment=True)
