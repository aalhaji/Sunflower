# This is a collection of functions to connect Sunflower's Raspberry Pi
# to the Countr API.
# Simply add "import SunflowerAPI" to a program in the same directory
# to start using these functions.
# You might need to refer to the library and class first
# e.g.  "SunflowerAPI.Access.authorize()" rather than "authorize()"


## add get stores
## make if status code its own fucntion then reference it in the functions
## find a cyclical way to refresh token

import requests
import json
import uuid
import socket

api_url_base = 'https://api-test.countr.rest/v2/' #'http://192.168.43.154:3030/v2/'

username = 'demo@countrhq.com'
password = 'Demo12345'
client_id = 'client-86a11a2564fb9b007b9901a21c10578753196d96'
client_secret = 'secret-7d6b06470b6b3d37367e3c5968fb91138d61509c'

grant_type = 'password'

fixed_uuid = 'ac04be98-7ec1-11e8-9bda-b827eb98dcda' # was generated from str(uuid.uuid1())

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]

############## LOGIN INFORMATION ###########

class Login:

    def credentials():

        Login.username = input("Please enter your username (usually an e-mail): ")
        Login.password = input("Please enter your password: ")
        Login.client_id = input("Please enter your client ID (carefully): ")
        Login.client_secret = input("Please enter your client secret (carefully): ")

        Login.uuid = str(uuid.uuid1())

################### ACCESS  ################

class Access:

############ FIRST TIME LOGIN ##############

    def authenticate(username, password, client_id, client_secret, grant_type):

        body ={"username":username,"password":password, "client_id":client_id, "client_secret":client_secret, "grant_type":grant_type}
        resp = requests.post(api_url_base+'oauth/token', data=body)

        if resp.status_code != 201:
            print("Authorization error. Error code: ", resp.status_code)

        Access.access_token = resp.json()["access_token"]
        Access.refresh_token = resp.json()["refresh_token"]
        Access.bearer = 'Bearer '+str(Access.access_token)

        print('Logged in. Access Token: {}'.format(Access.access_token))
        print('================================')

############ REFRESH TOKEN ##################

    def refresh(grant_type, client_id, client_secret, refresh_token):

        body ={"grant_type":grant_type, "client_id":client_id, "client_secret":client_secret, "refresh_token":refresh_token}
        resp = requests.post(api_url_base+'oauth/refresh', data=body)

        if resp.status_code != 200:
            print("Refresh token error. Error code: ", resp.status_code)

        Access.access_token = resp.json()["access_token"]
        Access.refresh_token = resp.json()["refresh_token"]
        Access.bearer = 'Bearer '+str(Access.access_token)

        print(resp.json())

        print('Token refreshed. Access Token: {}'.format(Access.access_token))

        return Access.access_token, Access.refresh_token

########### GET USER INFORMATION ################

    def getuserinfo(access_token):

        while True:
            body = {"Authorization":Access.bearer}
            resp = requests.get(api_url_base+'me', json=body, headers=body)

            if resp.status_code == 200:
                print(resp.json())
                print('==================================')
                break

            else:
                misc.Exception_Handler(resp)
                break

############# END CLASS 'ACCESS' ##################


################ STORES ###########################

class Stores:

################ GET STORES #######################

    def getStores(access_token):

        while True:

            body = {"Authorization":Access.bearer}
            resp = requests.get(api_url_base+'stores/simple', json=body, headers=body)


            if resp.status_code == 200 or 201:
                Stores.storedata = [] # initialize python dict
                for i in range(len(resp.json())):
                    Stores.storedata.append(dict(resp.json()[i])) # cast json to python dict
                break

            else:
                misc.Exception_Handler(resp)
                break

