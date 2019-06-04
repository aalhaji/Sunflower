# updating and checking the states, both locally and on the server
import SunflowerAPI as sF
import socket


class states:

    def updateLocalState(newState):
        open_state_file = open("/home/pi/sunflower/currentState.txt", "w")
        open_state_file.write(str(newState))
        open_state_file.close()

    def checkLocalState():
        currentState = int(open("/home/pi/sunflower/currentState.txt", "r").readline())
        return currentState

    def updateServerState():

        dev_file = open("/home/pi/sunflower/devicename.txt", "r").read().splitlines()
        devname = dev_file[0]

        uuid_file = open("/home/pi/sunflower/uuid.txt", "r").read().splitlines()
        uuid = uuid_file[0]

        sF.Devices.patchState(devname, uuid)

    # def checkServerState():

    def stateCooldown():
        states.updateLocalState(2)

    def stateCleaning():
        states.updateLocalState(3)
