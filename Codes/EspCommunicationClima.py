import paho.mqtt.client as mqtt
import re

# MQTT configuration
MQTT_BROKER = '192.168.0.103' 
MQTT_PORT = 1883
MQTT_TOPIC_TEMPERATURE = 'smarthome/devices/temperature'

# Initialize the MQTT client
mqtt_client = mqtt.Client()

def on_message(client, userdata, message):
    msg = message.payload.decode('utf-8')
    topic = message.topic
    print(f"Message received on topic '{topic}': {msg}")

    if topic == MQTT_TOPIC_TEMPERATURE:
        handle_temperature_change(msg)


def extract_clima_number(device_name):
    """Extract the LED number from the device name."""
    match = re.search(r'(\d+)', device_name)  # Find digits in the device name
    if match:
        return int(match.group(1))  # Return the number as an integer
    print(f"Error: No LED number found in '{device_name}'")
    return None

def handle_temperature_change(msg):
    """Handle temperature change messages."""
    temperature = extract_temperature(msg)
    device_info = extract_device_info(msg)
    if device_info and temperature is not None:
        device_name, device_type = device_info
        print(f"Setting temperature for Clima: {device_name} to {temperature}°C")
        # Add logic to set the temperature
    else:
        print("Error: Temperature or device info could not be extracted.")

def extract_temperature(msg):
    """Extract temperature value from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        return parts[3]  # Temperature value is expected here
    print("Error: Temperature value could not be extracted.")
    return None

def extract_device_info(msg):
    """Extract device name and type from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        device_name = parts[1]  # Device name
        device_type = parts[3]   # Device type
        return device_name, device_type
    print("Error: Device info could not be extracted.")
    return None

# Connect to the MQTT broker
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    print(f"Error: Could not connect to MQTT broker: {e}")

# Assign the callback function
mqtt_client.on_message = on_message

# Subscribe to relevant topics
try:

    mqtt_client.subscribe(MQTT_TOPIC_TEMPERATURE)
except Exception as e:
    print(f"Error: Could not subscribe to topics: {e}")

# Start the loop to process received messages
try:
    mqtt_client.loop_forever()
    print("Connected Succesfully")
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print(f"Error in MQTT loop: {e}")