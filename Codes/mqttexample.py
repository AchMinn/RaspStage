import paho.mqtt.client as mqtt

# MQTT configuration
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_ONOFF = 'smarthome/devices/onoff'
MQTT_TOPIC_OUTLET = 'smarthome/devices/outlet'
MQTT_TOPIC_INTENSITY = 'smarthome/devices/intensity'
MQTT_TOPIC_TEMPERATURE = 'smarthome/devices/temperature'

# Initialize the MQTT client
mqtt_client = mqtt.Client()

def on_message(client, userdata, message):
    msg = message.payload.decode('utf-8')
    topic = message.topic
    print(f"Message received on topic '{topic}': {msg}")

    if topic == MQTT_TOPIC_ONOFF:
        handle_device_onoff(msg)
    elif topic == MQTT_TOPIC_OUTLET:
        handle_outlet_control(msg)
    elif topic == MQTT_TOPIC_INTENSITY:
        handle_intensity_change(msg)
    elif topic == MQTT_TOPIC_TEMPERATURE:
        handle_temperature_change(msg)

def handle_device_onoff(msg):
    """Handle device on/off messages."""
    if "turned on" in msg:
        device_info = extract_device_info(msg)
        if device_info:
            device_name, device_type = device_info
            print(f"Turning on {device_type}: {device_name}")
            # Add logic to turn on the device

    elif "turned off" in msg:
        device_info = extract_device_info(msg)
        if device_info:
            device_name, device_type = device_info
            print(f"Turning off {device_type}: {device_name}")
            # Add logic to turn off the device

def handle_outlet_control(msg):
    """Handle outlet control messages."""
    if "turned on" in msg:
        outlet_info = extract_outlet_info(msg)
        if outlet_info:
            outlet_id, device_name = outlet_info
            print(f"Turning on outlet: {outlet_id} on device: {device_name}")
            # Add logic to turn on the outlet

    elif "turned off" in msg:
        outlet_info = extract_outlet_info(msg)
        if outlet_info:
            outlet_id, device_name = outlet_info
            print(f"Turning off outlet: {outlet_id} on device: {device_name}")
            # Add logic to turn off the outlet

def handle_intensity_change(msg):
    """Handle intensity change messages."""
    intensity = extract_intensity(msg)
    device_info = extract_device_info(msg)
    if device_info and intensity is not None:
        device_name, device_type = device_info
        print(f"Setting intensity for {device_type}: {device_name} to {intensity}")
        # Add logic to change intensity

def handle_temperature_change(msg):
    """Handle temperature change messages."""
    temperature = extract_temperature(msg)
    device_info = extract_device_info(msg)
    if device_info and temperature is not None:
        device_name, device_type = device_info
        print(f"Setting temperature for {device_type}: {device_name} to {temperature}°C")
        # Add logic to set the temperature

def extract_intensity(msg):
    """Extract intensity value from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        return parts[3]  # Intensity value is expected here
    return None

def extract_temperature(msg):
    """Extract temperature value from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        return parts[3]  # Temperature value is expected here
    return None

def extract_device_info(msg):
    """Extract device name and type from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        device_name = parts[1]  # Device name
        device_type = parts[3]   # Device type
        return device_name, device_type
    return None

def extract_outlet_info(msg):
    """Extract outlet ID and associated device name from the message."""
    parts = msg.split("'")
    if len(parts) >= 5:
        outlet_id = parts[1]     # Outlet ID
        device_name = parts[3]    # Device name
        return outlet_id, device_name
    return None

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Assign the callback function
mqtt_client.on_message = on_message

# Subscribe to relevant topics
mqtt_client.subscribe(MQTT_TOPIC_ONOFF)
mqtt_client.subscribe(MQTT_TOPIC_OUTLET)
mqtt_client.subscribe(MQTT_TOPIC_INTENSITY)
mqtt_client.subscribe(MQTT_TOPIC_TEMPERATURE)

# Start the loop to process received messages
mqtt_client.loop_forever()