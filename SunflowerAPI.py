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

uuid = 'ac04be98-7ec1-11e8-9bda-b827eb98dcda' # was generated from str(uuid.uuid1())

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]


###### FUNCTIONS #######

############ ACCESS LIBRARY  ################

class Access:

############ FIRST TIME LOGIN ##############
    
    def authenticate(username, password, client_id, client_secret, grant_type):
        
        auth={"username":username,"password":password, "client_id":client_id, "client_secret":client_secret, "grant_type":grant_type}
        
        resp = requests.post(api_url_base+'oauth/token', data=auth)
                
        if resp.status_code != 201:
            print("Authorization error. Error code: ", resp.status_code)

            
        Access.access_token = resp.json()["access_token"]
        Access.refresh_token = resp.json()["refresh_token"]
        Access.bearer = 'Bearer '+str(Access.access_token)
 
        print(resp.json())
        
        print('Logged in. Access Token: {}'.format(Access.access_token))
    
############ REFRESH TOKEN ##################
        
    def refresh(grant_type, client_id, client_secret, refresh_token):
        
        refr={"grant_type":grant_type, "client_id":client_id, "client_secret":client_secret, "refresh_token":refresh_token}
        
        rresp = requests.post(api_url_base+'oauth/refresh', data=refr)
        
        if rresp.status_code != 200:
            print("Refresh token error. Error code: ", rresp.status_code)
            
        Access.access_token = rresp.json()["access_token"]
        Access.refresh_token = rresp.json()["refresh_token"]
        Access.bearer = 'Bearer '+str(Access.access_token)
        
        print(rresp.json())

        print('Token refreshed. Access Token: {}'.format(Access.access_token))

        return Access.access_token, Access.refresh_token

########### GET USER INFORMATION ################
        
    def getuserinfo(access_token):

        while True:

            userinf = {"Authorization":Access.bearer}
            userresp = requests.get(api_url_base+'me', json=userinf, headers=userinf)

            if userresp.status_code == 200:

                print(userresp.json())
                print('==================================')
                break
            
            else:

                misc.Exception_Handler(userresp.status_code)
                

################ GET STORES #######################

    def getStores(access_token):

        storebody = {"Authorization":Access.bearer}
        storeresp = requests.get(api_url_base+'stores', json=storebody, headers=storebody)

        print(storeresp.json())
        print('=========================')


############# END CLASS 'ACCESS' ##################


##################### DEVICES #####################

class Devices:
    
############## CREATE  DEVICE #####################
    
    def CreateDevice(name, uuid, store):
        
        device = {"name":name, "uuid":uuid, "store":store}
        
        devresp = requests.post(api_url_base+'devices', data=device, headers={"Authorization":Access.bearer, "Content-Type":'application/x-www-form-urlencoded'})
        
        if devresp.status_code != 200:
           # if devresp.status_code == 401:
             #   print("Need to refresh token.")
               # Access.refresh("password", client_id, client_secret, Access.refresh_token)
            #    print("Token refreshed. Please try again.")
          #  else:
            print("Create device error. Error code: ", devresp.status_code)
           
        print(devresp.json())

############# GET SPECIFIC DEVICE ################

    def GetDevice(name, uuid):
        
        device = {"name":name, "uuid":uuid}, 

        devresp = requests.get(api_url_base+'devices/'+uuid, data=device, headers={"Authorization":Access.bearer, "Content-Type":'application/x-www-form-urlencoded'})

        if devresp.status_code != 200:
            #if devresp.status_code == 401:
              #  print("Need to refresh token."
              #  Access.refresh("password", client_id, client_secret, Access.refresh_token)
             ##   print("Token refreshed. Please try again.")
         #   else:
            print("Get device error. Error code: ", devresp.status_code)
            

        print(devresp.json())

############# SEND IP ADDRESS #####################

		
    def PatchIP(name, uuid,  ip_address):
	
	    body = {"name":name, "uuid":uuid, "info.ip_address":ip_address}
		
	    patchresp = requests.patch(api_url_base+'devices/'+uuid, data=body, headers={"Authorization":Access.bearer})
		
	    if patchresp.status_code != 200:
               # if patchresp.status_code == 401:
                  #  print("Need to refresh token."
                  #  Access.refresh("password", client_id, client_secret, Access.refresh_token)
                   # print("Token refreshed. Please try again.")
               # else:
                 print("Patch device error. Error code: ", patchresp.status_code)
			
	    print(patchresp.json())

########### END CLASS 'DEVICES' ####################

########### MISCELLANEOUS FUNCTIONS ################

class misc:

    def Exception_Handler(resp):
        
        print("Error. Status code: ", status_code)
        
        if status_code == 401:
            print("Need to refresh token.")
            Access.refresh('password', client_id, client_secret, Access.refresh_token)
            print("Token refreshed.")

        ## other errors



################### END CLASS 'MISC' ###############



		
#### testing zone ####

Access.authenticate(username, password, client_id, client_secret, grant_type)
Access.getStores(Access.access_token)
#Devices.PatchIP('raspberry', uuid, ip_address)
#Devices.RegisterDev('raspberry', uuid, '57c0135b83c6e6030079f474')
#Devices.GetDevice('raspberry', uuid)
