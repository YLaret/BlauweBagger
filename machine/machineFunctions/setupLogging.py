import logging
import os

def setupLogging():
    logDir = "../data/log"
    if not os.path.exists(logDir):
        os.makedirs(logDir)
    
    logFilename = f"{logDir}/machine_log_{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
    
    logging.basicConfig(
        filename=logFilename,
        level=logging.INFO,
        format='%(asctime)s -%(levelname)s - %(message)s'
    )
