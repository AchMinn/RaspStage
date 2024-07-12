# This code will be on the raspberryPI

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	print(f"Connected with result code : {rc}")
	client.subscribe("channel")

def on_message(client, userdata, msg):
	print(f"Received message on topic {msg.topic}:{msg.payload}")
 	
 	# Add command handling logic here
 	

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60) #Replace with MQTT broker's address
print("Listening Forever")
try:
	client.loop_forever()
except:
	print("Something happened while connecting the broker!")