import sqlite3

def setProgramRunTime(time):
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)
    db.execute('UPDATE MACHINESTATUS SET ProgramRunTime = ' + str(time))
    db.commit()
    # close connection
    db.close()
