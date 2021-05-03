import sqlite3
import csv
from datetime import datetime, timedelta
import time

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
    return (finalQueryString, count)

def importAnalyzerConfiguration():
    with open('analyzeConfiguration.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        configurationRows = []
        ifCount = 0
        goingToElse = False
        for row in csv_reader:
            if line_count == 0:
                configurationRows = row[1:]
            else:
                if row[0] == 'if':
                    query = buildSqlQuery(row[1:], configurationRows)
                    numberOfResults = exectureSQLQuery(query[0])
                    ifCount += 1
                    goingToElse = numberOfResults > query[1]
                elif row[0] == 'else':
                    if goingToElse and ifCount == 1:
                        goingToElse = False
                        query = buildSqlQuery(row[1:], configurationRows)
                        sqlSelectors.append(query)
                    else:
                        ifCount -= 1
                else:
                    if not goingToElse:
                        query = buildSqlQuery(row[1:], configurationRows)
                        sqlSelectors.append(query)
            line_count += 1

def exectureSQLQuery(query):
    c.execute(query[0])
    rows = c.fetchall()
    return int(rows[0][0])

def executeSQLQueries():
    for query in sqlSelectors:
        rowCount = exectureSQLQuery(query[0])
        print('------------------- Raport ------------------')
        print('Found {} rows matching data from configuration'.format(rowCount))
        print('Expected less than {} rows'.format(query[1]))
        print('------------------------------------- \n\n')


importAnalyzerConfiguration()

while True:
    executeSQLQueries()
    time.sleep(10)