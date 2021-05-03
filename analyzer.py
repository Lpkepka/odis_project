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
    for i, conditions in enumerate(cutOffArray):
        if conditions != '-':
            equal = '' if isPositive else 'NOT '
            orOrAnd = 'OR ' if isPositive else 'AND '
            conditionsSplit = conditions.split(';')
            if len(conditionsSplit) > 1 and isPositive:
                conditionalQuery += ' ('
            for condition in conditionsSplit:
                conditionString = " {}{}='{}' {}".format(equal, configurationRows[i], condition, orOrAnd)
                conditionalQuery += conditionString
            if len(conditionsSplit) > 1 and isPositive:
                conditionalQuery += ')'
        if conditionalQuery[-4:] == 'OR )':
            conditionalQuery = ') AND '.join(conditionalQuery.rsplit('OR )', 1))
        elif conditionalQuery[-3:] == 'OR ':
            conditionalQuery = ' AND '.join(conditionalQuery.rsplit('OR ', 1))

    if ((dataArray[0] != '-') and (dataArray[1] != '-')):
        splitDates = dataArray[0].split(';')
        if len(splitDates) > 1:
            conditionalQuery += '('
        for date in splitDates:
            datetime_object = datetime.strptime(date, '%d/%b/%Y:%I:%M:%S%z')
            time_change = getTimeDeltaFor(dataArray[1])
            new_time = datetime_object + time_change
            new_time_string = new_time.strftime('%d/%b/%Y:%I:%M:%S%z')
            conditionalQuery += " date BETWEEN '{}' AND '{}' OR".format(date, new_time_string)
    else:
        conditionalQuery = conditionalQuery[:-4]

    conditionalQuery = conditionalQuery[:-3]
    if len(splitDates) > 1:
        conditionalQuery += ')'

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
                    numberOfResults = exectureSQLQuery(query)
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
    print(query[0])
    c.execute(query[0])
    rows = c.fetchall()
    return int(rows[0][0])

def executeSQLQueries():
    for query in sqlSelectors:
        rowCount = exectureSQLQuery(query)
        if rowCount > query[1]:
            print('------------------- Raport ------------------')
            print('Found {} rows matching data from configuration'.format(rowCount))
            print('Expected less than {} rows'.format(query[1]))
            print('------------------------------------- \n\n')

while True:
    sqlSelectors.clear()
    importAnalyzerConfiguration()
    executeSQLQueries()
    time.sleep(10)