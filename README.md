# BlauweBagger
This is the repository for the software that controls the Blauwe Bagger prototype installation.

## User Guide
After booting up the Raspberry Pi and going to the main page: [Main](http://192.168.0.100). The schematic overview should be visible (meters are being updated live, so can have different values):
![Schematic Stop](https://raw.githubusercontent.com/YLaret/BlauweBagger/main/docs/schematic_stop.png)
The system always boots with all switches off (STOP mode).
### Automatic Control
To let the machine run on autopilot simply press `AUTO`. The machine will determine based on the sensors which pumps and motors to turn on/off.
![Schematic Auto](https://raw.githubusercontent.com/YLaret/BlauweBagger/main/docs/schematic_auto.png)
### Manual Control
To control the switches manually, press `PAUSE` all the switches will turn off. Pressing on a pump or motor will turn it on/off. **Be careful: NO METER CONTROL, dangerous situation can occur.** 
![Schematic Manual](https://raw.githubusercontent.com/YLaret/BlauweBagger/main/docs/schematic_pause.png)
### Timer Control (deprecated)
To run a timer based program, create stages with SwitchIDS and stageTimes and add these to a program. In the control view the program can be selected and executed. **NOTE:** the first program `Clay Unload` is a special program used by automatic control for the unload sequence, change with caution.
![Program Timer](https://raw.githubusercontent.com/YLaret/BlauweBagger/main/docs/program_timer.png)

## Architecture
The controller is a Raspberry Pi module which controls the pumps and motors with Tuya enabled switches. The Pi will control the machine with a python service `machine.py`. This service will read the preferred state and write the actual state of the machine from and to a SQL database. A second service `server.py` hosts a local website that reads and writes the database values, allowing the user to control the machine remotely.
* `machine.py` will rely on the [gpiod](https://pypi.org/project/gpiod/) library for interaction with switches (GPIO)
* `server.py` will be based around Flask and nginx

### Database Architecture
The database follows a relational model with the following layout:
![Database Architecture](https://raw.githubusercontent.com/YLaret/BlauweBagger/main/docs/databaseArchitecture_v2.jpeg)
**NOTE1:** Upon upgrading the Tuya switches with SSR controlled by the GPIO, the **SWITCH** table does NOT contain: {MeterIDS, MeterMIN, MeterMax, IPAdress, LocalKey} anymore, instead: {SwitchID, Name, GPIO}.
**NOTE2:** A new table linking meters to switches called **METERRULES** containing:{MeterRuleID, MeterID, MeterThreshold, MeterThresholdGEQ, SwitchID, SwitchBool, Stage}.
## General Design Requirements
* ✅ Controlling pumps (manual, timed and automatic (senorbased)) using WebUI
* ✅ Flowmeter visualization in WebUI
* ✅ Pump control based on pressuresensor
* ✅ Log pump data (flow and power)
* ✅ Log and display errors and stalls
* ✅ Be transferable to new systems

### Webserver Design Requirements
* ✅ Schematic and tableview
* ✅ Way to create programs and controll machine manually
* ✅ Tableview with meters table, motors table and log window
* ✅ Schematicview with visualization of the plant (motor and flow meter states) and a log window
* ✅ Program view with timing possibilities

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
ExecStart=/bin/bash -c "sudo chown pi:www-data /home/pi/BlauweBagger/server/server.sock; sudo chmod 660 /home/pi/BlauweBagger/server/server.sock; sudo chmod 755 /home/pi"
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
`sudo nano /etc/nginx/sites-available/BlauweBagger`
* Copy paste the following:

```
server {
    listen 80;
    server_name _;
location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/pi/BlauweBagger/server/server.sock;
    }
}
```
* Link to enabled sites:
`sudo ln -s /etc/nginx/sites-available/BlauweBagger /etc/nginx/sites-enabled`
* Restart Nginx:
`sudo systemctl restart nginx`

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

## Running the control program (for quick dev)
To run the control program in developer modus:
```
cd control
python control.py
```

Exit the program with Ctr+C

## Installing the machine program (permanent usage)
* Create the service `sudo nano /etc/systemd/system/BlauweBaggerControl.service`
* Copy and past the following:
```
[Unit]
Description=Python script controlling the hydrocyclone
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/BlauweBagger/control
ExecStart=/usr/bin/python /home/pi/BlauweBagger/control/control.py
Restart=on-abort


[Install]
WantedBy=multi-user.target
```
* Start the script
```
sudo systemctl daemon-reload
sudo systemctl start BlauweBaggerControl
sudo systemctl enable BlauweBaggerControl
```
## Hydrocyclone Control
The ACC page provides hydrocyclone control. The `Ref` entry of the `CONTROL` table in the `machine.db` Sqlite3 database is used to determine the set point, the `auto` entry is used to toggle sensor control (e.g. when a sensor fails possible to turn of automatic control of the VFD). The control service source code is `control/control.py`.

## Tailscale (remote access)
To access the installation remotely Tailscale is used to create a mesh VPN to which the Raspberry Pi and the control client are connected. To install follow the [instructions](https://pypi.org/project/gpiod/) to install on the Raspberry Pi, login with an account (e.g. `blueboxvpn@gmail.com`) and install on the control client side as well (iOS, macOS, Windows or Linux) and login with the same account. Go to the ip-address of the Raspberry Pi (visible on Tailscale dashboard). On the control client connect to the Tailscale VPN and

## 5G router setup (Zyxel NR5307)
Check the connected devices and note the MAC-address of the raspberrypi (e.g. 1c:cf:67:67:3c:d8). Go to Home Network->Static DHCP insert a configuration with the MAC-address and the preferred IP-address (e.g. 192.168.1.100). This will be url to which local (non-VPN) devices (e.g. iPad) can connect to the machine.
