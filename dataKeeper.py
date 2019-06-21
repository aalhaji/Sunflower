# This file is used to keep track of use Data
# It stores the content in a useData.csv
# The contents are then used as reference for lamp lifetime


import csv
from time import gmtime, strftime, time

# define dictionary's columns for csv
useData_columns = ['DATE', 'START_TIME', 'END_TIME', 'MINUTES_SPENT']

# configure parameters
dateToday = strftime("%d %b %Y", gmtime())

startTimeSec = time()
startTime = strftime("%H:%M:%S", gmtime())

endTimeSec = time()
endTime = strftime("%H:%M:%S", gmtime())

timeSpent = (endTimeSec - startTimeSec) / 60 # in minutes

useData_dict = [
                { 'DATE': dateToday,
                'START_TIME': startTime,
                'END_TIME': endTime,
                'MINUTES_SPENT': timeSpent }
                ]

useFile = "txt/useData.csv"

try:
    with open(useFile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=useData_columns)
        writer.writeheader()
        for data in useData_dict:
            writer.writerow(data)
except IOError:
    print("I/O Error")

from collections import OrderedDict

#tartTime = 'NEW START TIME'
#current_file = open("txt/useData.csv", "r")
#reader = csv.DictReader(current_file)

#readlist = list(reader)
#print(type(readlist))
#print(readlist[0])

#readdict = dict(readlist[0])
#print(readdict)

#writeList = open("txt/useData.csv", "w")
#writer = csv.writer(writeList)
#writer.writerows()
