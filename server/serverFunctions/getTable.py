# database package
import sqlite3

def getTable(table):
    # connect to database
    db = sqlite3.connect('../data/machine.db')

    # get the names of the columns
    cs = db.execute('SELECT * FROM ' + table)
    ns = [description[0] for description in cs.description]

    # turn the table into a dict list
    result = []
    ls = db.execute('SELECT * FROM ' + table)
    for li in ls:
        result.append(dict(zip(ns,li)))

    return result
