def shutDownSwitches(switches):
    # turn of each switch
    for i,switch in enumerate(switches):
        switch.turn_off(nowait=True)
    return
