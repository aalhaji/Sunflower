# updating and checking the states, both locally and on the server
import SunflowerAPI as sF
import socket


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
