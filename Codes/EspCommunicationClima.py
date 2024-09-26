import paho.mqtt.client as mqtt
import re
import json

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
        send_command_to_esp(1, None, int(temperature), None, {})

def handle_mode_change(msg):
    """Handle mode change messages."""
    mode = extract_mode(msg)
    device_info = extract_device_info(msg)
    if device_info and mode is not None:
        device_name, device_type = device_info
        print(f"Setting mode for Clima: {device_name} to {mode}")
        send_command_to_esp(1, int(mode), None, None, {})

def handle_fan_speed_change(msg):
    """Handle fan speed change messages."""
    fan_speed = extract_fan_speed(msg)
    device_info = extract_device_info(msg)
    if device_info and fan_speed is not None:
        device_name, device_type = device_info
        print(f"Setting fan speed for Clima: {device_name} to {fan_speed}")
        send_command_to_esp(1, None, None, int(fan_speed), {})

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
        power = 1 if power_state == 'on' else 0
        print(f"Setting power state for Clima: {device_name} to {'ON' if power else 'OFF'}")
        send_command_to_esp(power, None, None, None, {})

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
    if "turbo" in msg:
        options['turbo'] = int(msg.get('turbo', 0))
    if "swing" in msg:
        options['swing'] = int(msg.get('swing', 0))
    if "led" in msg:
        options['led'] = int(msg.get('led', 0))
    if "sleep" in msg:
        options['sleep'] = int(msg.get('sleep', 0))
    return options

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
    mqtt_client.subscribe(MQTT_TOPIC_MODE)
    mqtt_client.subscribe(MQTT_TOPIC_FAN_SPEED)
    mqtt_client.subscribe(MQTT_TOPIC_OPTIONS)
    mqtt_client.subscribe(MQTT_TOPIC_ONOFF) 
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