import controlFunctions as cF
from pymodbus.client import ModbusSerialClient
import datetime
import csv
import os
from time import sleep

# constants
sleepTime = 1 # [s]
FREQ_REGISTER = 0x2001

# initialize
controls = cF.getTable("CONTROL",0)
controlDict = {}
for control in controls:
	controlDict[control["ControlID"]] = {"e":0,"eSum":0,"t0":datetime.datetime.now(),"t1":datetime.datetime.now()}

# CONNECT VFD
vfd = ModbusSerialClient(
    port='/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0',
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)
vfd.connect()

while True:
    # READ PHASE
    controls = cF.getTable("CONTROL",0)
    meters = cF.getTable("METER",0)
    for control in controls:
        meas = meters[control["MeterID"]-1]["Value"]
        if control["cyclOn"] == 1:
            # CONTROL PHASE
            e = control["Ref"] - meas
            controlDict[control["ControlID"]]["t1"] = datetime.datetime.now()
            dt = (controlDict[control["ControlID"]]["t1"]-controlDict[control["ControlID"]]["t0"]).total_seconds()
            controlDict[control["ControlID"]]["t0"] = datetime.datetime.now()
            eSum = e*dt + controlDict[control["ControlID"]]["eSum"]
            de = (e-controlDict[control["ControlID"]]["e"])/dt

            if control["auto"] == 1:
                freq = min(max(control["Freq"] + control["Kp"]*e + control["Ki"]*eSum + control["Kd"]*de,0),50)
            else:
                freq = control["Freq"]
            
            value = int(freq * 10)
            result = vfd.write_register(FREQ_REGISTER, value, no_response_expected=True)

            # WRITE PHASE
            cF.writeFrequency(control["ControlID"],freq)
            controlDict[control["ControlID"]]["e"] = e
            controlDict[control["ControlID"]]["eSum"] = eSum
        else:
            freq = 0
            
        # LOG PHASE
        LOG_FILE = "control" + str(control["ControlID"]) + "_log.csv"
        LOG_PATH = "../data/control/" + LOG_FILE

        row = [
            datetime.datetime.now().isoformat(),
            meas,
            control["Ref"],
            freq
        ]

        if not os.path.exists(LOG_PATH):
            with open(LOG_PATH, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(row)
        else:
            with open(LOG_PATH, "a", newline="", buffering=1) as f:
                writer = csv.writer(f)
                writer.writerow(row)
                f.flush()

            # Keep only the last 120 rows
            with open(LOG_PATH, "r", newline="") as f:
                rows = list(csv.reader(f))

            header = rows[0]
            data = rows[1:]

            if len(data) > 120:
                with open(LOG_PATH, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(data[-119:])
    # SLEEP PHASE
    sleep(sleepTime)
