import sqlite3
import csv
import queryBuilder
import datetime
import time
import sys

conn = sqlite3.connect('Logs.db')
c = conn.cursor()
sqlSelectors = []
queryBuilder = queryBuilder.QueryBuilder()

def importAnalyzerConfiguration():
    with open('analyzeConfiguration.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        configurationRows = []
        ifCount = 0
        ifCountForNextElse = 0
        goingToElse = False
        for row in csv_reader:
            if line_count == 0:
                # The first row of the csv file contains the row names
                # The first column contains the if_else key, which is excluded
                # as it's part of the conditional parsing mechanism and not the data itself
                configurationRows = row[1:]
            else:
                if row[0] == 'if':
                    # If the row started with 'if' we execute the query and compare the results with the specified amount
                    query = queryBuilder.buildSqlQuery(row[1:], configurationRows)
                    numberOfResults = exectureSQLQuery(query)
                    # ifCount and ifCountForNextElse make sure to execute the correct 'else' if the condition is not met
                    ifCount += 1
                    ifCountForNextElse = ifCount
                    print('if query {} got {} results'.format(query[0], numberOfResults))
                    # if the 'if' query amount is not met, the loop proceeds to the proper 'else'
                    goingToElse = numberOfResults > query[1]
                elif row[0] == 'else':
                    # Check if the 'else' should be used by the means of our counter for the number of entered 'if'`s
                    if goingToElse and ifCount == ifCountForNextElse:
                        goingToElse = False
                        query = queryBuilder.buildSqlQuery(row[1:], configurationRows)
                        sqlSelectors.append(query)
                    else:
                        # We have not entered the proper 'else' and continue to the next one
                        ifCount -= 1
                else:
                    # standard/default lines are omitted while proceeding to the 'else'
                    if not goingToElse:
                        query = queryBuilder.buildSqlQuery(row[1:], configurationRows)
                        sqlSelectors.append(query)
            line_count += 1

def executeSQLQueries():
    # every sqlSelector is a touple with the query string and expected row amount
    for query in sqlSelectors:
        print(query[0])
        rowCount = exectureSQLQuery(query)
        if rowCount > query[1]:
            generateTXTRaport(query[0], query[1], rowCount)

def generateTXTRaport(query, expectedRows, foundRows):
    outF = open("generatedReports.txt", "a")
    today = datetime.datetime.now()
    outF.write('------------------- {} ------------------ \n'.format(today.strftime('%Y-%m-%d-%H:%M:%S')))
    outF.write('Found {} rows matching data from configuration\n'.format(foundRows))
    outF.write('Expected less than {} rows\n'.format(expectedRows))
    outF.write('Query {}\n'.format(query))
    outF.write('\n\n')

def exectureSQLQuery(query):
    c.execute(query[0])
    rows = c.fetchall()
    return int(rows[0][0])

def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    timeout = 30
    if (len(sys.argv) == 2):
        timeoutValue = sys.argv[1]
        # Check if the provided value is an integer value for timeout
        if representsInt(timeoutValue):
            timeout = int(timeoutValue)
    while True:
        # The analyzer is executed every 10 seconds by default and can be modified to the wanted amount
        sqlSelectors.clear()
        importAnalyzerConfiguration()
        executeSQLQueries()
        time.sleep(timeout)