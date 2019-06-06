# this one-function module checks for an internet connection

import urllib2

def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1) # Google
        return True
    except urllib2.URLError as err:
        return False
