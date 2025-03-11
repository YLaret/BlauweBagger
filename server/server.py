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
    return render_template('overview.html',tables=machineStatus,tableNames="MACHINESTATUS",programs=programs)
    
@app.route("/toggleswitch/<switch>")

@app.route("/selectprogram/")

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
