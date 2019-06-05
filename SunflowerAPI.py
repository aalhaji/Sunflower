# This is a collection of functions to connect Sunflower's Raspberry Pi
# to the Countr API.
# Simply add "import SunflowerAPI" to a program in the same directory
# to start using these functions.
# You might need to refer to the library and class first
# e.g.  "SunflowerAPI.Access.authorize()" rather than "authorize()"

import requests
import json
import uuid
import socket
import getpass

# for testing
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

    # Credential collection
    def credentials():

        Login.username = input("Please enter your username (usually an e-mail): ")

        cred_file = open("/home/pi/sunflower/credentials.txt", "w")
        cred_file.write(Login.username)
        cred_file.write("\n")

        Login.password = getpass.getpass(prompt='Please enter your password:', stream=None)  #input("Please enter your password: ")
        cred_file.write(Login.password)
        cred_file.write("\n")

        Login.client_id = 'client-86a11a2564fb9b007b9901a21c10578753196d96'
        Login.client_secret = 'secret-7d6b06470b6b3d37367e3c5968fb91138d61509c'
        Login.grant_type = 'password'

        cred_file.close()


    # Choice of staging or production API
    def selectAPI():

        API_DICT = {'staging': {'name':'Staging API', 'url_base':'https://api-test.countr.rest/v2/'},
                'production': {'name':'Production API', 'url_base':'https://api.countr.rest/v2/'}
                }

        print("List of available API's:")

        # this is hardcoded because Python dictionaries are unordered, and this isn't a function
        # that will change over time (i.e. list of API's is likely going to stay the same)
        # a for-loop implementation of the following list is doable with an ordered dictionary from
        # the library "odict" if desired

        print("1 ) {}".format(API_DICT['staging']['name']))
        print("2 ) {}".format(API_DICT['production']['name']))

        while True:
            api_index = int(input("Please enter the number of the API you'd like to connect to: "))

            if api_index == 2:
                selected_api = 'production'
            else:
                selected_api = 'staging'

            is_confirmed = input("You selected '{}', confirm [y/n]? ".format(API_DICT[selected_api]['name']))

            if (is_confirmed == ('y' or 'Y' or 'yes' or 'Yes')):
                print("'{}' selected.".format(API_DICT[selected_api]['name']))
                print("==================================")
                break
            else:
                print('API not selected. Starting over...')

        Login.API_URL_BASE = API_DICT[selected_api]['url_base']

        api_file = open("api_url.txt", "w")
        api_file.write(Login.API_URL_BASE)
        api_file.close()

################### ACCESS  ################

class Access:

    ############ FIRST TIME LOGIN ##############

    def authenticate(username, password, client_id, client_secret, grant_type):

        api_file = open("/home/pi/sunflower/api_url.txt", "r").read().splitlines()
        api_url_base = api_file[0]

        body ={"username":username,"password":password, "client_id":client_id, "client_secret":client_secret, "grant_type":grant_type}
        resp = requests.post(api_url_base+'oauth/token', data=body)

        if resp.status_code != 201:
            print("Authorization error. Error code: ", resp.status_code)

        Access.access_token = resp.json()["access_token"]
        Access.refresh_token = resp.json()["refresh_token"]
        Access.bearer = 'Bearer '+str(Access.access_token)

        token_file = open("/home/pi/sunflower/access_token.txt", "w")
        token_file.write(Access.bearer)
        token_file.close()

        print('Logged in. Access Token: {}'.format(Access.access_token))
        print('==================================')

############ REFRESH TOKEN ##################

    def refresh(grant_type, client_id, client_secret, refresh_token):

        api_file = open("/home/pi/sunflower/api_url.txt", "r").read().splitlines()
        api_url_base = api_file[0]

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
            resp = requests.get(Login.API_URL_BASE+'me', json=body, headers=body)

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
            resp = requests.get(Login.API_URL_BASE+'stores/simple', json=body, headers=body)


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

        print("List of stores registered to this user: ")
        for i in range(len(Stores.storedata)):
            print("{}) {}".format(i+1, Stores.storedata[i]['name']))

        # Then get user input
        while True:
            selected_store = int(input("Please select the store number you'd like this device registered to: ")) - 1

            is_confirmed = input("You selected store '{}', Confirm [y/n]? ".format(Stores.storedata[selected_store]['name']))

            if (is_confirmed == ('y' or 'Y')):
                print("Store '{}' confirmed.".format(Stores.storedata[selected_store]['name']))
                Stores.store_id = str(Stores.storedata[selected_store]['_id'])
                print("==================================")
                break

            else:
                print("Store not selected. Starting over...")

