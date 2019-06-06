# updating and checking the states, both locally and on the server
import SunflowerAPI as sF
import socket
import automationhat as shield
import threading
import time

global TREATMENT_DURATION
global COOLDOWN_DURATION

TREATMENT_DURATION = 10 # testing
COOLDOWN_DURATION = 10 # testing

global cooldown_timer


class states:

    def updateLocalState(newState):
        open_state_file = open("/home/pi/sunflower/txt/currentState.txt", "w")
        open_state_file.write(str(newState))
        open_state_file.close()

    def checkLocalState():
        currentState_file = open("/home/pi/sunflower/txt/currentState.txt", "r").read().splitlines()
        currentState = int(currentState_file[0])

        return currentState

    def updateServerState():

        from internet_on import internet_on
        if internet_on():
            dev_file = open("/home/pi/sunflower/txt/devicename.txt", "r").read().splitlines()
            devname = dev_file[0]

            uuid_file = open("/home/pi/sunflower/txt/uuid.txt", "r").read().splitlines()
            uuid = uuid_file[0]

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]

            sF.Devices.patchState(devname, uuid, ip_address)

        else:
            print("No internet connection. State change not patched to server.")

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

        cooldur_file = open("/home/pi/sunflower/txt/cooldownDuration.txt", "r").read().splitlines()
        rec_COOLDOWN_DURATION = int(cooldur_file[0])

        global COOLDOWN_DURATION

        if rec_COOLDOWN_DURATION != COOLDOWN_DURATION:
            COOLDOWN_DURATION = rec_COOLDOWN_DURATION

        global cooldown_timer
        cooldown_timer = threading.Timer(COOLDOWN_DURATION, transitions.afterCool)
        cooldown_timer.start()


    ## END AFTER ON FUNCTION ##
