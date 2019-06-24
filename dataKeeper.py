# This file is used to keep track of use Data
# It stores the content in a useData.csv
# The contents are then used as reference for lamp lifetime


import csv
from time import localtime, strftime, time

class logdata:

    def makeUseFile():

        useData_columns = ['DATE', 'START_TIME', 'END_TIME', 'MINUTES_SPENT']

        # configure parameters
        dateToday = strftime("%d %b %Y", localtime())

        startTimeSec = time()
        startTime = strftime("%H:%M:%S", localtime())

        endTimeSec = time()
        endTime = strftime("%H:%M:%S", localtime())

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
    ############

    def resetUseFile():


            # truncate the useFile

            useFile = "txt/useData.csv"

            csvfile = open(useFile, "w+")
            csvfile.close()

            # Redefine the labels

            useData_columns = ['DATE', 'START_TIME', 'END_TIME', 'MINUTES_SPENT']

            try:
                with open(useFile, 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=useData_columns)
                    writer.writeheader()
            except IOError:
                print("I/O Error")


    def getTotalUseTime():

        useFile = "txt/useData.csv"
        useFile = open(useFile, "r")
        reader = csv.reader(useFile)

        # Record last use time, for errors

        lastDuration = round((float((useFile.readlines()[-1]).split(","))),2)
        print("LAST DURATION")
        print(lastDuration)

        next(reader) # Skipping Header Line
        totalUseTime = 0

        for row in reader:
            totalUseTime += float(row[3]) ## Only float because the test values are under 1 minute

        totalUseTime = round(totalUseTime, 2) ## 2 significant numbers only

        return totalUseTime
