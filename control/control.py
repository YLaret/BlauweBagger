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
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)
vfd.connect()

try:
    # CONTACT VFD
    result = vfd.write_register(0x0001,0b01)
except:
    print("No connection with VFD")

while True:
    try:
        # CONTACT VFD
        result = vfd.write_register(0x0001,0b01)
        
        # CONNECTED TO VFD
        print("VFD connected")

        # READ PHASE
        controls = cF.getTable("CONTROL",0)
        meters = cF.getTable("METER",0)

        for control in controls:
            # CONTROL PHASE
            meas = meters[control["MeterID"]-1]["Value"]
            e = control["Ref"] - meas
            controlDict[control["ControlID"]]["t1"] = datetime.datetime.now()
            dt = (controlDict[control["ControlID"]]["t1"]-controlDict[control["ControlID"]]["t0"]).total_seconds()
            controlDict[control["ControlID"]]["t0"] = datetime.datetime.now()
            eSum = e*dt + controlDict[control["ControlID"]]["eSum"]
            de = (e-controlDict[control["ControlID"]]["e"])/dt

            freq = min(max(control["Freq"] + control["Kp"]*e + control["Ki"]*eSum + control["Kd"]*de,0),50)
            value = int(freq * 10)
            result = vfd.write_register(FREQ_REGISTER, value, no_response_expected=True)

            # WRITE PHASE
            cF.writeFrequency(control["ControlID"],freq)
            controlDict[control["ControlID"]]["e"] = e
            controlDict[control["ControlID"]]["eSum"] = eSum

            # LOG PHASE
            LOG_FILE = "control" + str(control["ControlID"])+ "_log.csv"

            if not os.path.exists("../data/control/"+LOG_FILE):
                with open("../data/contol/"+LOG_FILE, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.datetime.now().isoformat(),
                        meas,
                        control["Ref"],
                        freq
                    ])
            else:
                with open("../data/control/"+LOG_FILE, "a", newline="", buffering=1) as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.datetime.now().isoformat(),
                        meas,
                        control["Ref"],
                        freq
                    ])
                    f.flush()
            
		# SLEEP PHASE
        sleep(sleepTime)

    except:
        # NO CONNECTION
        print("No VFD connection")
        
        # READ PHASE
        controls = cF.getTable("CONTROL",0)
        meters = cF.getTable("METER",0)
        
        for control in controls:
            # RESET PHASE
            meas = meters[control["MeterID"]-1]["Value"]
            controlDict[control["ControlID"]]["e"] = 0
            controlDict[control["ControlID"]]["eSum"] = 0
            controlDict[control["ControlID"]]["t1"] = datetime.datetime.now()
            dt = (controlDict[control["ControlID"]]["t1"]-controlDict[control["ControlID"]]["t0"]).total_seconds()
            controlDict[control["ControlID"]]["t0"] = datetime.datetime.now()
            
            # LOG PHASE
            LOG_FILE = "control" + str(control["ControlID"])+ "_log.csv"

            if not os.path.exists("../data/control/"+LOG_FILE):
                with open("../data/control/"+LOG_FILE, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.datetime.now().isoformat(),
                        meas,
                        control["Ref"],
                        0
                    ])
            else:
                with open("../data/control/"+LOG_FILE, "a", newline="", buffering=1) as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.datetime.now().isoformat(),
                        meas,
                        control["Ref"],
                        0
                    ])
                    f.flush()
                    
        # SLEEP PHASE
        #sleep(sleepTime)
            
        
