import time
def shutDownSwitches(switches):
    # turn of each switch
    for i,switch in enumerate(switches):
        time.sleep(0.1)
        switch.turn_off(nowait=True)
    return
