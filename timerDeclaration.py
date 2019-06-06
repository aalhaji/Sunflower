import globals
import threading
from states import transitions

def onTimer(TREATMENT_DURATION):
    globals.on_timer = threading.Timer(TREATMENT_DURATION, transitions.afterOn)
