import automationhat as shield
import time
import threading
import socket
import csv


from states import states, transitions



on_timer = 0

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

        time.sleep(2) # allows room for state to be changed from POS

        currentState = states.checkLocalState()
        # if it was changed from the POS

        if currentState == (0 or 2 or 3):
            if(on_timer):
                on_timer.cancel()

        value = shield.analog.one.read()

        if (value > 1):

            # the '0.3' is because the analog signal only stabilizes after that time

            if ((time.time()-time_now) > 0.3):

                if currentState == 0: # if you're off

                    print("Button pressed to start bed.")
                    shield.relay.one.on()

                    global startTimeSec, startTime
                    startTimeSec = time.time()
                    startTime = time.strftime("%H:%M:%S", time.localtime())

                    currentState = 1
                    states.updateLocalState(currentState)
                    states.updateServerState()

                    dur_file = open("txt/durations.txt", "r").read().splitlines()
                    TREATMENT_DURATION = int(dur_file[0])

                    global on_timer
                    on_timer = threading.Timer(TREATMENT_DURATION, transitions.afterOn, args=[startTimeSec, startTime])
                    on_timer.start()

                    # debouncing here
                    time.sleep(2)

                    time_now = time.time()

                    break

                elif currentState == 1: # if you're on

                    print("Button pressed while bed is on.")
                    print("Bed cannot be turned off from the button.")
                    print("Must be turned off from the POS.")

                    time_now = time.time()

                    break

                    ## this code was from when the bed was allowed to turn OFF

            #        if mismatch != 1:
            #            on_timer.cancel()


            #        transitions.afterOn()

                    #debouncing
            #        time.sleep(5)



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
                    print("Error. Bed is in state {}.".format(currentState))
                    print("Bed cannot be turned off from the button.")
                    print("Must be turned off from the POS.")
                    time_now = time.time()
                    break
