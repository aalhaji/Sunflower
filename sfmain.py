
# I/O libraries
import automationhat as shield
import time
time.sleep(0.1)
import threading # library for timers
import csv


global TREATMENT_DURATION
global COOLDOWN_DURATION

# default values go here
TREATMENT_DURATION = 10 # 15*60 TO GET 15 MINUTES
COOLDOWN_DURATION = 4 # + 60*3 to get 3 mins

global on_timer
global startTime, startTimeSec, endTime, endTimeSec
global dateToday, timeSpent, totalUseTime

# reset default duration values

#cooldur_file = open("/home/pi/sunflower/txt/treatmentDuration.txt", "w")
#cooldur_file.write(str(TREATMENT_DURATION))
#cooldur_file.close()

#cooldur_file = open("/home/pi/sunflower/txt/cooldownDuration.txt", "w")
#cooldur_file.write(str(COOLDOWN_DURATION))
#cooldur_file.close()

# IP library
import socket
from internet_on import internet_on



# Check if the internet is on, or operate offline
if internet_on():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]


# API library
import SunflowerAPI as sF

# states library
from states import states
from states import transitions

# PATCH IP ADDRESS

cred_file = open("/home/pi/sunflower/txt/credentials.txt", "r").read().splitlines() # Read file into Python dictionary
uuid_file = open("/home/pi/sunflower/txt/uuid.txt", "r").read().splitlines()

username = cred_file[0]
password = cred_file[1]
client_id = 'client-86a11a2564fb9b007b9901a21c10578753196d96'
client_secret = 'secret-7d6b06470b6b3d37367e3c5968fb91138d61509c'
grant_type = 'password'
uuid = uuid_file[0]

dev_open = open("/home/pi/sunflower/txt/devicename.txt", "r").read().splitlines()
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
        1: "BED_ON",
        2: "COOLDOWN",
        3: "CLEANING"
        }

# START APP

from flask import Flask

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

@app.route('/bedon')
def bedon():

    currentState = states.checkLocalState()
    str_state = states_dict[currentState]

    if currentState == (1 or 2 or 3):
        return "ERROR. The bed is currently in state: {}".format(str_state)

    else:
        # Turn on
        shield.relay.one.on()

        # Record start time
        global dateToday, startTimeSec, startTime
        dateToday = time.strftime("%d %b %Y", time.gmtime())
        startTimeSec = time.time()
        startTime = time.strftime("%H:%M:%S", time.gmtime())

        # State change protocol
        currentState = 1
        states.updateLocalState(currentState)
        states.updateServerState()

        # Get treatment duration

        trdur_file = open("txt/treatmentDuration.txt", "r").read().splitlines()
        rec_TREATMENT_DURATION = int(trdur_file[0])

        global TREATMENT_DURATION

        if rec_TREATMENT_DURATION != TREATMENT_DURATION:
            TREATMENT_DURATION = rec_TREATMENT_DURATION

        #state ON for 15 minutes

        global on_timer
        on_timer = threading.Timer(TREATMENT_DURATION, transitions.afterOn)
        on_timer.start()

    return "Bed turned ON."


@app.route('/bedoff')
def bedoff():

    # cancel timer if still on
    on_timer.cancel()

    # Record Off time
    global endTimeSec, endTime, timeSpent
    endTimeSec = time.time()
    endTime = time.strftime("%H:%M:%S", time.gmtime())
    timeSpent = (endTimeSec - startTimeSec) / 60

    currentState = states.checkLocalState()
    str_state = states_dict[currentState]


    if currentState == 0: # already off
        return "The bed is already in state: {}".format(str_state)

    elif  currentState == 1: # on

        transitions.afterOn()
        currentState = states.checkLocalState()
        str_state = states_dict[currentState]

        # Save run info to useData.csv

        useData_columns = ['DATE', 'START_TIME', 'END_TIME', 'MINUTES_SPENT']
        useData_thisInstance = [
        { 'DATE':dateToday,
        'START_TIME':startTime,
        'END_TIME':endTime,
        "MINUTES_SPENT":timeSpent }]

        useData_file = open("txt/useData.csv", "a")
        writer = csv.DictWriter(useData_file, fieldnames=useData_columns)

        for data in useData_thisInstance:
            writer.writerow()

        useData_file.close()

        return "The bed has been turned off. Bed is now in state: {}".format(str_state)

    elif currentState == 2: # cooldown

        transitions.afterCool()
        currentState = states.checkLocalState()
        str_state = states_dict[currentState]

        return "Cooldown was interrupted. Bed is now in state: {}".format(str_state)

    elif currentState == 3: # Cleaning

        currentState = 0
        str_state = states_dict[currentState]
        states.updateLocalState(currentState)
        states.updateServerState()

        return "Cleaning done. Bed is now in state: {}".format(str_state)

    else:
        return "Bed off."

@app.route('/onduration/<treatmentDuration>')

def onDuration(treatmentDuration):

    global TREATMENT_DURATION
    TREATMENT_DURATION = int(treatmentDuration)

    # Convert Minutes to Seconds, Uncomment this for Production
    #TREATMENT_DURATION = 60 * TREATMENT_DURATION

    trdur_file = open("/home/pi/sunflower/txt/treatmentDuration.txt", "w")
    trdur_file.write(treatmentDuration)
    trdur_file.close()

    print("Treatment duration recorded as {} minutes.".format(treatmentDuration))

    return("The treatment duration has been recorded as " + treatmentDuration + " minutes")


@app.route('/coolduration/<cooldownDuration>')

def coolDuration(cooldownDuration):

    global COOLDOWN_DURATION
    COOLDOWN_DURATION = int(cooldownDuration)

    # Convert Minutes to Seconds, uncomment this for production
    #COOLDOWN_DURATION = 60 * COOLDOWN_DURATION

    cooldur_file = open("/home/pi/sunflower/txt/cooldownDuration.txt", "w")
    cooldur_file.write(cooldownDuration)
    cooldur_file.close()

    # cooldown duration has to be recorded in a txt file because it's referenced in "states"


    print("Cooldown duration recorded as {} minutes.".format(cooldownDuration))

    return("The cooldown duration has been recorded as " + cooldownDuration + " minutes")

# if you want to test the bed, 2 mins

@app.route('/test')

def test():

    currentState = states.checkLocalState()
    str_state = states_dict[currentState]

    if currentState == (1 or 2 or 3):
        return "ERROR. The bed is currently in state: {}".format(str_state)

    else:
        shield.relay.one.on()
        currentState = 1

        states.updateLocalState(currentState)
        states.updateServerState()
        #state ON for 2 minutes

        TESTING_DURATION = 2 # * 60 # to convert to minutes

        global on_timer
        on_timer = threading.Timer(TESTING_DURATION, transitions.afterOn)
        on_timer.start()

    return "Bed turned ON."







if __name__ == "__main__":

    app.run(host='0.0.0.0')


    # OUTPUT
    # For relay, use NO side
    # Connect 5V power supply to NO
    # Connect COM to LOAD (BED)
    # GROUND THE LOAD ON THE OTHER SIDE
