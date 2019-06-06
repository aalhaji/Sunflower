# updating and checking the states, both locally and on the server
import SunflowerAPI as sF
import socket
import automationhat as shield
import threading
import time

TREATMENT_DURATION = 10 # testing
COOLDOWN_DURATION = 10 # testing

global cooldown_timer


class states:

    def updateLocalState(newState):
        open_state_file = open("/home/pi/sunflower/currentState.txt", "w")
        open_state_file.write(str(newState))
        open_state_file.close()

    def checkLocalState():
        currentState_file = open("/home/pi/sunflower/currentState.txt", "r").read().splitlines()
        currentState = int(currentState_file[0])

        return currentState

    def updateServerState():

        dev_file = open("/home/pi/sunflower/devicename.txt", "r").read().splitlines()
        devname = dev_file[0]

        uuid_file = open("/home/pi/sunflower/uuid.txt", "r").read().splitlines()
        uuid = uuid_file[0]

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]

        sF.Devices.patchState(devname, uuid, ip_address)

    # def checkServerState():

    def stateCooldown():
        states.updateLocalState(2)

    def stateCleaning():
        states.updateLocalState(3)

class transitions:

    ## AFTER COOLDOWN FUNCTION ##

    def afterCool():

        cooldown_timer.cancel()

        states.stateCleaning()
        print("COOLDOWN FINISHED. NOW CLEANING.")
        print(time.ctime())
        states.updateServerState()

    ## END AFTER COOLDOWN FUNCTION ##


    ## AFTER ON FUNCTION ##
    def afterOn():

        shield.relay.one.off()
        print("RELAY TURNED OFF.")
        print(time.ctime())

        states.stateCooldown()
        print("COOLDOWN STARTED.")
        print(time.ctime())
        states.updateServerState()

        global cooldown_timer
        cooldown_timer = threading.Timer(COOLDOWN_DURATION, transitions.afterCool)
        cooldown_timer.start()


    ## END AFTER ON FUNCTION ##
