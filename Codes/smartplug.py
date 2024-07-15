from gpiozero import SmartPlug
import time

# Création de l'objet smart plug
smart_plug = SmartPlug(17)

# Création de l'objet bouton
button = Button(2)

def smart_plug_control():
    # Vérifier l'état de chaque port
    active_sockets = 0
    for socket in range(1, 5):
        if smart_plug.is_active_socket(socket):
            active_sockets += 1
            last_active_time = time.time()
            print(f"Le port {socket} est utilisé")
    
    # Si aucun port n'est utilisé pendant 10 minutes, éteindre la smart plug
    if active_sockets == 0 and time.time() - last_active_time >= 600:
        print("Aucun port n'est utilisé depuis 10 minutes, extinction de la smart plug.")
        smart_plug.off()
    else:
        print(f"{active_sockets} port(s) sont utilisés.")
        
    # Attendre 30 secondes avant de vérifier à nouveau
    time.sleep(10)

def button_press():
    if smart_plug.is_on:
        smart_plug.off()
        print("Smart plug éteinte manuellement.")
    else:
        smart_plug.on()
        print("Smart plug allumée manuellement.")

# Boucle principale
while True:
    smart_plug_control()
    if button.is_pressed:
        button_press()