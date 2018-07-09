# This script performs the following:
# 1) API selection
# 2) Database login
# 3) Device creation
# 4) Device confirmation

import SunflowerAPI as sF

# 1) API selection

sF.Login.selectAPI()

# 2) Database Login

sF.Login.credentials()
sF.Access.authenticate(sF.Login.username, sF.Login.password, sF.Login.client_id, sF.Login.client_secret, sF.Login.grant_type)

# 3) Device creation

sF.Devices.registerDevice()

# 4) Device confirmation

sF.Devices.getDevice(Devices.DeviceName, Login.uuid)
