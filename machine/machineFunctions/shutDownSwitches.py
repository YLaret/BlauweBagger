def shutDownSwitches(switches):
    # turn of each switch
    for i,switch in enumerate(switches):
        sleep(0.1)
        switch.turn_off(nowait=True)
    return
