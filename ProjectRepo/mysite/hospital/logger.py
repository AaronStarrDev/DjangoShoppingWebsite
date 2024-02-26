import csv

##########################################
#   LOG WRITE
##########################################
# myList = list that has the timestamp, user, messagetype, and the message
# logFile = the CSV file that contains the logs, it is opened in append-only mode
# wr = is an ACTIVE instance of the logfile, allowing for modifications through the writer function
def write(time, user, messageType, message):
    myList = [time, user, messageType, message]
    logFile = open('log.csv', 'a', newline='')
    wr = csv.writer(logFile, quoting=csv.QUOTE_ALL)
    wr.writerow(myList)
    logFile.close()

##########################################
#   LOG READ
##########################################
# rowList = list of each log, since log input is entered as rows.
def read():
    rowList = []
    with open('log.csv', 'r') as f: # opens log.csv and declares it as a local variable named f
        reader = csv.reader(f) # reader, reads the file using the csv helper function (.reader(FILE))
        for row in reader:
            rowList.append(row) # add each log to the rowList
    return rowList
