## Python has to be run from a venv to prevent breaking system python

## Setup already done in previous step: 5-Python

Install node-red-contrib-pythonshell palette and fill in the node and attach a debug node
Run the node and the python script will be executed

######Modbus usb drive######
When you are not able to acces a device outside the container, for example "/dev/ttyUSB0" you can add a <user> to the docker compose file or add a group to the compose file
For more information see "Permission_Errors.txt"


###############Python Node-red###############
https://www.rodened.com/posts/how-to-use-python-in-node-red-1/#:~:text=The%20first%20step%20is%20to,it%20to%20other%20service%20APIs
But it's easier to setup a venv using the code / tutorial from the "README_python.txt" in the "5-Python" folder
Also installing packages is easier via bash
