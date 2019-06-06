import globals
import threading
from states import transitions

def onTimer(TREATMENT_DURATION):
    globals.onTimer = threading.Timer(TREATMENT_DURATION, transitions.afterOn)
