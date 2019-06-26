# updating and checking the states, both locally and on the server
import SunflowerAPI as sF
import socket
import automationhat as shield
import threading
import time
import csv
import dataKeeper
from internet_on import internet_on

global auto_timer
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
    def afterOn(startTimeSec, startTime, cooldownDuration):

        ## the only TWO cases in which "auto_timer" would still be running
        ## is if the autostart timer was started from the POS
        ## but then the client clicked the button to start early
        ## since the buttonListener can't stop a timer that was started
        ## from the POS. We take care of it in this function
        ## since this function is the endpoint of *both* ways of turning
        ## on
        ## The second case is the rare case of route "starttest"

        if (auto_timer):
            auto_timer.cancel()
            print("autostart timer cancelled because bed started before timeout.")

        ## the case in which the "on_timer" is on is if you hit
        ## route bedoff() from POS during treatment

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

        # append new row

        useData_columns = ['DATE', 'START_TIME', 'START_TIME_SINCE_EPOCH', 'END_TIME', 'MINUTES_SPENT']
        useData_thisInstance = [
        { 'DATE':dateToday,
        'START_TIME':startTime,
        'START_TIME_SINCE_EPOCH':startTimeSec,
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

        global cooldown_timer
        cooldown_timer = threading.Timer(cooldownDuration, transitions.afterCool)
        cooldown_timer.start()

    ## END AFTER ON FUNCTION ##

    ## AFTER TIMEOUT FUNCTION (AUTOSTART TIMER DONE) ##

    def afterTimeout(treatmentDuration, cooldownDuration):

        # turn ON

        shield.relay.one.on()
        print("RELAY TURNED ON.")

        startTimeSec = time.time()
        startTime = time.strftime("%H:%M:%S", time.localtime())

        # State change protocol
        currentState = 1
        states.updateLocalState(currentState)
        states.updateServerState()

        global on_timer
        on_timer = threading.Timer(treatmentDuration, transitions.afterOn, args=[startTimeSec, startTime, cooldownDuration])
        on_timer.start()

    ## END AFTER TIMEOUT FUNCTION

    ## AUTOSTART FUNCTION ##

    def autoStart(treatmentDuration, cooldownDuration, autostartDuration):

        global auto_timer
        auto_timer = threading.Timer(autostartDuration, transitions.afterTimeout, args=[treatmentDuration, cooldownDuration])
        auto_timer.start()
