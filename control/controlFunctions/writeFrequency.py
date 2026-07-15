# database package
import sqlite3

def writeFrequency(controlID,frequency):
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)
    db.execute('UPDATE CONTROL SET Pause = ' + str(frequency) + ' WHERE ControlID = ' + str(controlID))
    # commit changes and close connection
    db.commit()
    db.close()
    return
