import unittest
import logParser

parser = logParser.LogParser()

class TestParser(unittest.TestCase):
    ELBLog = '2015-05-13T23:39:43.945958Z my-loadbalancer 192.168.131.39:2817 10.0.0.1:80 0.000086 0.001048 0.001337 200 200 0 57 "GET https://www.example.com:443/ HTTP/1.1" "curl/7.38.0" DHE-RSA-AES128-SHA TLSv1.2'
    IISLog = '192.168.114.201, -, 03/20/05, 7:55:20, W3SVC2, SERVER, 172.21.13.45, 4502, 163, 3223, 200, 0, GET, /DeptLogo.gif, -,'
    HTTPLog = 'GET /tutorials/other/top-20-mysql-best-practices/ HTTP/1.1'
    ApacheLog = '127.0.0.1 – frank [10/Oct/2000:13:55:36 -0700] “GET /apache_pb.gif HTTP/1.0” 200 2326'
    invalidLog = 'asdklsajdklajsd'

    def test_apache_logs_ip(self):
        values = parser.parseLogs(self.ApacheLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '127.0.0.1')
        self.assertEqual(values[2], '/apache_pb.gif')
        self.assertEqual(values[3], '200')

    def test_HTTPLog_ip(self):
        values = parser.parseLogs(self.HTTPLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '')
        self.assertEqual(values[2], '/tutorials/other/top-20-mysql-best-practices/')
        self.assertEqual(values[3], '')

    def test_IISLog_ip(self):
        values = parser.parseLogs(self.IISLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '192.168.114.201')
        self.assertEqual(values[2], '/DeptLogo.gif')
        self.assertEqual(values[3], '200')

    def test_ELBLog_ip(self):
        values = parser.parseLogs(self.ELBLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '192.168.131.39')
        self.assertEqual(values[2], 'https://www.example.com:443/')
        self.assertEqual(values[3], '200')

    def test_invalid_logs(self):
        values = parser.parseLogs(self.invalidLog)
        self.assertEqual(values, None)

if __name__ == '__main__':
    unittest.main()
