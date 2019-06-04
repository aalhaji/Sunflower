def automatedLogin():
    
    cred_file = open("/home/pi/sunflower/credentials.txt", "r").read().splitlines() # Read file into Python dictionary
    uuid_file = open("/home/pi/sunflower/uuid.txt", "r").read().splitlines()

    username = cred_file[0]
    password = cred_file[1]
    client_id = 'client-86a11a2564fb9b007b9901a21c10578753196d96'
    client_secret = 'secret-7d6b06470b6b3d37367e3c5968fb91138d61509c'
    grant_type = 'password'
    uuid = uuid_file[0]

    dev_open = open("/home/pi/sunflower/devicename.txt", "r").read().splitlines()
    devname = dev_open[0]

    print("Establishing Database Connection...")
    print("==================================")
    sF.Access.authenticate(username, password, client_id, client_secret, grant_type)
    sF.Devices.patchIP(devname, uuid, ip_address)
