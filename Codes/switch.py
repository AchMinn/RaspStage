from gpiozero import LED, Button
from time import sleep
import paho.mqtt.publish as publish

# Replace these values with your MQTT broker's address and the channel you wish to publish to
mqtt_broker_address = "192.168.10.174"
mqtt_channel = "channel"

# Message to be sent
# msg = "Led is turned on"


led1 = LED(25)
# button = Button(2)
button_state = False  # Initial state of the button

while True:

    # if button.is_pressed:
    if button_state:
        led1.on()
        if led1.is_lit:
            publish.single(mqtt_channel, "Led is turned off", hostname=mqtt_broker_address)
        else:
            print("There is an error")
    else:
        led1.off()
        if not led1.is_lit:
            publish.single(mqtt_channel, "Led is turned on", hostname=mqtt_broker_address)
        else:
            print("There is an error")

    # Simulate button press/release
    button_state = not button_state
    sleep(2)  # Change button state every 2 seconds