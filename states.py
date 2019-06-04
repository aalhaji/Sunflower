# updating and checking the states, both locally and on the server
import SunflowerAPI as sF
import automatedLogin as aL


class states:

    def updateLocalState(newState):
        open_state_file = open("/home/pi/sunflower/currentState.txt", "w")
        open_state_file.write(str(newState))
        open_state_file.close()

    def checkLocalState():
        currentState = int(open("/home/pi/sunflower/currentState.txt", "r").readline())
        return currentState

    def updateServerState():
        sF.Devices.patchState(devname, uuid, ip_address)

    # def checkServerState():

    def stateCooldown():
        states.updateLocalState(2)

    def stateCleaning():
        states.updateLocalState(3)
