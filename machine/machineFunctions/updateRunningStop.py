# database package
import sqlite3

def updateRunningStop():
    # connect to database
    db = sqlite3.connect("../data/machine.db",timeout=5)

    # stop running var
    db.execute("UPDATE programStatus SET running=0 WHERE id=0")

    # commit changes
    db.commit()
    
    return
