import re
import datetime

# supporting apache/nginx/iis/http/NSCA_access_logs/ELB
elbRegex = '(?P<timestamp>[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9A-Z]+) (?P<elbName>[0-9a-zA-Z-]+) (?P<clientPort>[0-9.:]+) (?P<backendPort>[0-9.:]+) (?P<request_processing_time>[.0-9-]+) (?P<response_processing_time>[.0-9]+) (?P<elb_status_code>[.0-9-]+) (?P<backend_status_code>[0-9-]+) (?P<received_bytes>[0-9-]+) (?P<sent_bytes>[0-9-]+) (?P<request>[0-9-]+) "(?P<user_agent>[^"]+)" "(?P<ssl_cipher>[^"]+)" (?P<ssl_protocol>[- A-Z0-9a-z.]+)'
apacheRegex = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] (\S+) (.+?) (\S+) (\d{3}) (\S+)'
basicHTTPRegex = '(?P<method>[A-Z]+) (?P<path>[^ ]+) (?P<protocol>[A-Z0-9.\/]+)'
IISRegex = '(?P<clientIP>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}), (?P<userName>[^,]+), (?P<timestamp>[[0-9]{2}\/[0-9]{2}\/[0-9]{2}, [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}), (?P<serviceInstance>[^,]+), (?P<serverName>[^,]+), (?P<serverIP>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}), (?P<timeTaken>[^,]+), (?P<clientBytesSent>[^,]+), (?P<serverBytesSent>[^,]+), (?P<serviceStatusCode>[^,]+), (?P<windowsStatusCode>[^,]+), (?P<requestType>[^,]+), (?P<targetOfOperation>[^,]+), (?P<parameters>[^,]+),'


class LogParser:
    def __init__(self):
        self.data = []

    def parseLogs(self, line):
        if re.match(apacheRegex, line) is not None:
            values = self.parseApacheLogs(line)
            return values
        elif re.match(basicHTTPRegex, line) is not None:
            values = self.parseHTTPLogs(line)
            return values
        elif re.match(IISRegex, line) is not None:
            values = self.parseIISLogs(line)
            return values
        elif re.match(elbRegex, line) is not None:
            values = self.parseELBLogs(line)
            return values

    def parseELBLogs(self, line):
        values = re.findall(elbRegex, line)[0]
        ip_addr = values[2].split(':')[0]
        datetimeString = values[0].replace('T', ' ').replace('Z', '')
        datetimeObject = datetime.datetime.strptime(datetimeString, '%Y-%m-%d %H:%M:%S.%f')
        date = datetimeObject.strftime('%d/%b/%Y:%I:%M:%S%z') + '+0000'
        method = values[11].split(' ')[0]
        path = values[11].split(' ')[1]
        http_version = values[11].split(' ')[2]
        response_code = values[7]

        return (ip_addr, method, path, response_code, http_version, date)

    def parseIISLogs(self, line):
        values = re.findall(IISRegex, line)[0]
        ip_addr = values[0]
        datetimeString = values[2]
        datetimeObject = datetime.datetime.strptime(datetimeString, '%m/%d/%y, %H:%M:%S')
        date = datetimeObject.strftime('%d/%b/%Y:%I:%M:%S%z') + '+0000'
        method = values[11]
        path = values[12]
        http_version = values[1]
        response_code = values[9]

        return (ip_addr, method, path, response_code, http_version, date)

    def parseHTTPLogs(self, line):
        values = re.findall(basicHTTPRegex, line)[0]

        ip_addr = ''
        date = ''
        method = values[2]
        path = values[0]
        http_version = values[1]
        response_code = ''

        return (ip_addr, method, path, response_code, http_version, date)

    def parseApacheLogs(self, line):
        values = re.findall(apacheRegex, line)[0]

        ip_addr = values[0]
        date = values[3]
        method = values[4]
        path = values[5]
        http_version = values[6]
        response_code = values[7]

        return (ip_addr, method, path, response_code, http_version, date)