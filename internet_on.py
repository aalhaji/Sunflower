# this one-function module checks for an internet connection

from urllib.request import urlopen
import urllib.error

def internet_on():
    try:
        urlopen('http://www.google.com', timeout=1) # generic
        return True
    except urllib.error.URLError as err:
        return False
