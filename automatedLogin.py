import SunflowerAPI as sF
import socket


def automatedLogin():

    cred_file = open("/home/pi/sunflower/txt/credentials.txt", "r").read().splitlines() # Read file into Python dictionary
    uuid_file = open("/home/pi/sunflower/txt/uuid.txt", "r").read().splitlines()

    username = cred_file[0]
    password = cred_file[1]
    client_id = 'client-86a11a2564fb9b007b9901a21c10578753196d96'
    client_secret = 'secret-7d6b06470b6b3d37367e3c5968fb91138d61509c'
    grant_type = 'password'
    uuid = uuid_file[0]

    dev_open = open("/home/pi/sunflower/txt/devicename.txt", "r").read().splitlines()
    devname = dev_open[0]

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]

    print("Establishing Database Connection...")
    print("==================================")
    sF.Access.authenticate(username, password, client_id, client_secret, grant_type)
    sF.Devices.patchIP(devname, uuid, ip_address)

    return (devname, uuid, ip_address)
