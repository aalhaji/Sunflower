import automationhat as shield

global lastState
# STATES

# STATE 1 : READY
# STATE 2 : ON
# STATE 3 : OFF

class routes:

    def bedready():

        lastState = 1
        state_open = open("currentState.txt", "w")
        state_open.write(lastState)
        state_open.close()


        return "The bed is now ready."

    def bedon():

        #while True:
            #bedstatus = shield.input.one.read()

#            if (bedstatus == 1):
#                shield.relay.one.on()
#                return "The bed is already on."

#            else:
        shield.relay.one.on()

        lastState = 2
        state_open = open("currentState.txt", "w")
        state_open.write(lastState)
        state_open.close()

        return "The bed is now on."

    def bedoff():

        #while True:
        #    bedstatus = shield.input.one.read()

        #    if(bedstatus == 0):
        #        shield.relay.one.off()
        #        return "The bed is already off."
        #    else:
        shield.relay.one.off()

        lastState = 3
        state_open = open("currentState.txt", "w")
        state_open.write(lastState)
        state_open.close()

        return "The bed is now off."
