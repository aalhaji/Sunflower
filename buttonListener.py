import automationhat as shield
import time

from states import states, transitions


TREATMENT_DURATION = 10 # TESTING
COOLDOWN_DURATION = 10 # testing

#IP library
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]

# API library
import SunflowerAPI as sF

cred_file = open("/home/pi/sunflower/credentials.txt", "r").read().splitlines() # Read file into Python dictionary

username = cred_file[0]
password = cred_file[1]
client_id = 'client-86a11a2564fb9b007b9901a21c10578753196d96'
client_secret = 'secret-7d6b06470b6b3d37367e3c5968fb91138d61509c'
grant_type = 'password'
uuid = cred_file[2]

dev_open = open("/home/pi/sunflower/devicename.txt", "r").read().splitlines()
devname = dev_open[0]

sF.Access.authenticate(username, password, client_id, client_secret, grant_type)

#######################################################################

time_now = time.time()

states_dict={0:"AVAILABLE(OFF)",
        1: "BED_ON",
        2: "COOLDOWN",
        3: "CLEANING"
        }

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
# initial state of 0

currentState = 0
sstates.updateLocalState(currentState)
states.updateServerState()

while True:

    while True:

        value = shield.analog.one.read()

        if (value > 1):

            if ((time.time()-time_now) > 0.3):
                #print(value)

                # BUTTON TO START BED

                currentState = states.checkLocalState()
                str_state = states_dict[currentState]

                if currentState == (1 or 2 or 3):
                    print("ERROR. The bed is currently in state: {}".format(str_state))

                else:
                    print("Button pressed to start bed.")
                    shield.relay.one.on()
                    currentState = 1
                    states.updateLocalState(currentState)
                    states.updateServerState()

                    #state ON for 15 minutes

                    on_timer = threading.Timer(TREATMENT_DURATION, transitions.afterOn)
                    on_timer.start()

                    break

    while True:

        value = shield.analog.one.read()

        if (value > 1):

            if ((time.time()-time_now) > 0.3):

                print("Bed cleaned. Time: {}".format(time.ctime()))

                currentState = 0
                states.updateLocalState(currentState)
                states.updateServerState()
                time.sleep(5) # debouncing
                time_now = time.time()
                break
