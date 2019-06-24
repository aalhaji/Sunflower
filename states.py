# updating and checking the states, both locally and on the server
import SunflowerAPI as sF
import socket
import automationhat as shield
import threading
import time
import csv
import dataKeeper
from internet_on import internet_on

global TREATMENT_DURATION
global COOLDOWN_DURATION

TREATMENT_DURATION = 10 # testing
COOLDOWN_DURATION = 10 # testing

global cooldown_timer


class states:

    def updateLocalState(newState):
        open_state_file = open("txt/currentState.txt", "w")
        open_state_file.write(str(newState))
        open_state_file.close()

    def checkLocalState():
        currentState_file = open("txt/currentState.txt", "r").read().splitlines()
        currentState = int(currentState_file[0])

        return currentState

    def updateServerState():

        if internet_on():
            dev_file = open("txt/devinfo.txt", "r").read().splitlines()
            devname = dev_file[0]

            uuid_file = open("txt/uuid.txt", "r").read().splitlines()
            uuid = uuid_file[0]

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]

            sF.Devices.patchState(devname, uuid, ip_address)

        else:
            print("No internet connection. State change and use time not patched to server.")


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
    def afterOn(startTimeSec, startTime):

        currentState = states.checkLocalState()

        if currentState == 1:

            # Record Off time
            global dateToday, endTimeSec, endTime, timeSpent
            dateToday = time.strftime("%d %b %Y", time.localtime())
            endTimeSec = time.time()
            endTime = time.strftime("%H:%M:%S", time.localtime())
            startTimeSec = float(startTimeSec)
            timeSpent = (endTimeSec - startTimeSec) / 60


            shield.relay.one.off()
            print("RELAY TURNED OFF.")

            useData_columns = ['DATE', 'START_TIME', 'END_TIME', 'MINUTES_SPENT']
            useData_thisInstance = [
            { 'DATE':dateToday,
            'START_TIME':startTime,
            'END_TIME':endTime,
            "MINUTES_SPENT":timeSpent }]

            useData_file = open("txt/useData.csv", "a")
            writer = csv.DictWriter(useData_file, fieldnames=useData_columns)

            for data in useData_thisInstance:
                writer.writerow(data)

            useData_file.close()

            ##### STATE CHANGE PROTOCOL

            states.stateCooldown()
            print("COOLDOWN STARTED.")
            states.updateServerState()

            ##### COOLDOWN PROTOCOL

            cooldur_file = open("txt/cooldownDuration.txt", "r").read().splitlines()
            rec_COOLDOWN_DURATION = int(cooldur_file[0])

            global COOLDOWN_DURATION

            if rec_COOLDOWN_DURATION != COOLDOWN_DURATION:
                COOLDOWN_DURATION = rec_COOLDOWN_DURATION

            global cooldown_timer
            cooldown_timer = threading.Timer(COOLDOWN_DURATION, transitions.afterCool)
            cooldown_timer.start()





    ## END AFTER ON FUNCTION ##
