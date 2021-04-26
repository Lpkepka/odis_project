import sqlite3
import threading
import requests

conn = sqlite3.connect('Logs.db')
c = conn.cursor()

def importConfiguration():
    configurationFile = open('logs.txt', 'r')
    while True:
        line = configurationFile.readline()
        if not line:
            break
        splitLine = line.split(" ")
        globalConfiguration[splitLine[0]] = splitLine[1]

    configurationFile.close()

def insertDataToDB(dataDictionary, serverURL):
    for line in dataDictionary:
        splitLine = line.strip().replace('- - ', '').split(' ')
        ip_addr = splitLine[0]
        date = splitLine[1].replace('[', '').replace(']', '')
        method = splitLine[2]
        path = splitLine[3]
        http_version = splitLine[4]
        response_code = splitLine[5]

        sql = 'INSERT INTO Logs(ip_addr,server_url,method,path,response_code,http_version,date) VALUES(?, ?, ?, ?, ?, ?, ?);'
        c.execute(sql, [ip_addr, serverURL, method, path, response_code, http_version, date])
    conn.commit()


def fetchNewData(interval, url):
    threading.Timer(interval, fetchNewData).start()
    response = requests.get(url)
    insertDataToDB(response.json()["Logs"], url)

def launchAPICalls():
    for url, timeoutValue in globalConfiguration.items():
        fetchNewData(timeoutValue, url)


globalConfiguration = {}
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
