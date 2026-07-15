# PSEUDO CODE
import controlFunctions as cF
from pymodbus.client import ModbusSerialClient
import datetime
import csv
import os

# constants
sleepTime = 1 # [s]
FREQ_REGISTER = 0x2001

# initialize
controls = cF.getTable("CONTROL",0)
controlDict = {}
for control in controls:
	controlDict[control["controlID"]] = {"e":0,"eSum":0,"t0":datetime.datetime.now(),"t1":datetime.datetime.now()}

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

while True:
    try:
        # CONTACT VFD
        result = vfd.write_register(0x2000, 0b01)

        # READ PHASE
        controls = cF.getTable("CONTROL",0)
        meters = cF.getTable("METER",0)

        for control in controls:
            # CONTROL PHASE
            e = control["Ref"] - meters[control["meterID"]]
            t1 = datetime.datetime.now()
            dt = (controlDict[control["controlID"]]["t1"]-controlDict[control["controlID"]]["t0"]).total_seconds()
            t0 = datetime.datetime.now()
            eSum = e*dt + controlDict[control["controlID"]]["eSum"]
            de = (e-controlDict[control.controlID]["e"])/dt

            freq = min(max(control["Freq"] + control["Kp"]*e + control["Ki"]*eSum + control["Kd"]*de,0),50)
            value = int(freq * 10)
            result = vfd.write_register(FREQ_REGISTER, value, no_response_expected=True)

            # WRITE PHASE
            cF.writeFrequency(control["controlID"],freq)
            controlDict[control["controlID"]]["e"] = e
            controlDict[control["controlID"]]["eSum"] = eSum

            # LOG PHASE
            LOG_FILE = "control" + str(control["controlID"])+ "_log.csv"

            if not os.path.exists("../data/"+LOG_FILE):
                with open("../data/"+LOG_FILE, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.datetime.now().isoformat(),
                        meters[control["MeterID"]],
                        control["Ref"],
                        freq
                    ])
            else:
                with open("../data/"+LOG_FILE, "a", newline="", buffering=1) as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.datetime.now().isoformat(),
                        meters[control["MeterID"]],
                        control["Ref"],
                        freq
                    ])
                    f.flush()
            
		# SLEEP PHASE
        sleep(sleepTime)
    except:
        for control in controls:
            controlDict[control["controlID"]]["e"] = 0
            controlDict[control["controlID"]]["eSum"] = 0
            t1 = datetime.datetime.now()
            dt = (controlDict[control["controlID"]]["t1"]-controlDict[control["controlID"]]["t0"]).total_seconds()
            t0 = datetime.datetime.now()
            
        
