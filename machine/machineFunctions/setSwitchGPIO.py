import gpiod
from gpiod.line import Direction, Value

def setSwitchGPIO(gpio,value):
    # switch gpio
    LINE = gpio
        
    with gpiod.request_lines(
        "/dev/gpiochip4",
        consumer="set-switch",
        config={
            LINE: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=Value.ACTIVE
            ),
        },
    ) as request:
        if value:
            request.set_value(LINE, Value.ACTIVE)
        else:
            request.set_value(LINE, Value.INACTIVE)
    return
