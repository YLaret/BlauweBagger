# package to handle form submit
from flask import request
# database package
import sqlite3

def updateControl():
    # control only
    table = "CONTROL"
    
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)

    # get the possible rows and columns
    cs = db.execute('SELECT * FROM ' + table)
    ns = [description[0] for description in cs.description]

    # count rows
    rows = 0
    
    # update the rows and columns
    for i,ci in enumerate(cs):
        rows = i
        for ni in ns:
            # get form data
            value = request.form.get(str(i+1) + str(ni))
            
            # update database
            db.execute('UPDATE ' + str(table) + ' SET ' + str(ni) + '="' + str(value) + '" WHERE ' + str(ns[0]) + '="' + str(ci[0]) + '"')

    if values and columns:
        db.execute(query)

    # commit changes and close connection
    db.commit()
    db.close()
    return
