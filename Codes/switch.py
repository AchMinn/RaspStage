from gpiozero import LED, Button
from time import sleep

led1 = LED(25)
# button = Button(2)
button_state = False  # Initial state of the button

while True:

    # if button.is_pressed:
    if button_state:
        led1.on()
        if led1.is_lit:
            exec(open("mqttexampleLOCAL.py").read())
        else:
            print("There is an error")
    else:
        led1.off()
        if not led1.is_lit:
            exec(open("mqttexampleLOCAL2.py").read())
        else:
            print("There is an error")
            
    # Simulate button press/release
    button_state = not button_state
    sleep(2)  # Change button state every 2 seconds