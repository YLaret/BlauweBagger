Installation of pi cpu temp monitor
https://github.com/hjelev/rpi-mqtt-monitor


!!!!!!!!!!!Does not work with paho 2!!!!!!!!!!!
works with 1.6
pip install paho-mqtt==1.6.1

Has to be installed using a venv because otherwise OS python may break
See folder "5-Python" => "README_python.txt" how to set-up a venv

#open python venv
$cd /docker-volumes/python
$source python_docker/bin/activate

#check if you are in correct python
$which python

$git clone https://github.com/hjelev/rpi-mqtt-monitor.git

#close python venv
$deactivate

Rename src/config.py.example to src/config.py

Er zijn 2 source bestanden:het python script rpi-cpu2mqtt.py en het config bestand config.py. 
In het config.py bestand moet de 'mqtt_host' en de 'mqtt_topic_prefix' worden ingevuld, dit is in de huidige situatie het IP adres van de Pi zelf.
Het python3 script rpi-cpu2mqtt.py verstuurd de cpu temperatuur naar de MQTT server.
Kopieer de bestanden naar een locatie bv (/docker-volumes/python/rpi-mqtt-monitor/src) of ander gewenst pad
Dit path moet in de schedule regel van de crontab worden ingevoerd.


To schedule the "rpi-cpu2mqtt.py" script every minute with Crontab.
see: https://www.raspberrypi.org/documentation/linux/usage/cron.md
see: https://crontab.guru/every-1-minutes

Hiervoor moet je onderstaande regel toevoegen aan de crontab (Cron Table)
Voer hiervoor onderstaand commando uit:

crontab -e 	//je krijgt dan een lijstje te zien met een aantal editers. Kies default 1. Bin/nano
voeg onderstaande regel toe:
*/1 * * * *  /docker-volumes/python/python_docker/bin/python /docker-volumes/python/rpi-mqtt-monitor/src/rpi-cpu2mqtt.py
Deze regel opent eerst de venv en voert dan het script uit

afsluiten met cntr x en Enter

Je kunt controleren welke scheduled task er aktief zijn met onderstaand commando:
crontab -l


Na invoering van de schedule task wordt deze gelijk actief dit kun je controleren met bv. MQTT.fx door te 
MQTT.fx kun je downloaden via onderstaande link, en installeren op je PC.
https://mqttfx.jensd.de/

Connect met MQTT.fx naar je MQTT server op de Pi en subscribe op # , dit is een wildcard waarmee je alle binnenkomende berichten op je MQTT server ziet.
Handmatig opvragen van de CPU temperatuur:  $vcgencmd measure_temp

Zie ook 
https://github.com/hjelev/rpi-mqtt-monitor/blob/master/src/rpi-cpu2mqtt.py#L63
https://git.cjparish.uk/cparish/rpi-mqtt-monitor/-/blob/master/src/rpi-cpu2mqtt.py








cd /docker-volumes/python/ && source python_docker/bin/activate && python3 /rpi-mqtt-monitor/src/rpi-cpu2mqtt.py

/docker-volumes/python/python_docker/bin/python /docker-volumes/python/rpi-mqtt-monitor/src/rpi-cpu2mqtt.py



