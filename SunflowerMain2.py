# We'll start with the just the i/o, then incorporate the Flask stuff

# code logic for now
# 1) Read analog input
# 2) Make analog output using relay

import time
import automationhat
time.sleep(0.1)

# Read an input on port "one"
# This should stay generic in the app

# Function output





# Function input
while True:
    
    one = automationhat.analog.one.read()
    print(one)
    time.sleep(0.25)





