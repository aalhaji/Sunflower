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

#States:

#0: AVAILABLE_NOT_STARTED
#1: AVAILABLE
#2: BED_STARTED
#3: BED_COOLING_DOWN
#4: NEEDS_CLEANING
#5: NOT_AVAILABLE_ERROR

states={0:"AVAILABLE_NOT_STARTED",
        1: "AVAILABLE",
        2: "BED_STARTED",
        3: "BED_COOLING_DOWN",
        4: "NEEDS_CLEANING",
        5: "NOT_AVAILABLE_ERROR"
        }

class routes:

    def bedready():

        currentState = 1 # states[1]
        state_open = open("currentState.txt", "w")
        state_open.write(str(currentState))
        state_open.close()

        sF.Devices.patchCurrentState(devname, uuid, ip_address)

        return "The bed is now ready."

    def bedon():

        shield.relay.one.on()

        currentState = 2 # states[2]
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

        currentState = states[1]
        state_open = open("currentState.txt", "w")
        state_open.write(str(currentState))
        state_open.close()

        sF.Devices.patchCurrentState(devname, uuid, ip_address)

        return "The bed is now off."
