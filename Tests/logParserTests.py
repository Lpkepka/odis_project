import unittest
import logParser

parser = logParser.LogParser()

class TestParser(unittest.TestCase):
    ELBLog = '2015-05-13T23:39:43.945958Z my-loadbalancer 192.168.131.39:2817 10.0.0.1:80 0.000086 0.001048 0.001337 200 200 0 57 "GET https://www.example.com:443/ HTTP/1.1" "curl/7.38.0" DHE-RSA-AES128-SHA TLSv1.2'
    IISLog = '192.168.114.201, -, 03/20/05, 7:55:20, W3SVC2, SERVER, 172.21.13.45, 4502, 163, 3223, 200, 0, GET, /DeptLogo.gif, -,'
    HTTPLog = 'GET /tutorials/other/top-20-mysql-best-practices/ HTTP/1.1'
    ApacheLog = '127.0.0.1 – frank [10/Oct/2000:13:55:36 -0700] “GET /apache_pb.gif HTTP/1.0” 200 2326'
    NginxLog = '127.0.0.1 - dbmanager [20/Nov/2017:18:52:17 +0000] "GET / HTTP/1.1" 401 188 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"'
    NCAS_access_log = '172.21.13.45 - Microsoft\JohnDoe [07/Apr/2004:17:39:04 -0800] "GET /scripts/iisadmin/ism.dll?http/serv HTTP/1.0" 200 3401'
    invalidLog = 'asdklsajdklajsd'

    def test_apache_log(self):
        values = parser.parseLogs(self.ApacheLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '127.0.0.1')
        self.assertEqual(values[2], '/apache_pb.gif')
        self.assertEqual(values[3], '200')

    def test_HTTPLog(self):
        values = parser.parseLogs(self.HTTPLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '')
        self.assertEqual(values[2], '/tutorials/other/top-20-mysql-best-practices/')
        self.assertEqual(values[3], '')

    def test_IISLog(self):
        values = parser.parseLogs(self.IISLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '192.168.114.201')
        self.assertEqual(values[2], '/DeptLogo.gif')
        self.assertEqual(values[3], '200')

    def test_ELBLog(self):
        values = parser.parseLogs(self.ELBLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '192.168.131.39')
        self.assertEqual(values[2], 'https://www.example.com:443/')
        self.assertEqual(values[3], '200')

    def test_NginxLog(self):
        values = parser.parseLogs(self.NginxLog)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '127.0.0.1')
        self.assertEqual(values[2], '/')
        self.assertEqual(values[3], '401')

    def test_NCAS_access_Log(self):
        values = parser.parseLogs(self.NCAS_access_log)
        self.assertEqual(len(values), 6)
        self.assertEqual(values[0], '172.21.13.45')
        self.assertEqual(values[2], '/scripts/iisadmin/ism.dll?http/serv')
        self.assertEqual(values[3], '200')

    def test_invalid_logs(self):
        values = parser.parseLogs(self.invalidLog)
        self.assertIsNone(values)

if __name__ == '__main__':
    unittest.main()
