# Python 3 script to check cpu temperature,
# on a Raspberry Pi computer and publish the data to a MQTT server.
# RUN pip install paho-mqtt
# RUN sudo apt-get install python-pip


import subprocess, time, socket, os
import paho.mqtt.client as paho
import json
import config

# get device host name - used in mqtt topic
hostname = socket.gethostname()



def check_cpu_temp():
		full_cmd = "vcgencmd measure_temp"
		p = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
		cpu_temp = p.decode("utf-8").replace('\n', '').replace('\r', '').split("=")[1].split("'")[0]
		return float(cpu_temp)
		

	
def publish_to_mqtt (cpu_temp = 0):
		# connect to mqtt server
		client = paho.Client()
		client.username_pw_set(config.mqtt_user, config.mqtt_password)
		client.connect(config.mqtt_host, config.mqtt_port)

		# publish monitored values to MQTT
		client.publish(config.mqtt_topic_prefix+"/"+hostname+"/cputemp", cpu_temp, qos=1)
		client.disconnect()


if __name__ == '__main__':

		# collect the monitored values
		cpu_temp = check_cpu_temp()

		# Publish messages to MQTT
		publish_to_mqtt(cpu_temp)

