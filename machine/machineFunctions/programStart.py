# database package
import sqlite3

def programStart():
    # connect database
    db = sqlite3.connect("../data/machine.db")

    # get the start value from the database
    load = db.execute("SELECT id FROM programStatus").fetchall()
    start = load[0][0]

    # see if the start switch (int) is on (1)
    if start == 1:
        return True
    else:
        return False
