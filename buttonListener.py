import automationhat as shield
import time
import threading
import socket


from states import states, transitions

# should always fetch duration values from txt, whether "last recorded" or "default"

global TREATMENT_DURATION
global COOLDOWN_DURATION

TREATMENT_DURATION = int((open("/home/pi/sunflower/txt/treatmentDuration.txt", "r").read().splitlines())[0])
COOLDOWN_DURATION = int((open("/home/pi/sunflower/txt/cooldownDuration.txt", "r").read().splitlines())[0])

global on_timer


#IP library
from internet_on import internet_on
if internet_on():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]

#######################################################################

time_now = time.time()

states_dict={0:"AVAILABLE(OFF)",
        1: "BED_ON",
        2: "COOLDOWN",
        3: "CLEANING"
        }

# this func here for testing purposes

def bedAvailable():

    time_now = time.time()

    val = shield.analog.one.read()

    if (val > 1):

        if((time.time()-time_now) > 0.3):

            print("Bed Available. Not started.")

            currentState = 0

            states.updateLocalState(currentState)
            states.updateServerState()

##########################################################################

# LISTENS FOR BUTTON TO TURN ON
while True:

    while True:

        value = shield.analog.one.read()

        if (value > 1):

            # the '0.3' is because the analog signal only stabilizes after that time

            if ((time.time()-time_now) > 0.3):
                #print(value)

                # BUTTON TO START BED

                currentState = states.checkLocalState()

                if currentState == (0 or 1):
                    if currentState != shield.relay.one.read():
                        currentState == shield.relay.one.read()
                        states.updateLocalState(currentState)
                        states.updateServerState()


                if currentState == 0: # if you're off
                    print("Button pressed to start bed.")
                    shield.relay.one.on()
                    currentState = 1
                    states.updateLocalState(currentState)
                    states.updateServerState()


                    global on_timer
                    on_timer = threading.Timer(TREATMENT_DURATION, transitions.afterOn)
                    on_timer.start()

                    # debouncing here
                    time.sleep(5)

                    time_now = time.time()

                    break

                elif currentState == 1: # if you're on

                    shield.relay.one.off()
                    on_timer.cancel()
                    print("Button pressed to turn off bed.")
                    transitions.afterOn()

                    #debouncing
                    time.sleep(5)

                    time_now = time.time()

                    break

                elif currentState == 3: # if you're in cleaning

                    print("Button was pressed to declare cleaning done.")
                    currentState = 0
                    states.updateLocalState(currentState)
                    states.updateServerState()

                    #debouncing
                    time.sleep(5)

                    time_now = time.time()
                    break

                else:
                    currentState = states.checkLocalState()
                    print("Error. Bed is already in state {}.".format(currentState))
                    time_now = time.time()
                    break
