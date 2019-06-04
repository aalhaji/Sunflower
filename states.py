# updating and checking the states, locally

class states:

    def updateLocalState(newStatus):
        open_state_file = open("/home/pi/sunflower/currentState.txt", "w")
        open_state_file.write(str(newStatus))
        open_state_file.close()

    def checkLocalState():
        currentState = int(open("/home/pi/sunflower/currentState.txt", "r").readline())
        return currentState

    def stateCooldown():
        states.updateLocalState(2)

    def stateCleaning():
        states.updateLocalState(3)
