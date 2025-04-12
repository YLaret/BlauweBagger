import sqlite3
import getTable

def forceAllSwitches():
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)
    
    # get all switches
    switchData = sF.getTable("SWITCH",0)
    swq = ''
    for sw in switchData:
        swq = swq + str(sw["SwitchID"]) + ','
    swq = swq[:-1]
    
    # force all switches
    db.execute('UPDATE FORCE SET SwitchIDS = "'+swq+'"')
    db.commit()
    db.close()
    return
