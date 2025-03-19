import time
def shutDownSwitches(switches):
    # turn of each switch
    for i,switch in enumerate(switches):
        TiD = 1
        if switch["TuyaVersion"] == 3.3:
            TiD = 1
        elif switch["TuyaVersion"] == 3.4:
            TiD = 17
        switch.set_value(TiD,False,nowait=True)
    return
