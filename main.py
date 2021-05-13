import sqlite3
import requests
import sched, time
import re

#supporting apache/ngins/iis/http/NSCA_access_logs/ELB
elbRegex = '(?P<timestamp>[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9A-Z]+) (?P<elbName>[0-9a-zA-Z-]+) (?P<clientPort>[0-9.:]+) (?P<backendPort>[0-9.:]+) (?P<request_processing_time>[.0-9-]+) (?P<response_processing_time>[.0-9]+) (?P<elb_status_code>[.0-9-]+) (?P<backend_status_code>[0-9-]+) (?P<received_bytes>[0-9-]+) (?P<sent_bytes>[0-9-]+) (?P<request>[0-9-]+) "(?P<user_agent>[^"]+)" "(?P<ssl_cipher>[^"]+)" (?P<ssl_protocol>[- A-Z0-9a-z.]+)'
apacheRegex = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] (\S+) (.+?) (\S+) (\d{3}) (\S+)'
basicHTTPRegex = '(?P<method>[A-Z]+) (?P<path>[^ ]+) (?P<protocol>[A-Z0-9.\/]+)'
IISRegex = '(?P<clientIP>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}), (?P<userName>[^,]+), (?P<timestamp>[[0-9]{2}\/[0-9]{2}\/[0-9]{2}, [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}), (?P<serviceInstance>[^,]+), (?P<serverName>[^,]+), (?P<serverIP>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}), (?P<timeTaken>[^,]+), (?P<clientBytesSent>[^,]+), (?P<serverBytesSent>[^,]+), (?P<serviceStatusCode>[^,]+), (?P<windowsStatusCode>[^,]+), (?P<requestType>[^,]+), (?P<targetOfOperation>[^,]+), (?P<parameters>[^,]+),'

globalConfiguration = {}
conn = sqlite3.connect('Logs.db')
c = conn.cursor()
s = sched.scheduler(time.time, time.sleep)

def parseLogs(line):
    line2 = '192.168.114.201, -, 03/20/05, 7:55:20, W3SVC2, SERVER, 172.21.13.45, 4502, 163, 3223, 200, 0, GET, /DeptLogo.gif, -,'
    if re.match(apacheRegex, line2) is not None:
        values = parseApacheLogs(line2)
        return values
    elif re.match(basicHTTPRegex, line2) is not None:
        values = parseHTTPLogs(line2)
        return values
    elif re.match(IISRegex, line2) is not None:
        values = parseIISLogs(line2)
        return values
    elif re.match(elbRegex, line2) is not None:
        values = parseELBLogs(line2)
        return values

def parseELBLogs(line):
    values = re.findall(elbRegex, line)[0]
    # add proper date time
    ip_addr = values[0].split(':')[0]
    #'2015-05-13T23:39:43.945958Z'
    date = values[0]
    method = values[11].split(' ')[0]
    path = values[11].split(' ')[1]
    http_version = values[11].split(' ')[2]
    response_code = values[7]

    return (ip_addr, method, path, response_code, http_version, date)

def parseIISLogs(line):
    values = re.findall(IISRegex, line)[0]
    #add proper date time
    ip_addr = values[0]
    #'03/20/05, 7:55:20'
    date = values[2]
    method = values[11]
    path = values[12]
    http_version = values[1]
    response_code = values[9]

    return (ip_addr, method, path, response_code, http_version, date)

def parseHTTPLogs(line):
    values = re.findall(basicHTTPRegex, line)[0]

    ip_addr = ''
    date = ''
    method = values[2]
    path = values[0]
    http_version = values[1]
    response_code = ''

    return (ip_addr, method, path, response_code, http_version, date)

def parseApacheLogs(line):
    values = re.findall(apacheRegex, line)[0]

    ip_addr = values[0]
    date = values[3]
    method = values[4]
    path = values[5]
    http_version = values[6]
    response_code = values[7]

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
        values = parseLogs(line)
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
