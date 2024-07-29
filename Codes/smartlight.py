from gpiozero import LightSensor, PWMLED
from signal import pause

# Replace these values with your MQTT broker's address and the channel you wish to publish to
mqtt_broker_address = "192.168.10.174"
mqtt_channel = "/SmartLightNode1"

sensor = LightSensor(18)
ambient_sensor = LightSensor(15)
led = PWMLED(16)

button = Button(19)

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

def button_pressed():
    if led.value == 0:
        led.value = 1
        publish.single(mqtt_channel, "Lumière allumée manuellement", hostname=mqtt_broker_address)
    else:
        led.value = 0
        publish.single(mqtt_channel, "Lumière éteinte manuellement", hostname=mqtt_broker_address)


while True:
	button.when_pressed = button_pressed()
	led.source = lambda: 1 - ambient_sensor.value
	check_light_level()
