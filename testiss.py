#import requests
#import json

#parameters = {"lat": 40.71, "lon": -74}

#resp = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)

#data = resp.json()

#print(type(data))
#print(data)

import time
import automationhat as ah
time.sleep(0.1)

#while True:
#    ah.output.one.write(1)
#    print(ah.input.two.read())
#    time.sleep(1)
#    ah.output.one.write(0)
#    print(ah.input.two.read())

print(ah.input.one.read())
