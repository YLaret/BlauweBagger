# package to handle form submit
from flask import request
# database package
import sqlite3

def selectProgram():
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)

    value = request.form.get('program')

    # update database
    db.execute('UPDATE MACHINESTATUS SET ProgramID =' + str(value))
    db.execute('UPDATE MACHINESTATUS SET Pause = 2')
    
    # commit changes and close connection
    db.commit()
    db.close()
    return
