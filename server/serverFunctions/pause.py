import sqlite3

def pause():
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)
    db.execute('UPDATE MACHINESTATUS SET Pause = 1')
    db.commit()
    # close connection
    db.close()

