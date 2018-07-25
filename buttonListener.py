import automationhat as shield
import time

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
bedon_time = 5 # 5 seconds for testing, 15 minutes of "bed_started"
cooling_time = 5 # 5 seconds for testing, 3 minutes for real

states={0:"AVAILABLE_NOT_STARTED",
        1: "AVAILABLE",
        2: "BED_STARTED",
        3: "BED_COOLING_DOWN",
        4: "NEEDS_CLEANING",
        5: "NOT_AVAILABLE_ERROR"
        }

while True:

    value = shield.analog.one.read()

    if (value > 1):

        if ((time.time()-time_now) > 0.3):
            #print(value)

            # BUTTON TO START BED

            print("Button pressed to start bed.")
            shield.relay.one.on()

            currentState = states[2]
            state_open = open("currentState.txt", "w")
            state_open.write(currentState)
            state_open.close()
            sF.Devices.patchCurrentState(devname, uuid, ip_address)


            startTime = time.ctime()
            print("Bed started at: {}".format(startTime))
            time.sleep(bedon_time)

            shield.relay.one.off()

            endTime = time.ctime()
            print("Bed turned off at: {}".format(endTime))

            # COOLING STATE

            print("Bed cooldown started at: {}".format(endTime))

            currentState = states[3]
            state_open = open("currentState.txt", "w")
            state_open.write(currentState)
            state_open.close()
            sF.Devices.patchCurrentState(devname, uuid, ip_address)

            time.sleep(cooling_time)

            cooldown_endtime = time.ctime()

            print("Bed cooldown ended at: {}".format(cooldown_endtime))
            


        time_now = time.time()
