import automationhat as shield
import time
time.sleep(0.1)

wait = 2

# Initialization
try:
    shield.relay.one.read()
except RuntimeError:
    shield.relay.one.read()
# End initialization

def togglestate():
    while True:
        if shield.input.one.is_on():
            shield.relay.one.toggle()
            print("Change of state. Current relay status is {}.".format(shield.relay.one.read()))
            break

while True:
    togglestate()
    time.sleep(wait)
    togglestate()
    time.sleep(wait)


