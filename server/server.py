# websever
from flask import Flask, render_template

# local functions
import serverFunctions as sF

app = Flask(__name__)

@app.route("/")
def overview():
    return render_template('overview.html')

@app.route("/tableview")
def tableview():
    motors = sF.getTable("motors")
    return render_template('tableview.html',motors=motors)

@app.route("/program")
def program():
    return render_template('program.html')
