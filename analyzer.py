import sqlite3
import csv
from datetime import datetime, timedelta

conn = sqlite3.connect('Logs.db')
c = conn.cursor()
sqlSelectors = []

def getTimeDeltaFor(text):
    if text == 's':
        return timedelta(seconds=1)
    elif text == 'm':
        return timedelta(minutes=1)
    elif text == 'h':
        return timedelta(hours=1)
    elif text == 'd':
        return timedelta(days=1)
    elif text == 'w':
        return timedelta(weeks=1)


def buildSqlQuery(configuration, configurationRows):
    baseQuery = 'SELECT Count(*) FROM Logs WHERE{}'
    conditionalQuery = ''
    cutOffArray = configuration[:-4]
    dataArray = configuration[-4:-2]
    isPositive = configuration[-2] == '1'
    count = int(configuration[-1])
    for i, condition in enumerate(cutOffArray):
        if condition != '-':
            equal = '' if isPositive else 'NOT '
            conditionString = " {}{}='{}' AND".format(equal, configurationRows[i], condition)
            conditionalQuery += conditionString

    if ((dataArray[0] != '-') and (dataArray[1] != '-')):
        datetime_object = datetime.strptime(dataArray[0], '%d/%b/%Y:%I:%M:%S%z')
        time_change = getTimeDeltaFor(dataArray[1])
        new_time = datetime_object + time_change
        new_time_string = new_time.strftime('%d/%b/%Y:%I:%M:%S%z')
        conditionalQuery += " date BETWEEN '{}' AND '{}'".format(dataArray[0], new_time_string)
    else:
        conditionalQuery = conditionalQuery[:-4]

    finalQueryString = baseQuery.format(conditionalQuery)
    finalQueryString += ';'
    sqlSelectors.append((finalQueryString, count))

def importAnalyzerConfiguration():
    with open('analyzeConfiguration.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        configurationRows = []
        for row in csv_reader:
            if line_count == 0:
                configurationRows = row
            else:
                buildSqlQuery(row, configurationRows)
            line_count += 1

def executeSQLQueries():
    for query in sqlSelectors:
        c.execute(query[0])
        rows = c.fetchall()
        print('------------------- Raport ------------------')
        print('Found {} rows matching data from configuration'.format(int(rows[0][0])))
        print('Expected less than {} rows'.format(query[1]))
        print('------------------------------------- \n\n')


importAnalyzerConfiguration()
executeSQLQueries()