import minimalmodbus
def readFlowSensor.py():
    mb_address = 3 # Modbus address of sensor
    sensy_boi = minimalmodbus.Instrument('/dev/ttyUSB0',mb_address)    # Make an "instrument" object called sensy_boi (port name, slave address (in decimal))

    sensy_boi.serial.baudrate = 9600                # BaudRate
    sensy_boi.serial.bytesize = 8                    # Number of data bits to be requested
    sensy_boi.serial.parity = minimalmodbus.serial.PARITY_NONE    # Parity Setting here is NONE but can be ODD or EVEN
    sensy_boi.serial.stopbits = 1                    # Number of stop bits
    sensy_boi.serial.timeout  = 0.1                    # Timeout time in seconds
    sensy_boi.mode = minimalmodbus.MODE_RTU                # Mode to be used (RTU or ascii mode)

    # Good practice to clean up before and after each execution
    sensy_boi.clear_buffers_before_each_transaction = True

    # Needed when running on Windows, slows down the script a lot
    # sensy_boi.close_port_after_each_call = True

    # Get list of values from MULTIPLE registers
    # Every .read call makes the script slower. Often it is faster to read multiple register at once than seperating them
    # For example its faster to read 17 registers in 1 read than 9 seperate reads
    # Arguments - (register start address, number of registers to read, function code)
    data= sensy_boi.read_registers(0, 13, 3)

    f200qa = (data[0]/4095*16*12.1875)
    f250qa = (data[1]/4095*16*14.84375)
    f25ad = (data[2]/4095*16*8.8125)

    data = [f200qa,f250qa,f25ad]

return data

# Piece of mind close out
sensy_boi.serial.close()
