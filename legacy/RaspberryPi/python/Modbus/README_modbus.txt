Modbus data can be extracted using python and the minimalmodbus package

###Current working setup###
python 3.11.2
minimalmodbus 2.1.1
pyserial 3.5

###To connect to a modbus device the following parameters need to be known:###

Connection: serial port / RTU
modbus address: 1
Baud rate: 9600 
Data bits: 8
Parity: None
Stop bit: 1

Above values are default for most devices and can be changed. modbus address should be changed in most instances.
Because when multiple modbus slaves are connected they can't have the same address

###Register addresses###
Data from sensors will be written to register addresses with a Function code (FC)
For sensors this usually is FC3
https://control.com/technical-articles/introduction-to-modbus-and-modbus-function-codes/ 

with ####modbus poll### it is possible to poll all registers to find out where the data is you want to read or write

###minimal modbus###
this python package is used to read modbus data
https://www.youtube.com/watch?v=FUfxETGIyUo&t=309s 
https://minimalmodbus.readthedocs.io/en/stable/usage.html 


###Polling multiple devices###
When polling mutliple devices make sure to insert a delay/timeout between polls to prevent crashing/errors
Ports need to be closed before they can be opened again. And a port cannot be opened at the same time by multiple scripts/"pollers"/programs/clients