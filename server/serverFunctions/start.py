import sqlite3

def start():
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)
    db.execute('UPDATE MACHINESTATUS SET Pause = 0')
    db.commit()
    # close connection
    db.close()
