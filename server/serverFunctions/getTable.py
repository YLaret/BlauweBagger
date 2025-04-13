# database package
import sqlite3

def getTable(table,add):
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)

    # get the names of the columns
    cs = db.execute('SELECT * FROM ' + table)
    ns = [description[0] for description in cs.description]

    # turn the table into a dict list
    result = []
    rows = 1;
    for ci in cs:
        result.append(dict(zip(ns,ci)))
        rows = rows + 1
    if add:
        if table != "MACHINESTATUS" and table != "FORCE":
            result.append(dict(zip(ns,[rows]+[None]*len(ns))))
    else:
        if not result:
            result.append(dict(zip(ns,[rows]+[None]*len(ns))))
    # close connection
    db.close()
    return result
