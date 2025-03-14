from random import randrange

# Script version
version = "0.6.2"
# MQTT server configuration
mqtt_host = "192.168.0.100"
mqtt_user = "username"
mqtt_password = "password"
mqtt_port = "1883"
mqtt_topic_prefix = "Bagger-Pi-Temp-monitor"

# Messages configuration

# Uncomment the line bellow to send just one CSV message containing all values (this method don't support HA discovery_messages)
# group_messages = True

# If this is set, then the script will send MQTT discovery messages meaning a config less setup in HA.
# Only works when group_messages is not used
discovery_messages = True

# Enable remote restart button in Home Assistant
restart_button = True

# Enable remote shutdown button in Home Assistant
shutdown_button = True

# Binary sensor that displays when there are  updates
git_update = True

# Enable remote update of the script via Home Assistant
update = True

# Retain flag for published topics
retain = True

# QOS setting for published topics: 0,1,2 are acceptable values
qos = 0

# Random delay in seconds before measuring the values
# - this is used for de-synchronizing message if you run this script on many hosts.
# - if you want a fixed delay you can remove the randrange function and just set the needed value.
# random_delay = randrange(10)

# this is the time between executiuons if the script is used as service (--service option)
service_sleep_time = 120
update_check_interval = 3600 # 1 hour
cpu_load = True
cpu_temp = True
used_space = True
used_space_path = '/'
voltage = False
sys_clock_speed = False
swap = False
memory = True
uptime = True
uptime_seconds = False

# Enable wifi_signal for unit of measuring % or wifi_signal_dbm for unit of meaning dBm
wifi_signal = False
wifi_signal_dbm = False

# this works only on raspbery pi version 5 with stock fan
rpi5_fan_speed = False
