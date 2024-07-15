from gpiozero import LightSensor, PWMLED
from signal import pause

# Replace these values with your MQTT broker's address and the channel you wish to publish to
mqtt_broker_address = "192.168.10.174"
mqtt_channel = "channel"

sensor = LightSensor(18)
led = PWMLED(16)

# Inverser la valeur du capteur de lumière
led.source = lambda: 1 - sensor.value

def check_light_level():
    while True:
        if sensor.value <= 0.25:
        	publish.single(mqtt_channel, "Niveau de lumière à 25% ou moins", hostname=mqtt_broker_address)
        elif sensor.value <= 0.5:
        	publish.single(mqtt_channel, "Niveau de lumière à 50% ou moins", hostname=mqtt_broker_address)
        elif sensor.value <= 0.75:
        	publish.single(mqtt_channel, "Niveau de lumière à 75% ou moins", hostname=mqtt_broker_address)
        elif sensor.value <= 1:
        	publish.single(mqtt_channel, "Niveau de lumière à 100%", hostname=mqtt_broker_address)
        pause(0.1)  # Pause de 0,1 seconde pour éviter de saturer la console

check_light_level()