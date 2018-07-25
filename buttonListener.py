import automationhat as shield
import time

time_now = time.time()

while True:

    value = shield.analog.one.read()

    if (value > 1):

        if ((time.time()-time_now) > 0.3):
            print(value)
            print("button pressed.")
            
        time_now = time.time()
