import sqlite3

def stop():
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)
    db.execute('UPDATE MACHINESTATUS SET Pause = 2')
    db.execute('UPDATE MACHINESTATUS SET ProgramRunTime = 0')
    db.commit()
    # close connection
    db.close()

