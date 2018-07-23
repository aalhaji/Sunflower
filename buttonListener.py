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

def buttonlisten():
    while True:
        if shield.input.one.is_on():
           # shield.relay.one.toggle()
            print("Button pressed.")
            break

while True:
    buttonlisten()
    time.sleep(wait)
    buttonlisten()
    time.sleep(wait)
