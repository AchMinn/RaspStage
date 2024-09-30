import paho.mqtt.client as mqtt
import re
import json
import subprocess
import time

# MQTT configuration
MQTT_BROKER = '192.168.0.103'
MQTT_PORT = 1883

# Define topics for communication
MQTT_TOPIC_TEMPERATURE = 'smarthome/devices/temperature'
MQTT_TOPIC_MODE = 'smarthome/devices/mode'
MQTT_TOPIC_FAN_SPEED = 'smarthome/devices/fan_speed'
MQTT_TOPIC_OPTIONS = 'smarthome/devices/options'
MQTT_TOPIC_ONOFF = 'smarthome/devices/onoff'
MQTT_TOPIC_CLIMA_COMMAND = 'SmartClima_CMD'



# Initialize the MQTT client
mqtt_client = mqtt.Client()

# def check_wifi(ssid):
#     """Check if connected to the specified Wi-Fi SSID."""
#     try:
#         current_ssid = subprocess.check_output(["iwgetid", "-r"]).decode().strip()
#         return current_ssid == ssid
#     except Exception as e:
#         print(f"Error checking Wi-Fi: {e}")
#         return False

# def wait_for_wifi(ssid):
#     """Wait until connected to the specified SSID."""
#     while not check_wifi(ssid):
#         print(f"Waiting for Wi-Fi connection to SSID: {ssid}...")
#         time.sleep(5)

def on_message(client, userdata, message):
    msg = message.payload.decode('utf-8')
    topic = message.topic
    print(f"Message received on topic '{topic}': {msg}")

    if topic == MQTT_TOPIC_TEMPERATURE:
        handle_temperature_change(msg)
    elif topic == MQTT_TOPIC_MODE:
        handle_mode_change(msg)
    elif topic == MQTT_TOPIC_FAN_SPEED:
        handle_fan_speed_change(msg)
    elif topic == MQTT_TOPIC_OPTIONS:
        handle_option_change(msg)
    elif topic == MQTT_TOPIC_ONOFF:
        handle_on_off_change(msg)

def extract_device_info(msg):
    """Extract device name and type from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        device_name = parts[1]
        device_type = parts[3]
        return device_name, device_type
    print("Error: Device info could not be extracted.")
    return None

def send_command_to_esp(power, mode, temperature, fan_speed, options):
    """Send command to ESP8266 as JSON."""
    command = {
        "power": power,
        "mode": mode,
        "temp": temperature,
        "fan_speed": fan_speed,
        **options
    }
    mqtt_client.publish(MQTT_TOPIC_CLIMA_COMMAND, json.dumps(command))

def handle_temperature_change(msg):
    """Handle temperature change messages."""
    temperature = extract_temperature(msg)
    device_info = extract_device_info(msg)
    if device_info and temperature is not None:
        device_name, device_type = device_info
        print(f"Setting temperature for Clima: {device_name} to {temperature}°C")
        send_command_to_esp(1, None, temperature, None, {})

def handle_mode_change(msg):
    """Handle mode change messages."""
    mode = extract_mode(msg)
    device_info = extract_device_info(msg)
    
    if device_info and mode is not None:
        device_name, device_type = device_info
        print(f"Setting mode for Clima: {device_name} to {mode}")
        
        # Pass mode as a string, no conversion to int
        send_command_to_esp(1, mode, None, None, {})

def handle_fan_speed_change(msg):
    """Handle fan speed change messages."""
    fan_speed = extract_fan_speed(msg)
    device_info = extract_device_info(msg)
    if device_info and fan_speed is not None:
        device_name, device_type = device_info
        print(f"Setting fan speed for Clima: {device_name} to {fan_speed}")
        send_command_to_esp(1, None, None, fan_speed, {})

def handle_option_change(msg):
    """Handle option change messages."""
    options = extract_options(msg)
    device_info = extract_device_info(msg)
    if device_info and options:
        device_name, device_type = device_info
        print(f"Activating options for Clima: {device_name} with options {options}")
        send_command_to_esp(1, None, None, None, options)

def handle_on_off_change(msg):
    """Handle ON/OFF messages."""
    power_state = extract_on_off(msg)
    device_info = extract_device_info(msg)
    
    if device_info and power_state is not None:
        device_name, device_type = device_info        
        # Check if the device type is 'Clima'
        if device_type.lower() == 'clima':
            power = 1 if power_state == 'on' else 0
            print(f"Setting power state for Clima: {device_name} to {'ON' if power else 'OFF'}")
            send_command_to_esp(power, None, None, None, {})
        else:
            print(f"Ignoring ON/OFF command for non-Clima device: {device_name}")

def extract_on_off(msg):
    """Extract ON/OFF state from the message."""
    if "turned on" in msg:
        return 'on'
    elif "turned off" in msg:
        return 'off'
    print("Error: ON/OFF state could not be determined.")
    return None

def extract_temperature(msg):
    """Extract temperature value from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        return parts[3]
    print("Error: Temperature value could not be extracted.")
    return None

def extract_mode(msg):
    """Extract mode value from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        return parts[3]  # Adjust this as needed
    print("Error: Mode value could not be extracted.")
    return None

def extract_fan_speed(msg):
    """Extract fan speed from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        return parts[3]  # Adjust this as needed
    print("Error: Fan speed value could not be extracted.")
    return None

def extract_options(msg):
    """Extract additional options from the message."""
    options = {}
    
    if "Turbo" in msg:
        options['turbo'] = 1  # Activated
    if "Swing" in msg:
        options['swing'] = 1  # Activated
    if "LED" in msg:
        options['led'] = 1  # Activated
    if "Sleep" in msg:
        options['sleep'] = 1  # Activated
    
    return options if options else None  # Return None if no options found

# Wait for Wi-Fi connection to the specified SSID
# wait_for_wifi("AILAB")

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
    print(f"Subscribed to {MQTT_TOPIC_TEMPERATURE}")
    mqtt_client.subscribe(MQTT_TOPIC_MODE)
    print(f"Subscribed to {MQTT_TOPIC_MODE}")
    mqtt_client.subscribe(MQTT_TOPIC_FAN_SPEED)
    print(f"Subscribed to {MQTT_TOPIC_FAN_SPEED}")
    mqtt_client.subscribe(MQTT_TOPIC_OPTIONS)
    print(f"Subscribed to {MQTT_TOPIC_OPTIONS}")
    mqtt_client.subscribe(MQTT_TOPIC_ONOFF)
    print(f"Subscribed to {MQTT_TOPIC_ONOFF}")
except Exception as e:
    print(f"Error: Could not subscribe to topics: {e}")
# Start the loop to process received messages
try:
    mqtt_client.loop_forever()
    print("Connected Successfully")
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print(f"Error in MQTT loop: {e}")