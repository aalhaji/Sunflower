# consider moving this chunk to a new file
class states:

    def updateLocalState(newStatus):
        open_state_file = open("/home/pi/sunflower/currentState.txt", "w")
        open_state_file.write(str(newStatus))
        open_state_file.close()

    def checkLocalState():
        currentState = open("/home/pi/sunflower/currentState.txt", "r").readline()
        return currentState
