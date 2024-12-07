# database package
import sqlite3

# date and time functions
import datetime

def writePrefStateSwitches(switches,startTime):
    # get the current time
    currentTime = datetime.datetime.now()

    # calculate the pass seconds
    secondsPassed = (currentTime - startTime).total_seconds()

    # program switches according to program
    db = sqlite3.connect("../data/machine.db",timeout=5))

    # get the program
    program = db.execute("SELECT * FROM program").fetchall()

    # close the database
    db.close()

    # set the preferred state of each switch
    for i,switch in enumerate(switches):
        # need to get somekind of verification here, but no access to any tuya devices so...
        # if id's match...:

        # if time passed greater then the starting delay and smaller than the starting delay and the needed runtime
        if secondsPassed > program[i][5] and secondsPassed < (program[i][3] + program[i][5]):
            # turn on switch, disabled for test
            #switch.turn_on()
            print("switch "+str(i)+" turning on")
        else:
            # turn off switch, disabled for test
            #switch.turn_off()
            print("switch "+str(i)+" turning off")

    return
