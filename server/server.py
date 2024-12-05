# websever
from flask import Flask, render_template, redirect

# local functions
import serverFunctions as sF

app = Flask(__name__)

# define table names, this will need something different in the future
tableNames = ["motors","meters","states","switches","program","programStatus"]

@app.route("/")
def overview():
    return render_template('overview.html')

@app.route("/tableview")
def tableview():
    tables = []
    for tableName in tableNames:
        tables.append(sF.getTable(tableName))
    return render_template('tableview.html',tables=tables,tableNames=tableNames)

@app.route("/program")
def program():
    tables = []
    for tableName in tableNames:
        tables.append(sF.getTable(tableName))
    return render_template('program.html',tables=tables,tableNames=tableNames)

@app.route("/program/<table>", methods=["POST"])
def protramMotors(table):
    sF.updateTable(table)
    return redirect("/tableview")
