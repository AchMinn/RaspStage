import paho.mqtt.client as mqtt
import re
import subprocess
import time

# MQTT configuration
MQTT_BROKER = '192.168.0.103' 
MQTT_PORT = 1883
MQTT_TOPIC_ONOFF = 'smarthome/devices/onoff'
MQTT_TOPIC_INTENSITY = 'smarthome/devices/intensity'

# Initialize the MQTT client
mqtt_client = mqtt.Client()

def check_wifi(ssid):
    """Check if connected to the specified Wi-Fi SSID."""
    try:
        current_ssid = subprocess.check_output(["iwgetid", "-r"]).decode().strip()
        return current_ssid == ssid
    except Exception as e:
        print(f"Error checking Wi-Fi: {e}")
        return False

def wait_for_wifi(ssid):
    """Wait until connected to the specified SSID."""
    while not check_wifi(ssid):
        print(f"Waiting for Wi-Fi connection to SSID: {ssid}...")
        time.sleep(5)

def on_message(client, userdata, message):
    msg = message.payload.decode('utf-8')
    topic = message.topic
    print(f"Message received on topic '{topic}': {msg}")

    if topic == MQTT_TOPIC_ONOFF:
        handle_device_onoff(msg)
    elif topic == MQTT_TOPIC_INTENSITY:
        handle_intensity_change(msg)

def handle_device_onoff(msg):
    """Handle device on/off messages."""
    if "turned on" in msg:
        device_info = extract_device_info(msg)
        if device_info:
            device_name, device_type = device_info
            led_number = extract_led_number(device_name)
            if led_number is not None:
                print(f"Turning on {device_type}: {device_name}")
                mqtt_client.publish("SmartLightNode1_CMD", f"{led_number}_1")  # Turn on
            else:
                print("Error: LED number could not be extracted.")

    elif "turned off" in msg:
        device_info = extract_device_info(msg)
        if device_info:
            device_name, device_type = device_info
            led_number = extract_led_number(device_name)
            if led_number is not None:
                print(f"Turning off {device_type}: {device_name}")
                mqtt_client.publish("SmartLightNode1_CMD", f"{led_number}_0")  # Turn off
            else:
                print("Error: LED number could not be extracted.")

def extract_led_number(device_name):
    """Extract the LED number from the device name."""
    match = re.search(r'(\d+)', device_name)  # Find digits in the device name
    if match:
        return int(match.group(1))  # Return the number as an integer
    print(f"Error: No LED number found in '{device_name}'")
    return None

def handle_intensity_change(msg):
    """Handle intensity change messages."""
    intensity = extract_intensity(msg)
    device_info = extract_device_info(msg)
    if device_info and intensity is not None:
        device_name, device_type = device_info
        print(f"Setting intensity for: {device_name} to {intensity}")
        # Publish to a topic that only the Arduino knows
        mqtt_client.publish("TOPIC", f"Setting intensity for: {device_name} to {intensity}")
    else:
        print("Error: Intensity or device info could not be extracted.")

def extract_intensity(msg):
    """Extract intensity value from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        return parts[3]  # Intensity value is expected here
    print("Error: Intensity value could not be extracted.")
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

# Wait for Wi-Fi connection to the specified SSID
wait_for_wifi("AILAB")

# Connect to the MQTT broker
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    print(f"Error: Could not connect to MQTT broker: {e}")

# Assign the callback function
mqtt_client.on_message = on_message

# Subscribe to relevant topics
try:
    mqtt_client.subscribe(MQTT_TOPIC_ONOFF)
    mqtt_client.subscribe(MQTT_TOPIC_INTENSITY)
except Exception as e:
    print(f"Error: Could not subscribe to topics: {e}")

# Start the loop to process received messages
try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print(f"Error in MQTT loop: {e}")