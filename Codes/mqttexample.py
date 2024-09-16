import paho.mqtt.client as mqtt

# Callback function to handle incoming messages
def on_message(client, userdata, message):
    msg = message.payload.decode('utf-8')
    topic = message.topic
    print(f"Message received on topic '{topic}': {msg}")

    if "turned on" in msg:
        # Handle regular device turn on
        if "Device" in msg:
            device_name = msg.split('"')[1]  # Extract device name
            print(f"Turning on Device: {device_name}")
            # Code to turn on the device

        # Handle outlet turn on
        elif "Outlet" in msg:
            outlet_info = msg.split('"')
            outlet_id = outlet_info[1]
            device_name = outlet_info[3]  # Extract device name
            print(f"Turning on Outlet: {outlet_id} on Device: {device_name}")
            # Code to turn on the outlet

    elif "turned off" in msg:
        # Handle regular device turn off
        if "Device" in msg:
            device_name = msg.split('"')[1]  # Extract device name
            print(f"Turning off Device: {device_name}")
            # Code to turn off the device

        # Handle outlet turn off
        elif "Outlet" in msg:
            outlet_info = msg.split('"')
            outlet_id = outlet_info[1]
            device_name = outlet_info[3]  # Extract device name
            print(f"Turning off Outlet: {outlet_id} on Device: {device_name}")
            # Code to turn off the outlet

    elif "changed to" in msg:
        # Handle intensity change
        if "Intensity" in msg:
            parts = msg.split('"')
            device_name = parts[1]
            intensity = parts[3]
            print(f"Setting Intensity for Device '{device_name}' to {intensity}")
            # Code to change the intensity

    elif "set to" in msg:
        # Handle temperature setting
        if "Temperature" in msg:
            parts = msg.split('"')
            device_name = parts[1]
            temperature = parts[3]
            print(f"Setting Temperature for Device '{device_name}' to {temperature}°C")
            # Code to set the temperature

# MQTT configuration
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883

# List of topics to subscribe to
topics = [
    'home/device1/control',
    'home/device2/control',
    'home/outlet1/control',
    'channel',
    # Add more device topics as needed
]

# Create an MQTT client instance
client = mqtt.Client()

# Assign the callback function
client.on_message = on_message

# Connect to the broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to each topic in the list
for topic in topics:
    client.subscribe(topic)

# Start the loop to process received messages
client.loop_forever()