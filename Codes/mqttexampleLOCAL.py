# This code is to be executed on the local side

import paho.mqtt.publish as publish
# Replace these values with your MQTT broker's address and the channel you wish to publish to
mqtt_broker_address = "192.168.10.174"
mqtt_channel = "/SmartLightNode1"

# Message to be sent
msg = "Led is turned on"

# Publish the message 
publish.single(mqtt_channel, msg, hostname=mqtt_broker_address)
