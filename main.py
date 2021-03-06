import sqlite3
import requests
import sched, time
import logParser

globalConfiguration = {}
conn = sqlite3.connect('Logs.db')
parser = logParser.LogParser()
c = conn.cursor()
s = sched.scheduler(time.time, time.sleep)

def importConfiguration():
    configurationFile = open('configuration.txt', 'r')
    while True:
        line = configurationFile.readline()
        if not line:
            break
        # Splits the line into the URL and timeout between calls in seconds
        splitLine = line.split(" ")
        globalConfiguration[splitLine[0]] = int(splitLine[1])

    configurationFile.close()

def insertDataToDB(dataDictionary, serverURL):
    # Logs are split in new lines with the ',' delimiter and parsed by the logParser module
    # SQL queries are inserted with the c.execute to prevent unwanted injections
    dataArray = dataDictionary
    for line in dataArray:
        values = parser.parseLogs(line)
        if values is not None :
            sql = 'INSERT INTO Logs(ip_addr,server_url,method,path,response_code,http_version,date) VALUES(?, ?, ?, ?, ?, ?, ?);'
            c.execute(sql, [values[0], serverURL, values[1], values[2], values[3], values[4], values[5]])
    conn.commit()


def scheduleNewDataFetch(sc, url, interval):
    response = requests.get(url)
    # Logs are extracted from the response and must be present in the form of an array
    # The value key must be specified as "Logs"
    insertDataToDB(response.json()["Logs"], url)
    print('Sending to:', url)
    s.enter(interval, 1, scheduleNewDataFetch, (sc, url, interval))

def launchAPICalls():
    # Schedules calls based while iterating over keys and inputing the timouts to the scheduler
    for key in globalConfiguration:
        s.enter(1, 1, scheduleNewDataFetch, (s, key, globalConfiguration[key]))

    s.run()

if __name__ == '__main__':
    importConfiguration()
    # If the DB is empty, creates the table upon starting the script
    c.execute('''CREATE TABLE IF NOT EXISTS Logs(
                ip_addr text,
                server_url text,
                method text,
                path text,
                response_code text,
                http_version text,
                date date)''')
    launchAPICalls()
