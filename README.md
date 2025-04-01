# BlauweBagger
This is the repository for the software that controls the Blauwe Bagger prototype installation.

## TODO
* Logging monitor and output        !!
* Pump control based on flowmeter   !!
* Direct toggle for switches        !

## Architecture
The controller is a Raspberry Pi module which controls the pumps and motors with Tuya enabled switches. The Pi will control the machine with a python service `machine.py`. This service will read the preferred state and write the actual state of the machine from and to a SQL database. A second service `server.py` hosts a local website that reads and writes the database values, allowing the user to control the machine remotely.
* `machine.py` will rely heavily on the [TinyTuya](https://github.com/jasonacox/tinytuya) library for interaction with switches
* `server.py` will be based around Flask and nginx

### Database Architecture
The database follows a relational model with the following layout:
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
* Turn on SSH and add user `pi` with password [...]
* SSH into the Pi:
`ssh pi@[ipaddress]`
* Install pip, git and nginx:
```
sudo apt update
sudo apt upgrade
sudo apt install pip
sudo apt install git
sudo apt install nginx
```


Make sure python and pip are installed
* Clone the repository 
`git clone https://github.com/YLaret/BlauweBagger`
* Go to the BlauweBagger directory 
`cd BlauweBagger`
* Install the python dependencies 
`sudo pip install -r requirements.txt --break-system-packages`

## Running the webserver (for quick dev)
To run the webserver in developer modus:
```
cd server
export FLASK_APP=server
flask run --host=0.0.0.0
```
* After making some changes to the `server.py`, the server can be stopped by Ctr+C and restarted by the previous command

## Installing the webserver (permanent usage)
* Create a service for the server:
`sudo nano /etc/systemd/system/BlauweBagger.service`
* Copy paste the following:

```
[Unit]
Description=uWSGI instance to serve BlauweBagger server
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/BlauweBagger/server
ExecStart=/usr/local/bin/uwsgi --ini server.ini

[Install]
WantedBy=multi-user.target
```
* Enable the service:
```
sudo systemctl start BlauweBagger
sudo systemctl enable BlauweBagger
```

* Create start up script to fix permissions:
`sudo nano /etc/systemd/system/FixSocketPermissions.service`
* Copy and past the following:
```
[Unit]
Description=Fix socket permissions
After=network.target BlauweBagger.service

[Service]
ExecStart=/bin/bash -c "sudo chown pi:www-data /home/pi/BlauweBagger/server/server.sock; sudo chmod 660 /home/pi/BlauweBagger/server/server.sock"
Type=oneshot
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```
* Activate script:
```
sudo systemctl daemon-reload
sudo systemctl enable FixSocketPermissions
sudo systemctl start FixSocketPermissions
```

* Configure Nginx to proxy Request:
* `sudo nano /etc/nginx/sites-available/BlauweBagger`
* Copy paste the following:

```
server {
    listen 80;
    server_name 192.168.0.200;
location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/pi/BlauweBagger/server/server.sock;
    }
}
```
* Link to enabled sites:
* `sudo ln -s /etc/nginx/sites-available/BlauweBagger /etc/nginx/sites-enabled`
* Restart Nginx:
* `sudo systemctl restart nginx`

## Running the machine program (for quick dev)
To run the machine program in developer modus:
```
cd machine
python machine.py
```

Exit the program with Ctr+C

## Installing the machine program (permanent usage)
* Create the service `sudo nano /etc/systemd/system/BlauweBaggerMachine.service`
* Copy and past the following:
```
[Unit]
Description=Python script controlling the machine
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/BlauweBagger/machine
ExecStart=/usr/bin/python /home/pi/BlauweBagger/machine/machine.py
Restart=on-abort


[Install]
WantedBy=multi-user.target
```
* Start the script
```
sudo systemctl daemon-reload
sudo systemctl start BlauweBaggerMachine
sudo systemctl enable BlauweBaggerMachine
```
