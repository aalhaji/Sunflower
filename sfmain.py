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

sF.Access.authenticate(username, password, client_id, client_secret, grant_type)
sF.Devices.patchIP(devname, uuid, ip_address)

# END PATCH IP ADDRESS

while True:
    if shield.input.one.is_on():
        shield.relay.one.on()
        print("Bed has been turned on from inside.")
    if shield.input.one.is_off():
        shield.relay.one.off()
        print("Bed has been turned off from inside.")

# START APP

from flask import Flask
app = Flask(__name__)

@app.route('/')

def home_page():

    output = "Welcome to Sunflower!"
    return output

@app.route('/bedon')

def bedon():

    bedstatus = shield.input.one.read()
    print(bedstatus) # for testing

    if (bedstatus == 1):
        shield.relay.one.off()
        time.sleep(0.1)
        shield.relay.one.on()
        return "The bed is now on."
    else:
        shield.relay.one.on()
        return "The bed is now on."

@app.route('/bedoff')

def bedoff():

    shield.relay.one.off()
    return 'The bed is now off.'

if __name__ == "__main__":
    app.run(host='0.0.0.0')


    # OUTPUT
    # For relay, use NO side
    # Connect 5V power supply to NO
    # Connect COM to LOAD (BED)
    # GROUND THE LOAD ON THE OTHER SIDE
