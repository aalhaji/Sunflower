
# I/O libraries
import automationhat as shield
import time
time.sleep(0.1)
import threading # library for timers

TREATMENT_DURATION = 10 # 15*60 TO GET 15 MINUTES
COOLDOWN_DURATION = 10 # + 60*3 to get 3 mins



# IP library
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]

# API library
import SunflowerAPI as sF

# states library
from states import states
from states import transitions

# PATCH IP ADDRESS

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

print("Establishing Database Connection...")
print("==================================")
sF.Access.authenticate(username, password, client_id, client_secret, grant_type)
sF.Devices.patchIP(devname, uuid, ip_address)

# END PATCH IP ADDRESS

# SHIELD INITIALIZATION
# Automation pHAT needs to run "setup" after the first command
# so it will raise a runtime error on
# the first command
# So this is to ignore the first runtime error

print("Initializing Automation pHAT")
shield.relay.one.off()
print("==================================")
states.updateLocalState(0)
states.updateServerState()

try:
    shield.relay.one.read()
except RuntimeError:
    shield.relay.one.off() # Ensure that relay is off


# END INITIALIZATION

# STATES

states_dict={0:"AVAILABLE(OFF)",
        1: "BED_ON",
        2: "COOLDOWN",
        3: "CLEANING"
        }

# START APP

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route('/')
def home():
    return("Welcome to Sunflower! Current relay status: {}".format(shield.relay.one.read()))

@app.route('/bedstatus')
def status():

    currentState = states.checkLocalState()
    str_state = states_dict[currentState]

    return "The current state is {}".format(str_state)

@app.route('/bedon')
def bedon():

    currentState = states.checkLocalState()
    str_state = states_dict[currentState]

    if currentState == (1 or 2 or 3):
        return "ERROR. The bed is currently in state: {}".format(str_state)

    else:
        shield.relay.one.on()
        currentState = 1 # states[1]
        str_state = states_dict[currentState]
        states.updateLocalState(currentState)
        states.updateServerState()

        #state ON for 15 minutes

        global on_timer
        on_timer = threading.Timer(TREATMENT_DURATION, transitions.afterOn)
        on_timer.start()
        #if (states.checkLocalState() != 1):
        #    on_timer.cancel()

    return "Bed turned ON."


@app.route('/bedoff')
def bedoff():

    on_timer.cancel()

    currentState = states.checkLocalState()
    str_state = states_dict[currentState]


    if currentState == 0: # already off
        return "The bed is already in state: {}".format(str_state)

    elif  currentState == 1: # on

        transitions.afterOn()
        currentState = states.checkLocalState()
        str_state = states_dict[currentState]

        return "The bed has been turned off. Bed is now in state: {}".format(str_state)

    elif currentState == 2: # cooldown

        transitions.afterCool()
        currentState = states.checkLocalState()
        str_state = states_dict[currentState]

        return "Cooldown was interrupted. Bed is now in state: {}".format(str_state)

    elif currentState == 3: # Cleaning

        currentState = 0
        str_state = states_dict[currentState]
        states.updateLocalState(currentState)
        states.updateServerState()

        return "Cleaning done. Bed is now in state: {}".format(str_state)

    else:
        return "Bed off."

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

    @app.route("/onduration", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)

        print(form.errors)
        if request.method == 'POST':
            name=request.form['name']
            print(name)

        if form.validate():
            # Save the comment here.
            flash('Hello ' + name)
        else:
            flash('All the form fields are required. ')

        return render_template('on_duration.html', form=form)



if __name__ == "__main__":

    app.run(host='0.0.0.0')


    # OUTPUT
    # For relay, use NO side
    # Connect 5V power supply to NO
    # Connect COM to LOAD (BED)
    # GROUND THE LOAD ON THE OTHER SIDE
