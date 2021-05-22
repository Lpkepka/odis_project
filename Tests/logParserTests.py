import unittest
import logParser

parser = logParser.LogParser()

class TestParser(unittest.TestCase):
    ELBLog = '2015-05-13T23:39:43.945958Z my-loadbalancer 192.168.131.39:2817 10.0.0.1:80 0.000086 0.001048 0.001337 200 200 0 57 "GET https://www.example.com:443/ HTTP/1.1" "curl/7.38.0" DHE-RSA-AES128-SHA TLSv1.2'
    IISLog = '192.168.114.201, -, 03/20/05, 7:55:20, W3SVC2, SERVER, 172.21.13.45, 4502, 163, 3223, 200, 0, GET, /DeptLogo.gif, -,'
    HTTPLog = '127.0.0.1 - "" - [01/Feb/2016:19:12:22 +0000] "GET /s3/SmokeS3/2d9482ead66d4e748ff06ea4a0bb98490000 HTTP/1.1" 200 3145728 "-" "aws-sdk-java/1.7.5 Linux/3.14.0-0.clevos.1-amd64 OpenJDK_64-Bit_Server_VM/25.45-b02/1.8.0_45-internal" 50'
    ApacheLog = '127.0.0.1 – frank [10/Oct/2000:13:55:36 -0700] “GET /apache_pb.gif HTTP/1.0” 200 2326'
    invalidLog = 'asdklsajdklajsd'

    def test_apache_logs(self):
        values = parser.parseLogs(self.ApacheLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '127.0.0.1')

    def test_invalid_logs(self):
        values = parser.parseLogs(self.invalidLog)
        self.assertEqual(values, None)

    def test_IISLog(self):
        values = parser.parseLogs(self.IISLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '192.168.114.201')

if __name__ == '__main__':
    unittest.main()
