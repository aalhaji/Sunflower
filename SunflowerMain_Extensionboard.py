# control libraries
import RPi.GPIO as GPIO # initializing GPIO
import time

#IP library
import socket

#API library (don't uncomment until it's ready)

#import SunflowerAPI

# NOTE: THIS RELAY USES INVERSE LOGIC. GPIO.LOW TURNS IT ON, GPIO.HIGH TURNS IT OFF.

relaych1 = 26
relaych2 = 20
#relaych3 = 21 #if needed

GPIO.setmode(GPIO.BCM) # pinout configuration for model 3 B+
GPIO.setwarnings(False)

# PIN ASSIGNMENT FOR I/O

GPIO.setup(relaych1, GPIO.OUT, initial=GPIO.HIGH)

#GPIO.setup(relaych2, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(relaych2, GPIO.IN)
print("START STATE: ", GPIO.input(relaych2))


#def my_callback(channel):
#  print("rising edge detected on CHANNEL")

#GPIO.add_event_detect(relaych2, GPIO.RISING, callback=my_callback, bouncetime=500)

bedstatus = not GPIO.input(relaych2)

#GPIO.setup(25, GPIO.IN)
#GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

########################

from flask import Flask

app = Flask(__name__)

@app.route('/')

def home_page():

    if (bedstatus == 1):

        bed = 'on'

    else:

        bed = 'off'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]


    output = "Welcome to the Sun! The bed is currently "+bed+". "+"My IP address is "+ip+"."

    return output

@app.route('/bedon')

def bedon():
    
    global bedstatus

    while True:

        if (bedstatus == 1):

            GPIO.output(relaych1, GPIO.LOW)
            bedstatus = 1
            return 'The bed is already on.'
            app.logger.info("It's on.")

        else:

            GPIO.output(relaych1, GPIO.LOW)
            bedstatus = 1
            return 'The bed is now on.'

    
@app.route('/bedoff')

def bedoff():
    
    global bedstatus
    
    while True:

        if (bedstatus == 0):

            GPIO.output(relaych1, GPIO.HIGH)
            bedstatus = 0
            return 'The bed is already off.'

        else:

            GPIO.output(relaych1, GPIO.HIGH)
            bedstatus = 0
            return 'The bed is now off.'
						

if __name__ == "__main__":

    app.run(host='0.0.0.0')


