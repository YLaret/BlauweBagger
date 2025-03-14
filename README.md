# BlauweBagger
This is the repository for the software that controls the Blauwe Bagger prototype installation.

## Architecture
The controller is a Raspberry Pi module which controls the pumps and motors with Tuya enabled switches. The Pi will control the machine with a python service `machine.py`. This service will read the preferred state and write the actual state of the machine from and to a SQL database. A second service `server.py` hosts a local website reads and writes the database values, allowing the user to control the machine remotely.
* `machine.py` will rely heavily on the [TinyTuya](https://github.com/jasonacox/tinytuya) library for interaction with switches
* `server.py` will be based around Flask and nginx

### Database Architecture
The databse follows a relational model with the following layout:
![Database Architecture](https://raw.githubusercontent.com/YLaret/BlauweBagger/main/docs/databaseArchitecture_v2.jpeg)

## General Design Requirements
* Controlling pumps (timed and manual) using WebUI
* Flowmeter visualization in WebUI
* Pump control based on flowmeter
* Log pump data (flow and power)
* Log and display errors and stalls
* Be transferable to new systems

### Webserver Design Requirements
* Schematic and tableview
* Way to create programs and controll machine manually
* Tableview with meters table, motors table and log window
* Schematicview with visualization of the plant (motor and flow meter states) and a log window
* Program view with timing possibilities

## Installation
### Installing Rasbian
* Download [Raspberry Pi OS Lite (64-bit)](https://www.raspberrypi.com/software/operating-systems/)
* Use Rasbian Imager to etch OS on an SD card
* Turn on SSH, configure wifi (`BlauweBagger_5G`) and add user
* Install pip and git:
* `sudo apt update`
* `sudo apt upgrade`
* `sudo apt install pip`
* `sudo apt install git`


Make sure python and pip are installed
* Clone the repository `git clone https://github.com/YLaret/BlauweBagger`
* Go to the BlauweBagger directory `cd BlauweBagger`
* Install the python dependencies `sudo pip install -r requirements.txt --break-system-packages`

## Running the webserver
To run the webserver in developer modus:
* `cd server`
* `export FLASK_APP=server`
* `flask run --host=0.0.0.0`
* After making some changes to the `server.py`, the server can be stopped by Ctr+C and restarted by the previous command

## Running the machine program
To run the machine program in developer modus:
* `cd machine`
* `python machine.py`

Exit the program with Ctr+C
