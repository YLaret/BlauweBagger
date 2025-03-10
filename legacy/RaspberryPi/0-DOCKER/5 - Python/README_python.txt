## Python has to be run from a venv to prevent breaking system python

## How to install python venv and pip install packages
https://www.tomshardware.com/how-to/install-python-modules-raspberry-pi
https://www.raspberrypi.com/documentation/computers/os.html#python-on-raspberry-pi 

## go to venv folder using cd or where u want to make your venv
cd /docker-volumes/python

##Make python venv
sudo python -m venv python_docker

## go to venv folder using cd
cd python_docker

##start python env
source python_docker/bin/activate

##check if you are in the correct python
which python
## if you are correct path should be: /docker-volumes/python/python_docker/bin/python

##close python venv
deactivate

#############packages#############
##modbus
pip install minimalmodbus
##numpy
pip install numpy



###############Python Node-red###############
https://www.rodened.com/posts/how-to-use-python-in-node-red-1/#:~:text=The%20first%20step%20is%20to,it%20to%20other%20service%20APIs
But it's easier to setup a venv using the code / tutorial above
Also installing packages is easier via bash
