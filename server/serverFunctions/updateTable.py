# package to handle form submit
from flask import request
# database package
import sqlite3

def updateTable(table):
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
    
    # allow for addition of 1 row if not none
    values = ""
    columns = ""
    for i,ni in enumerate(ns):
        if i>0:
            # value
            value = request.form.get(str(rows+2) + str(ni))
            if value != "None":
                try:
                    float(value)
                except ValueError:
                    value = '"'+str(value)+'"'
                values = values + str(value) + ','
                columns = columns + ni + ','
    
    values = values[:-1]
    columns = columns[:-1]
    
    query = 'INSERT INTO ' + str(table) + ' ('+columns+') VALUES (' + values + ')'

    if values and columns:
        db.execute(query)

    # commit changes and close connection
    db.commit()
    db.close()
    return
