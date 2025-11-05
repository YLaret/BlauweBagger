import gpiod
from gpiod.line import Direction, Value

def shutDownSwitchesGPIO(switchData):
    # turn of each switch
    for i, switch in enumerate(switchData):
        # turn down switches
        LINE = switch["GPIO"]
        
        with gpiod.request_lines(
            "/dev/gpiochip0",
            consumer="turnoff-switch",
            config={
                LINE: gpiod.LineSettings(
                    direction=Direction.OUTPUT, output_value=Value.INACTIVE
                ),
            },
        ) as request:
            request.set_value(LINE, Value.INACTIVE)
    return