################## SELECT STORE ###################

    def selectStore(access_token):

        # First, get stores
        Stores.getStores(access_token)

        # Then display the stores in a numbered list

        print("List of stores registered to this user:")
        for i in range(len(Stores.storedata)):
            print("{}) {}".format(i+1, Stores.storedata[i]['name']))

        # Then get user input
        while True:
            selected_store = int(input("Please select the store number you'd like this device registered to: ")) - 1

            is_confirmed = input("You selected store '{}'. Confirm [y/n]? ".format(Stores.storedata[selected_store]['name']))

            if (is_confirmed == ('y' or 'Y')):
                print("Store '{}' selected.".format(Stores.storedata[selected_store]['name']))
                Stores.store_id = str(Stores.storedata[selected_store]['_id'])
                break

            else:
                print("Store not selected. Starting over...")

##################### DEVICES #####################

class Devices:

############## CREATE  DEVICE #####################

    def createDevice(name, uuid, store):

        while True:
            body = {"name":name, "uuid":uuid, "store":store}
            resp = requests.post(api_url_base+'devices', data=body, headers={"Authorization":Access.bearer, "Content-Type":'application/x-www-form-urlencoded'})

            if resp.status_code == 200 or 201:
                print("Device has been created.")
                print('==================================')
                break

            else:
                misc.Exception_Handler(resp)
                break


############# GET SPECIFIC DEVICE ################

    def getDevice(name, uuid):

        while True:
            body = {"name":name, "uuid":uuid},
            resp = requests.get(api_url_base+'devices/'+uuid, data=body, headers={"Authorization":Access.bearer, "Content-Type":'application/x-www-form-urlencoded'})

            if resp.status_code == 200:
                print(resp.json())
                print('==================================')
                break

            else:
                misc.Exception_Handler(resp)
                break

############# SEND IP ADDRESS #####################


    def patchIP(name, uuid,  ip_address):

        while True:
            body = {"name":name, "uuid":uuid, "info.ip_address":ip_address}
            resp = requests.patch(api_url_base+'devices/'+uuid, data=body, headers={"Authorization":Access.bearer})

            if resp.status_code == 200:
                print("IP has been sent.")
                print('==================================')
                break

            else:
                misc.Exception_Handler(resp)
                break

########## DEVICE REGISTRATION PROMPT #############

    def registerDevice():

        print("Device Registration Starting.")

        ### 1) NAME

        while True:
            Devices.DeviceName = input("1) Please enter your desired device name:")
            is_confirmed = input("Name '{}' selected. Confirm [y/n]?".format(Devices.DeviceName))

            if (is_confirmed == ('y' or 'Y')):
                print("Name '{}' confirmed.".format(Devices.DeviceName))
                break
            else:
                print("Starting over...")


        ### 2) STORE SELECTION

        print("2) Please select your store:")
        Stores.selectStore(Access.access_token)

        ### 3) CREATE DEVICE

        print("Device being created...")
        Devices.createDevice(Devices.DeviceName, fixed_uuid, Stores.store_id)

        ### 4) PATCH IP ADDRESS
        
        print("Sending IP Address to Countr Database...")
        Devices.patchIP(Devices.DeviceName, fixed_uuid, ip_address)


########### END CLASS 'DEVICES' ####################

########### MISCELLANEOUS FUNCTIONS ################

class misc:

    def Exception_Handler(resp):

        print("Exception. Status code: ", resp.status_code)

        if resp.status_code == 401:
            print("Need to refresh token.")
            Access.refresh('password', client_id, client_secret, Access.refresh_token)
            print("Token refreshed.")

        print(resp.json())

        ## other errors

################### END CLASS 'MISC' ###############




#### testing zone ####

Access.authenticate(username, password, client_id, client_secret, grant_type)
Devices.registerDevice()
#Login.credentials()
#Stores.selectStore(Access.access_token)
#Stores.getStores(Access.access_token)
#Devices.patchIP('raspberry', fixed_uuid, ip_address)
#Devices.createDevice('RaspberryPiTest', fixed_uuid, Stores.store_id)
#Devices.getDevice('raspberry', fixed_uuid)
