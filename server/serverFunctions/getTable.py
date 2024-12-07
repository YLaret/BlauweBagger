# database package
import sqlite3

def getTable(table):
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)

    # get the names of the columns and close the connection
    cs = db.execute('SELECT * FROM ' + table)
    ns = [description[0] for description in cs.description]
    db.close()

    # turn the table into a dict list
    result = []
    for ci in cs:
        result.append(dict(zip(ns,ci)))

    return result
