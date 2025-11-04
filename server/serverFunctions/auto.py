import sqlite3

def auto():
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)
    db.execute('UPDATE MACHINESTATUS SET Pause = 14')
    db.execute('UPDATE STAGE SET SwitchIDS = "0" WHERE StageID = 2')
    db.commit()
    # close connection
    db.close()