##################### DEVICES #####################

class Devices:

    ############## CREATE  DEVICE #####################

    def createDevice(name, uuid, store):

        while True:
            body = {"name":name, "uuid":uuid, "store":store}
            resp = requests.post(Login.API_URL_BASE+'devices', data=body, headers={"Authorization":Access.bearer, "Content-Type":'application/x-www-form-urlencoded'})

            if resp.status_code == 200 or 201:
                print("Device has been created.")
                print('==================================')
                break

            else:
                misc.Exception_Handler(resp)
                break

    ########### ONE-TIME UUID GENERATION ################

    def generateUUID():

            Devices.uuid = str(uuid.uuid1())

            uuid_file = open("/home/pi/sunflower/uuid.txt", "w")
            uuid_file.write(Devices.uuid)
            uuid_file.write("\n")
            uuid_file.close()

############# GET SPECIFIC DEVICE ################

    def getDevice(name, uuid):

        while True:
            body = {"name":name, "uuid":uuid},
            resp = requests.get(Login.API_URL_BASE+'devices/'+uuid, data=body, headers={"Authorization":Access.bearer, "Content-Type":'application/x-www-form-urlencoded'})

            if resp.status_code == 200:
                print(resp.json())
                print('==================================')
                break

            else:
                misc.Exception_Handler(resp)
                break

############# SEND IP ADDRESS #####################


    def patchIP(name, uuid,  ip_address):

        api_file = open("/home/pi/sunflower/api_url.txt", "r").read().splitlines()
        api_url_base = api_file[0]

        token_file = open("/home/pi/sunflower/access_token.txt", "r").read().splitlines()
        auth = token_file[0]

        while True:
            body = {"name":name, "uuid":uuid, "info.ip_address":ip_address}
            resp = requests.patch(api_url_base+'devices/'+uuid, data=body, headers={"Authorization":auth})

            if resp.status_code == 200:
                print("IP has been sent.")
                print('==================================')
                break

            else:
                misc.Exception_Handler(resp)
                break

############# SEND CURRENT STATE #####################


    def patchState(name, uuid, ip_address):

        api_file = open("/home/pi/sunflower/api_url.txt", "r").read().splitlines()
        api_url_base = api_file[0]

        token_file = open("/home/pi/sunflower/access_token.txt", "r").read().splitlines()
        auth = token_file[0]

        currentStateFile = open("/home/pi/sunflower/currentState.txt", "r").read().splitlines()
        currentState = int(currentStateFile[0])

        while True:
            body = {"name":name, "uuid":uuid, "info.ip_address":ip_address, "info.last_state":currentState}
            resp = requests.patch(api_url_base+'devices/'+uuid, data=body, headers={"Authorization":auth})

            if resp.status_code == 200:
                print("State change patched to Countr server.")
                print('==================================')
                break

            else:
                misc.Exception_Handler(resp)
                break


########## DEVICE REGISTRATION PROMPT #############

    def registerDevice():

        print("Starting Device Registration...")

        ### 1) NAME

        while True:
            Devices.DeviceName = input("1) Please enter your desired device name:")
            is_confirmed = input("You selected name '{}', Confirm [y/n]?".format(Devices.DeviceName))

            if (is_confirmed == ('y' or 'Y')):
                print("Name '{}' confirmed.".format(Devices.DeviceName))
                print("==================================")
                dev_open = open("devicename.txt", "w")
                dev_open.write(Devices.DeviceName)
                dev_open.write("\n")
                dev_open.close()
                break
            else:
                print("Starting over...")


        ### 2) STORE SELECTION

        print("2) Please select your store:")
        Stores.selectStore(Access.access_token)

        ### 3) CREATE DEVICE

        print("Generating UUID...")
        print("Creating Device...")
        Devices.createDevice(Devices.DeviceName, Devices.uuid, Stores.store_id)

        ### 4) PATCH IP ADDRESS

        print("Sending IP Address to Countr Database...")
        Devices.patchIP(Devices.DeviceName, Devices.uuid, ip_address)


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
