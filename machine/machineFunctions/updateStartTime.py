# date time functions
import datetime

# database package
import sqlite3

def updateStartTime(startTime):
    # connect to database
    db = sqlite3.connect("../data/machine.db")

    # get the current program status
    ps = db.execute("SELECT * FROM programStatus").fetchall()
    ps = ps[0]

    if ps[0] == 1 and ps[1] == 0:
        # refresh starttime if not already running
        startTime = datetime.datetime.now()
        db.execute('UPDATE programStatus SET running=1 WHERE id=1')
    # update the runtime
    runtime = (datetime.datetime.now() - startTime).total_seconds()
    db.execute('UPDATE programStatus SET runtime='+str(runtime)+' WHERE id=1')
    db.commit()

    return startTime
