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
    
    # round the meter reading
    for i in len(meterData):
        meterData[i]["Value"] = round(float(meterData[i]["Value"]))
    # current machine status
    CMS = sF.getMachineStatus(machineStatus,programs,stages)
    
    return render_template('overview.html',CMS=CMS,programs=programs,meters=meters,switches=switches)

@app.route("/updatepage")
def updatePage():
    machineStatus = sF.getTable("MACHINESTATUS",0)
    programs = sF.getTable("PROGRAM",0)
    switches = sF.getTable("SWITCH",0)
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
