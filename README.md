# BlauweBagger
This is the repository for the software that controls the Blauwe Bagger prototype installation.
## Architecture
The controller is a Raspberry Pi module which controls the pumps and motors with Tuya enabled switches. The Pi will control the machine with a python service `machine.py`. This service will read the preferred state and write the actual state of the machine from and to a SQL database. A second service `server.py` hosts a local website reads and writes the database values, allowing the user to control the machine remotely.
* `machine.py` will rely heavily on the tinytuya library for interaction with switches
* `server.py` will be base around Flask and nginx
