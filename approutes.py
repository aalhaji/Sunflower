import automationhat as shield

# IP library
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]

# API library
import SunflowerAPI as sF

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

sF.Access.authenticate(username, password, client_id, client_secret, grant_type)

#States:

#0: AVAILABLE
#1: BED_ON
#2: COOLDOWN
#3: CLEANING
#4: NOT_AVAILABLE_ERROR

states={0:"AVAILABLE",
        1: "BED_ON",
        2: "COOLDOWN",
        3: "CLEANING",
        4: "NOT_AVAILABLE_ERROR"
        }

class routes:

    def bedready():

        currentState = 0  # states[0]
        state_open = open("currentState.txt", "w")
        state_open.write(str(currentState))
        state_open.close()

        sF.Devices.patchCurrentState(devname, uuid, ip_address)

        return "The bed is now ready."

    def bedstatus():

        state_open = open("currentState.txt", "r").read().splitlines()
        currentState = int(state_open[0])
        str_state = states[currentState]
       # state_open.close()

        return "The current state is {}".format(str_state)

    def bedon():
        state_open = open("currentState.txt", "r").read().splitlines()
        currentState = int(state_open[0])
        str_state = states[currentState]
       # state_open.close()

        if currentState == (1 or 2 or 3 or 4):
            return "Error. The bed is currently in state: {}".format(str_state)

        else:
            shield.relay.one.on()
            currentState = 1 # states[1]
            str_state = states[currentState]
            state_write = open("currentState.txt", "w")
            state_write.write(str(currentState))
            state_write.close()

            return "The bed is now in state: {}".format(str_state)
