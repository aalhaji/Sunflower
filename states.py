# updating and checking the states, both locally and on the server
import SunflowerAPI as sF
import socket
import automationhat as shield
import threading
import time
import csv
import dataKeeper
from internet_on import internet_on


global on_timer
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
            print("No internet connection. State change and use data not patched to server.")


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
        states.updateServerState()

        ## CLEAR DURATIONS (to prevent unauthorized use)
        open("txt/durations.txt", "w").close()



    ## END AFTER COOLDOWN FUNCTION ##


    ## AFTER ON FUNCTION ##
    def afterOn(startTimeSec, startTime):

        if (on_timer):
            on_timer.cancel()

        # Record Off time

        dateToday = time.strftime("%d %b %Y", time.localtime())
        #startTime = startTime
        endTimeSec = time.time()
        endTime = time.strftime("%H:%M:%S", time.localtime())
        startTimeSec = float(startTimeSec)
        timeSpent = (endTimeSec - startTimeSec) / 60 # in minutes


        shield.relay.one.off()
        print("RELAY TURNED OFF.")

        useData_columns = ['DATE', 'START_TIME', 'START_TIME_SINCE_EPOCH', 'END_TIME', 'MINUTES_SPENT']
        useData_thisInstance = [
        { 'DATE':dateToday,
        'START_TIME':startTime,
        'START_TIME_SINCE_EPOCH':startTimeSec,
        'END_TIME':endTime,
        "MINUTES_SPENT":timeSpent }]

        # here rewrite the row

        # first erase the last row

        useData_file = open("txt/useData.csv", "r+w")
        lines = useData_file.readlines()
        lastRow =lines[:-1]

        eraser = csv.writer(useFile, delimiter=',')
        for data in lastRow:
            eraser.writerow(data)

        useData_file.close()

        # second, write over it

        useData_file = open("txt/useData.csv", "a")
        writer = csv.DictWriter(useData_file, fieldnames=useData_columns)

        for data in useData_thisInstance:
            writer.writerow(data)

        writeFile.close()

        ##### STATE CHANGE PROTOCOL

        states.stateCooldown()
        print("COOLDOWN STARTED.")
        states.updateServerState()

        ##### COOLDOWN PROTOCOL

        cooldur_file = open("txt/durations.txt", "r").read().splitlines()
        cooldownDuration = int(cooldur_file[1])

        global cooldown_timer
        cooldown_timer = threading.Timer(cooldownDuration, transitions.afterCool)
        cooldown_timer.start()

    ## END AFTER ON FUNCTION ##

    ## AFTER TIMEOUT FUNCTION (AUTOSTART TIMER DONE) ##

    def afterTimeout():

        # turn ON

        dur_file = open("txt/durations.txt", "r").read().splitlines()
        treatmentDuration = int(dur_file[0])

        shield.relay.one.on()
        print("RELAY TURNED ON.")

        startTimeSec = time.time()
        startTime = time.strftime("%H:%M:%S", time.localtime())

        useData_columns = ['DATE', 'START_TIME', 'START_TIME_SINCE_EPOCH', 'END_TIME', 'MINUTES_SPENT']
        useData_thisInstance = [
        { 'DATE':'0',
        'START_TIME':startTime,
        'START_TIME_SINCE_EPOCH':startTimeSec,
        'END_TIME':'0',
        "MINUTES_SPENT":'0' }]

        useData_file = open("txt/useData.csv", "a")
        writer = csv.DictWriter(useData_file, fieldnames=useData_columns)

        for data in useData_thisInstance:
            writer.writerow(data)

        useData_file.close()

        # State change protocol
        currentState = 1
        states.updateLocalState(currentState)
        states.updateServerState()

        global on_timer
        on_timer = threading.Timer(treatmentDuration, transitions.afterOn, args=[startTimeSec, startTime])
        on_timer.start()

    ## END AFTER TIMEOUT FUNCTION
