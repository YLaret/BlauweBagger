def shutDownSwitches(switches):
    # turn of each switch
    for i,switch in enumerate(switches):
        if i>1:
            switch.turn_off()
    return
