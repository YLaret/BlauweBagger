# database package
import sqlite3

def toggleSwitch(switch):
    # connect to database
    db = sqlite3.connect('../data/machine.db',timeout=5)
    db.execute('UPDATE MACHINESTATUS SET Pause = 1')
    switchData = db.execute('SELECT * FROM STAGE WHERE StageID = 1').fetchall()
    
    switches = [int(item) for item in stageData[0][2].split(',')]
    
    if switch in switches:
        switches.remove(switch)
    else:
        switches.append(switch)
    
    swq = ''
    for sw in switches:
        swq = swq + str(sw) + ','
    
    swq = swq[:-1]
    
    db.execute('UPDATE STAGE SET SwitchIDS = '+swq' WHERE StageID = 1')
    
    # commit changes and close connection
    db.commit()
    db.close()
    return
