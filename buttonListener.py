import automationhat as shield
import time
time.sleep(0.1)

wait = 1

# Initialization
try:
    shield.relay.one.read()
except RuntimeError:
    shield.relay.one.read()
# End initialization

# The variable "is_pressed" is meant to indicate the last stete of the button
# call it condittionally in the app, and reset it to 0 once
# the last has been fulfilled

class Listen():

    def buttonlisten():
        while True:
            if shield.input.one.is_on():
                print("Button pressed.")
                Listen.is_pressed = 1
                break


while True:
    Listen.buttonlisten()
    time.sleep(wait)
    Listen.buttonlisten()
    time.sleep(wait)
