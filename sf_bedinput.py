import automationhat as shield
import time
time.sleep(0.1)

# Initialization
try:
    shield.relay.one.read()
except RuntimeError:
    shield.relay.one.read()
# End initialization

while True:
    if shield.input.one.is_on():
        if shield.relay.one.is_on():
            print("Relay is already on.")
        if shield.relay.one.is_off():
            shield.relay.one.on()
            print("Relay is now on.")
   # if shield.input.one.is_off():
      #  if shield.relay.one.is_off():
      #      print("Relay is already off.")
      #  if shield.relay.one.is_on():
      #      shield.relay.one.off()
       #     print("Relay is now off.")
