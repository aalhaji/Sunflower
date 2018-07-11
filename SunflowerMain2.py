# I/O libraries
import time
import automationhat
time.sleep(0.1)

# IP library
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]

# API library
import SunflowerAPI as sF

# Microframework for web application
from flask import Flask
app = Flask(__name__)

# PATCH IP ADDRESS
# this part has been debugged, just uncomment it when ready

#cred_file = open("credentials.txt", "r").read().splitlines() # Read file into Python dictionary

#username = cred_file[0]
#password = cred_file[1]
#client_id = 'client-86a11a2564fb9b007b9901a21c10578753196d96'
#client_secret = 'secret-7d6b06470b6b3d37367e3c5968fb91138d61509c'
#grant_type = 'password'
#uuid = cred_file[2]

#dev_open = open("devicename.txt", "r").read().splitlines()
#devname = dev_open[0]

#sF.Access.authenticate(username, password, client_id, client_secret, grant_type)
#sF.Devices.patchIP(devname, uuid, ip_address)

# END PATCH IP ADDRESS

#global bool bedstatus

# START APP
while True:

    app.route('/bedon')

    def bedon():

        automationhat.relay.one.on()


    app.route('/bedoff')

    def bedoff():

        automationhat.relay.one.off()


    if __name__ == "__main__":

        app.run(host='0.0.0.0')

    # READ BED STATUS HERE

#input_voltage = automationhat.analog.one.read()
#    print("The input voltage is {}.".format(input_voltage))
#    time.sleep(0.25)

#    if (input_voltage < 1):
#        bedstatus = False # bed OFF
#        print("The bed is off.")
#    elif (input_voltage > 1 and input_voltage < 3):
#        bedstatus = False # UNDEFINED
##        print("Error. Undefined state.")
    #elif (input_voltage > 3 and input_voltage < 24):
#        bedstatus = True # bed ON
    #    print("The bed is on.")
#    else:
#        bedstatus = False # UNDEFINED
    #    print("Error. Input voltage is too high.")

    # CONFIGURE WEB APP HERE

#    @app.route('/'):

    #def home_page():

    #    if (bedstatus = True): bed = 'on'
    #    else: bed = "off"

    #    output = "Welcome to Sunflower. The bed is currently "+bed+". "+"MY IP address is " +ip+"."

    #    return output






    # OUTPUT
    # For relay, use NO side
    # Connect 5V power supply to NO
    # Connect COM to LOAD (BED)
    # GROUND THE LOAD ON THE OTHER SIDE

    #automationhat.relay.one.on()
