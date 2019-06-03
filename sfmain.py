# I/O libraries
import automationhat as shield
import time
time.sleep(0.1)

# IP library
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]

# API library
import SunflowerAPI as sF

# states library
import states

# PATCH IP ADDRESS
# this part has been debugged, just uncomment it when ready

cred_file = open("/home/pi/sunflower/credentials.txt", "r").read().splitlines() # Read file into Python dictionary
uuid_file = open("/home/pi/sunflower/uuid.txt", "r").read().splitlines()

username = cred_file[0]
password = cred_file[1]
client_id = 'client-86a11a2564fb9b007b9901a21c10578753196d96'
client_secret = 'secret-7d6b06470b6b3d37367e3c5968fb91138d61509c'
grant_type = 'password'
uuid = uuid_file[0]

dev_open = open("/home/pi/sunflower/devicename.txt", "r").read().splitlines()
devname = dev_open[0]

print("Establishing Database Connection...")
print("==================================")
sF.Access.authenticate(username, password, client_id, client_secret, grant_type)
sF.Devices.patchIP(devname, uuid, ip_address)

# END PATCH IP ADDRESS

# SHIELD INITIALIZATION
# Automation pHAT needs to run "setup" after the first command
# so it will raise a runtime error on
# the first command
# So this is to ignore the first runtime error

print("Initializing Automation pHAT")
shield.relay.one.off()
states.updateLocalState(0)
try:
    shield.relay.one.read()
except RuntimeError:
    shield.relay.one.off() # Ensure that relay is off
print("==================================")
# END INITIALIZATION

# STATES

states_dict={0:"AVAILABLE",
        1: "BED_ON",
        2: "COOLDOWN",
        3: "CLEANING",
        4: "NOT_AVAILABLE_ERROR"
        }

# START APP

from flask import Flask
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

    if currentState == (1 or 2 or 3 or 4):
        return "Error. The bed is currently in state: {}".format(str_state)

    else:
        shield.relay.one.on()
        currentState = 1 # states[1]
        str_state = states_dict[currentState]
        states.updateLocalState(currentState)
        return "The bed is now in state: {}".format(str_state)


if __name__ == "__main__":

    app.run(host='0.0.0.0')


    # OUTPUT
    # For relay, use NO side
    # Connect 5V power supply to NO
    # Connect COM to LOAD (BED)
    # GROUND THE LOAD ON THE OTHER SIDE
