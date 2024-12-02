# BlauweBagger
This is the repository for the software that controls the Blauwe Bagger prototype installation.

## Architecture
The controller is a Raspberry Pi module which controls the pumps and motors with Tuya enabled switches. The Pi will control the machine with a python service `machine.py`. This service will read the preferred state and write the actual state of the machine from and to a SQL database. A second service `server.py` hosts a local website reads and writes the database values, allowing the user to control the machine remotely.
* `machine.py` will rely heavily on the tinytuya library for interaction with switches
* `server.py` will be based around Flask and nginx

## Design Requirements
* Controlling pumps (timed and manual) using WebUI
* Flowmeter visualization in WebUI
* Pump control based on flowmeter
* Log pump data (flow and power)
* Log and display errors and stalls
* Be transferable to new systems

## Installation
* Make sure python and pip are installed
* Clone the repository `git clone https://github.com/YLaret/BlauweBagger`
* Go to the BlauweBagger directory `cd BlauweBagger`
* Install the python dependencies `pip install -r requirements.txt`

## Running the webserver
To run the webserver in developer modus:
* `cd server`
* `export FLASK_APP=server`
* `python3 -m flask run --host=0.0.0.0`
* After making some changes to the `server.py`, the server can be stopped by Ctr-C and restarted by the previous command
