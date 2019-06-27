import automationhat as shield
import time
import threading
import socket
import csv
from os import stat

from states import states, transitions

time_now = time.time()

global on_timer
on_timer = 0

#IP library
from internet_on import internet_on
if internet_on():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]

#######################################################################



states_dict={0:"AVAILABLE(OFF)",
        1: "WAITING_TO_AUTOSTART",
        2: "BED_ON",
        3: "COOLDOWN",
        4: "CLEANING"
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

        time.sleep(2) # allows room for state to be changed from POS

        currentState = states.checkLocalState()

        value = shield.analog.one.read()

        if (value > 1):

            # the '0.3' is because the analog signal only stabilizes after that time

            if ((time.time()-time_now) > 0.3):

                if currentState == 1: # if you're waiting to start

                    print("Button pressed to start bed.")

                    dur_file = open("txt/durations.txt", "r").read().splitlines()
                    treatmentDuration = int(dur_file[0])
                    cooldownDuration = int(dur_file[1])
                    autostartDuration = int(dur_file[2])

                    print("Autostart timer interrupted from BUTTON.")
                    BUTTON_STARTED_FROM_BED = 1

                    transitions.afterAutostart(treatmentDuration, cooldownDuration, autostartDuration, BUTTON_STARTED_FROM_BED)

                    # debouncing here
                    time.sleep(2)

                    time_now = time.time()

                    break


                elif currentState == 2: # if you're on

                    print("Button pressed while bed is on.")
                    print("Bed cannot be turned off from the button.")
                    print("Must be turned off from the POS.")

                    time_now = time.time()

                    break

                elif currentState == 3: # if you're in cooldown

                    print("Button pressed during cooldown.")
                    print("Please wait until cooldown is done.")

                elif currentState == 4: # if you're in cleaning

                    print("Button was pressed to declare cleaning done.")
                    currentState = 0
                    states.updateLocalState(currentState)
                    states.updateServerState()

                    #debouncing
                    time.sleep(5)

                    time_now = time.time()
                    break

                else: # elif state 0
                    print("Bed needs durations to be input from the POS.")
                    time_now = time.time()
                    break
