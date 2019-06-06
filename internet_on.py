# this one-function module checks for an internet connection

rom urllib.request import urlopen

def internet_on():
    try:
        urllib2.urlopen('http://1.1.1.1', timeout=1) # generic
        return True
    except urllib2.URLError as err:
        return False
