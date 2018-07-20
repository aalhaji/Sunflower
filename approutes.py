import automationhat as shield

class routes:
    def home_page():

        output = "Welcome to Sunflower!"
        return output

    def bedon():

        bedstatus = shield.input.one.read()

        if (bedstatus == 1):
            shield.relay.one.on()
            return "The bed is already on."
        else:
            shield.relay.one.on()
            return "The bed is now on."

    def bedoff():

        bedstatus = shield.input.one.read()

        if(bedstatus == 0):
            shield.relay.one.off()
            return "The bed is already off."
        else:
            shield.relay.one.off()
            return "The bed is now off."
