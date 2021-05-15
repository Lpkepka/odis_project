import sqlite3
import csv
import queryBuilder

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
                configurationRows = row[1:]
            else:
                if row[0] == 'if':
                    query = queryBuilder.buildSqlQuery(row[1:], configurationRows)
                    numberOfResults = exectureSQLQuery(query)
                    ifCount += 1
                    ifCountForNextElse = ifCount
                    goingToElse = numberOfResults > query[1]
                elif row[0] == 'else':
                    if goingToElse and ifCount == ifCountForNextElse:
                        goingToElse = False
                        query = queryBuilder.buildSqlQuery(row[1:], configurationRows)
                        sqlSelectors.append(query)
                    else:
                        ifCount -= 1
                else:
                    if not goingToElse:
                        query = queryBuilder.buildSqlQuery(row[1:], configurationRows)
                        sqlSelectors.append(query)
            line_count += 1

def executeSQLQueries():
    for query in sqlSelectors:
        print(query[0])
        rowCount = exectureSQLQuery(query)
        if rowCount > query[1]:
            generateTXTRaport(query[0], query[1], rowCount)

def generateTXTRaport(query, expectedRows, foundRows):
    print('------------------- Raport ------------------')
    print('Found {} rows matching data from configuration'.format(foundRows))
    print('Expected less than {} rows'.format(expectedRows))
    print('Query {}'.format(query))
    print('------------------------------------- \n\n')

def exectureSQLQuery(query):
    c.execute(query[0])
    rows = c.fetchall()
    return int(rows[0][0])


while True:
    sqlSelectors.clear()
    importAnalyzerConfiguration()
    executeSQLQueries()
    time.sleep(10)