
# Libraries
import automationhat as shield

import time
time.sleep(0.1)
import threading

from os import stat

import csv

import socket
from internet_on import internet_on

import SunflowerAPI as sF

from states import states
from states import transitions

# Global variables

global auto_timer
global startTime, startTimeSec, endTime, endTimeSec
global dateToday, timeSpent, totalUseTime

# Check if the internet is on, or operate offline
if internet_on():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]


# PATCH IP ADDRESS

cred_file = open("txt/credentials.txt", "r").read().splitlines() # Read file into Python dictionary
uuid_file = open("txt/uuid.txt", "r").read().splitlines()

username = cred_file[0]
password = cred_file[1]
client_id = 'client-86a11a2564fb9b007b9901a21c10578753196d96'
client_secret = 'secret-7d6b06470b6b3d37367e3c5968fb91138d61509c'
grant_type = 'password'
uuid = uuid_file[0]

dev_open = open("txt/devinfo.txt", "r").read().splitlines()
devname = dev_open[0]

if internet_on():
    print("Establishing Database Connection...")
    print("==================================")
    sF.Access.authenticate(username, password, client_id, client_secret, grant_type)
    sF.Devices.patchIP(devname, uuid, ip_address)
else:
    print("No internet connection.")
    print("Sunflower operating exclusively offline.")
    print("==================================")

# END PATCH IP ADDRESS

# SHIELD INITIALIZATION
# Automation pHAT needs to run "setup" after the first command
# so it will raise a runtime error on
# the first command
# So this is to ignore the first runtime error

print("Initializing Automation pHAT")
shield.relay.one.off()
print("==================================")
states.updateLocalState(0)
states.updateServerState()

try:
    shield.relay.one.read()
except RuntimeError:
    shield.relay.one.off() # Ensure that relay is off

# END INITIALIZATION

# STATES

states_dict={0:"AVAILABLE(OFF)",
        1: "WAITING_TO_AUTOSTART",
        2: "BED_ON",
        3: "COOLDOWN",
        4: "CLEANING"
        }

# START APP

from flask import Flask, request, jsonify

# App config.
#DEBUG = True # debug mode
app = Flask(__name__)

@app.route('/')
def home():
    return("Welcome to Sunflower! Current relay status: {}".format(shield.relay.one.read()))

@app.route('/bedstatus')
def status():

    currentState = states.checkLocalState()
    str_state = states_dict[currentState]

    return "The current state is {}".format(str_state)

@app.route('/starttest')
def startTest():

    currentState = states.checkLocalState()
    str_state = states_dict[currentState]

    if currentState == (1 or 2 or 3):
        return "ERROR. The bed is currently in state: {}".format(str_state)

    else:

        # read treatment durations

        DURATIONS_EXIST = stat("txt/durations.txt").st_size

        if(DURATIONS_EXIST):

            dur_file = open("txt/durations.txt", "r").read().splitlines()
            autostartDuration = int(dur_file[2])

            global BED_STARTED_FROM_POS
            BED_STARTED_FROM_POS = 1

            # State change protocol
            currentState = 1
            states.updateLocalState(currentState)
            states.updateServerState()

            global autostart_timer
            autostart_timer = threading.Timer(autostartDuration, transitions.afterTimeout)

            autostart_timer.start()

            return "Autostart timer started to begin treatment."

        else:
            return "Please input durations in the POS."


@app.route('/bedoff')
def bedoff():

    currentState = states.checkLocalState()
    str_state = states_dict[currentState]


    if currentState == 0: # already off
        return "The bed is already in state: {}".format(str_state)

    elif currentState == 1: # waiting for autoStart

        # interrupt autotimer
        transitions.stopTimer("auto_timer")

        # change state back to 0
        currentState = 0
        states.updateLocalState(currentState)
        states.updateServerState()

    elif  currentState == 2: # on

        useFile = open("txt/useData.csv", "r")

        timesArray = useFile.readlines()[-1].split(",")

        startTime = timesArray[1]
        startTimeSec = timesArray[2]

        useFile.close()

        dur_file = open("txt/durations.txt", "r").read().splitlines()
        cooldownDuration = int(dur_file[1])

        transitions.afterOn(startTimeSec, startTime, cooldownDuration)
        currentState = states.checkLocalState()
        str_state = states_dict[currentState]

        return "The bed has been turned off. Bed is now in state: {}".format(str_state)

    elif currentState == 3: # cooldown

        #transitions.afterCool()
        #currentState = states.checkLocalState()
        #str_state = states_dict[currentState]

        #return "Cooldown was interrupted. Bed is now in state: {}".format(str_state)

        # can't interrupt cooldown (anymore)
        return "The bed is in cooldown. Please wait."

    elif currentState == 4: # Cleaning

        currentState = 0
        str_state = states_dict[currentState]
        states.updateLocalState(currentState)
        states.updateServerState()

        return "Cleaning done. Bed is now in state: {}".format(str_state)

    else:
        return "Bed off."


@app.route('/durations', methods=['GET']) #<int:treatmentDuration>/<int:cooldownDuration>')
def durations():

    treatment_duration = request.args.get('treatmentDuration', default=None)
    cooldown_duration = request.args.get('cooldownDuration', default=None)
    autostart_duration = request.args.get('autostartDuration', default=None)

    treatmentDuration = int(treatment_duration)
    cooldownDuration = int(cooldown_duration)
    autostartDuration = int(autostart_duration)

    # Convert Minutes to Seconds, Uncomment this for Production
    #TREATMENT_DURATION = 60 * TREATMENT_DURATION

    dur_file = open("txt/durations.txt", "w")
    dur_file.write(treatment_duration)
    dur_file.write("\n")
    dur_file.write(cooldown_duration)
    dur_file.write("\n")
    dur_file.write(autostart_duration)
    dur_file.close()

    print("Treatment duration recorded as {} seconds.".format(treatmentDuration))
    print("Cooldown duration recorded as {} seconds.".format(cooldownDuration))
    print("Autostart duration recorded as {} seconds.".format(autostartDuration))

    ## Here, start autostart timer

    transitions.autoStart(treatmentDuration, cooldownDuration, autostartDuration)

    return jsonify({'treatment': treatmentDuration,
                    'cooldown': cooldownDuration,
                    'autostart': autostartDuration})



if __name__ == "__main__":

    app.run(host='0.0.0.0')


    # OUTPUT
    # For relay, use NO side
    # Connect 5V power supply to NO
    # Connect COM to LOAD (BED)
    # GROUND THE LOAD ON THE OTHER SIDE
