import automationhat as shield

# IP library
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

# STATES

# STATE 1 : READY
# STATE 2 : ON
# STATE 3 : OFF

class routes:

    def bedready():

        currentState = 1
        state_open = open("currentState.txt", "w")
        state_open.write(str(currentState))
        state_open.close()

        sF.Devices.patchCurrentState(devname, uuid, ip_address)


        return "The bed is now ready."

    def bedon():

        #while True:
            #bedstatus = shield.input.one.read()

#            if (bedstatus == 1):
#                shield.relay.one.on()
#                return "The bed is already on."

#            else:
        shield.relay.one.on()

        currentState = 2
        state_open = open("currentState.txt", "w")
        state_open.write(str(currentState))
        state_open.close()

        sF.Devices.patchCurrentState(devname, uuid, ip_address)

        return "The bed is now on."

    def bedoff():

        #while True:
        #    bedstatus = shield.input.one.read()

        #    if(bedstatus == 0):
        #        shield.relay.one.off()
        #        return "The bed is already off."
        #    else:
        shield.relay.one.off()

        currentState = 3
        state_open = open("currentState.txt", "w")
        state_open.write(str(currentState))
        state_open.close()

        sF.Devices.patchCurrentState(devname, uuid, ip_address)

        return "The bed is now off."
