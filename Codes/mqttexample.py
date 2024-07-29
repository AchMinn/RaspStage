# This code will be on the computer receiving a messafe from the raspberry

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	channel = "channel"
	client.subscribe(channel)
	print(f"Connected to channel '{channel}' with result code : {rc}")

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