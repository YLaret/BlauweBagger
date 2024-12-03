# websever
from flask import Flask, render_template, redirect

# local functions
import serverFunctions as sF

app = Flask(__name__)

@app.route("/")
def overview():
    return render_template('overview.html')

@app.route("/tableview")
def tableview():
    motors = sF.getTable("motors")
    meters = sF.getTable("meters")
    switches = sF.getTable("switches")
    states = sF.getTable("states")
    return render_template('tableview.html',motors=motors,meters=meters,switches=switches,states=states)

@app.route("/program")
def program():
    motors = sF.getTable("motors")
    return render_template('program.html',motors=motors)

@app.route("/program/<table>", methods=["POST"])
def protramMotors(table):
    sF.updateTable(table)
    return redirect("/tableview")
