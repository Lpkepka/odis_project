import sqlite3
import requests
import sched, time

globalConfiguration = {}
conn = sqlite3.connect('Logs.db')
c = conn.cursor()
s = sched.scheduler(time.time, time.sleep)

def parseApacheLogs(line):
    splitLine = line.strip().replace('- - ', '').replace(' +', '+').split(' ')
    ip_addr = splitLine[0]
    date = splitLine[1].replace('[', '').replace(']', '')
    method = splitLine[2]
    path = splitLine[3]
    http_version = splitLine[4]
    response_code = splitLine[5]

    return (ip_addr, method, path, response_code, http_version, date)

def importConfiguration():
    configurationFile = open('configuration.txt', 'r')
    while True:
        line = configurationFile.readline()
        if not line:
            break
        splitLine = line.split(" ")
        globalConfiguration[splitLine[0]] = int(splitLine[1])

    configurationFile.close()

def insertDataToDB(dataDictionary, serverURL):
    dataArray = dataDictionary.split(',')
    for line in dataArray:
        values = parseApacheLogs(line)
        sql = 'INSERT INTO Logs(ip_addr,server_url,method,path,response_code,http_version,date) VALUES(?, ?, ?, ?, ?, ?, ?);'
        c.execute(sql, [values[0], serverURL, values[1], values[2], values[3], values[4], values[5]])
    conn.commit()


def scheduleNewDataFetch(sc, url, interval):
    response = requests.get(url)
    insertDataToDB(response.json()["Logs"], url)
    print('Sending to:', url)
    s.enter(interval, 1, scheduleNewDataFetch, (sc, url, interval))

def launchAPICalls():
    for key in globalConfiguration:
        s.enter(1, 1, scheduleNewDataFetch, (s, key, globalConfiguration[key]))

    s.run()

if __name__ == '__main__':
    importConfiguration()
    c.execute('''CREATE TABLE IF NOT EXISTS Logs(
                ip_addr text,
                server_url text,
                method text,
                path text,
                response_code text,
                http_version text,
                date date)''')
    launchAPICalls()
