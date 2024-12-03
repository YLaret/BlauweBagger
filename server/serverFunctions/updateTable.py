# package to handle form submit
from flask import request
# database package
import sqlite3

def updateTable(table):
    # connect to database
    db = sqlite3.connect('../data/machine.db')

    # get the possible rows and columns
    cs = db.execute('SELECT * FROM ' + table)
    ns = [description[0] for description in cs.description]

    # update the rows and columns
    for ci in cs:
        for ni in ns:
            # get form data
            value = request.form.get(ci[0] + ni)
            # update database
            db.execute('UPDATE ' + table + ' SET ' + ni + '="' + value + '" WHERE ' + ns[0] + '="' + ci[0] + '"')
    db.commit()
    return
