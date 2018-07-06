import requests
import json

parameters = {"lat": 40.71, "lon": -74}

resp = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)

data = resp.json()

print(type(data))
print(data)


