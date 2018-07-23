# I/O libraries
import time
import automationhat as shield
time.sleep(0.1)

# IP library
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]

# API library
import SunflowerAPI as sF

# App routes library
import approutes

# PATCH IP ADDRESS
# this part has been debugged, just uncomment it when ready

cred_file = open("/home/pi/sunflower/credentials.txt", "r").read().splitlines() # Read file into Python dictionary

username = cred_file[0]
password = cred_file[1]
client_id = 'client-86a11a2564fb9b007b9901a21c10578753196d96'
client_secret = 'secret-7d6b06470b6b3d37367e3c5968fb91138d61509c'
grant_type = 'password'
uuid = cred_file[2]

dev_open = open("/home/pi/sunflower/devicename.txt", "r").read().splitlines()
devname = dev_open[0]

print("Establishing Database Connection...")
print("================================")
sF.Access.authenticate(username, password, client_id, client_secret, grant_type)
sF.Devices.patchIP(devname, uuid, ip_address)

# END PATCH IP ADDRESS

# SHIELD INITIALIZATION
# Automation pHAT needs to run "setup" after the first command
# so it will raise a runtime error on
# the first command
# So this is to ignore the first runtime error

print("Initializing Automation pHAT")
try:
    shield.relay.one.read()
except RuntimeError:
    shield.relay.one.off() # Ensure that relay is off
print("================================")
# END INITIALIZATION

# START APP

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    approutes.routes.homepage()
    return "Welcome to Sunflower!"

@app.route('/bedon')
def onapp():
    approutes.routes.bedon()
    return "Bed on."

@app.route('/bedoff')
def offapp():
    approutes.routes.bedoff()
    return "Bed off."

@app.route('/status')

def state():
    return("Relay status: {}".format(shield.relay.one.read()))


if __name__ == "__main__":

    app.run(host='0.0.0.0')


    # OUTPUT
    # For relay, use NO side
    # Connect 5V power supply to NO
    # Connect COM to LOAD (BED)
    # GROUND THE LOAD ON THE OTHER SIDE
