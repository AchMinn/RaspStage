from gpiozero import LED, Button
from time import sleep

led1 = LED(25)
button = Button(2)

while True:

    if button.is_pressed:
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
    sleep(1)