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
global AUTO_TIMER_STARTED
AUTO_TIMER_STARTED = 0
global on_timer
global ON_TIMER_STARTED
ON_TIMER_STARTED = 0
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
        states.updateLocalState(3)

    def stateCleaning():
        states.updateLocalState(4)

class transitions:

    ## INTERRUPT TIMER FUNCTION ##

    def stopTimer(timer):

        if timer == "auto_timer":
            auto_timer.cancel()
            print("auto timer cancelled.")

        elif timer == "on_timer":
            on_timer.cancel()
            print("on timer cancelled.")

        elif timer == "cooldown_timer":
            cooldown_timer.cancel()
            print("cooldown timer cancelled.")

        else:
            print("Unidentified timer. Check spelling.")

    ## END INTERRUPT TIMER FUNCTION ##

    ## AFTER COOLDOWN FUNCTION ##

    def afterCool():

        transitions.stopTimer("cooldown_timer")

        states.stateCleaning()
        print("COOLDOWN FINISHED. NOW CLEANING.")
        states.updateServerState()

        ## CLEAR DURATIONS (to prevent unauthorized use)
        open("txt/durations.txt", "w").close()



    ## END AFTER COOLDOWN FUNCTION ##


    ## AFTER ON FUNCTION ##
    def afterOn(startTimeSec, startTime, cooldownDuration):

        ## the case in which the "on_timer" is on is if you hit
        ## route bedoff() from POS during treatment

        if (ON_TIMER_STARTED):
            global ON_TIMER_STARTED
            ON_TIMER_STARTED = 0
            transitions.stopTimer("on_timer")

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

    def afterAutostart(treatmentDuration, cooldownDuration, autostartDuration, BUTTON_STARTED_FROM_BED):

        global auto_timer
    #    global AUTO_TIMER_STARTED
    #    STARTED_FROM_BUTTON = 0
        auto_timer = threading.Timer(autostartDuration, transitions.turnOn, args=[treatmentDuration, cooldownDuration])
        #AUTO_TIMER_STARTED = 1
        auto_timer.start()

        if (BUTTON_STARTED_FROM_BED):
            # CANCEL TIMER THEN TURN ON
            transitions.stopTimer("auto_timer")
            transitions.turnOn(treatmentDuration, cooldownDuration)

        else:
            # just turn on
            print("timed out. starting now.")
            transitions.turnOn(treatmentDuration, cooldownDuration)



        ## the only case in which "auto_timer" would still be running
        ## is if the autostart timer was started from the POS
        ## but then the client clicked the button to start early
        ## since the buttonListener can't stop a timer that was started
        ## from the POS. We take care of it in this function
        ## since this function is the endpoint of *both* ways of turning
        ## on

        if (AUTO_TIMER_STARTED or STARTED_FROM_BUTTON):
            global AUTO_TIMER_STARTED
            AUTO_TIMER_STARTED = 0
            transitions.stopTimer("auto_timer")

    ## END AFTER TIMEOUT FUNCTION

    ## AUTOSTART FUNCTION ##

    def autoStart(treatmentDuration, cooldownDuration, autostartDuration):

        ## CHANGE TO STATE 1
        currentState = 1
        states.updateLocalState(currentState)
        states.updateServerState()

        transitions.afterAutostart(treatmentDuration, cooldownDuration, autoStartDuration)

    ## END AUTOSTART FUNCTION ##

    def turnOn(treatmentDuration, cooldownDuration):
        # turn ON

        shield.relay.one.on()
        print("RELAY TURNED ON.")

        startTimeSec = time.time()
        startTime = time.strftime("%H:%M:%S", time.localtime())

        # CHANGE TO STATE 2
        currentState = 2
        states.updateLocalState(currentState)
        states.updateServerState()

        global on_timer
        global ON_TIMER_STARTED
        on_timer = threading.Timer(treatmentDuration, transitions.afterOn, args=[startTimeSec, startTime, cooldownDuration])
        ON_TIMER_STARTED = 1
        on_timer.start()
