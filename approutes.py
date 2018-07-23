import automationhat as shield

class routes:
    
    def bedon():

        while True:
            bedstatus = shield.input.one.read()

            if (bedstatus == 1):
                shield.relay.one.on()
                return "The bed is already on."

            else:
                shield.relay.one.on()
                return "The bed is now on."

    def bedoff():

        while True:
            bedstatus = shield.input.one.read()

            if(bedstatus == 0):
                shield.relay.one.off()
                return "The bed is already off."
            else:
                shield.relay.one.off()
                return "The bed is now off."
