# this one-function module checks for an internet connection

from urllib.request import urlopen
import urllib.error

def internet_on():
    try:
        urlopen('http://1.1.1.1', timeout=1) # generic
        return True
    except urllib.error.urlerror as err:
        return False
