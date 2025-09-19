import gpiod
from gpiod.line import Direction, Value, Bias

def getValueGPIO(gpio):
    SENSOR = gpio
    with gpiod.request_lines(
        "/dev/gpiochip0",
        consumer="getvalue-gpio",
        config={
            SENSOR: gpiod.LineSettings(
                direction=Direction.INPUT,
            ),
        },
    ) as request:
        # Read sensor
        sensor_value = request.get_value(SENSOR)
        if sensor_value:
            return 1
        else:
            return 0
