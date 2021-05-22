import unittest
import queryBuilder

queryBuilderObject = queryBuilder.QueryBuilder()

class MyTestCase(unittest.TestCase):
    configurationRows = ['ip_addr', 'server_url', 'method', 'path', 'response_code', 'http_version', 'date', 'granulation', 'isPositive', 'count']

    def test_base_2values_with_negative(self):
        configuration = ['1.2.3.4;1.3.4.5', '-', '-', '-', '-', '-', '-', '-', '0', '300']
        query = queryBuilderObject.buildSqlQuery(configuration, self.configurationRows)
        self.assertEqual(query[1], 300)
        self.assertEqual(query[0], "SELECT Count(*) FROM Logs WHERE NOT ip_addr='1.2.3.4' AND NOT ip_addr='1.3.4.5';")

    def test_base_2values_with_positive(self):
        configuration = ['1.2.3.4;1.3.4.5', '-', '-', '-', '-', '-', '-', '-', '1', '100']
        query = queryBuilderObject.buildSqlQuery(configuration, self.configurationRows)
        self.assertEqual(query[1], 100)
        self.assertEqual(query[0], "SELECT Count(*) FROM Logs WHERE ( ip_addr='1.2.3.4' OR ip_addr='1.3.4.5' );")

    def test_base_1value_with_positive(self):
        configuration = ['1.2.3.4', '-', '-', '-', '-', '-', '-', '-', '1', '50']
        query = queryBuilderObject.buildSqlQuery(configuration, self.configurationRows)
        self.assertEqual(query[1], 50)
        self.assertEqual(query[0], "SELECT Count(*) FROM Logs WHERE ip_addr='1.2.3.4';")

    def test_date_with_2values_minute(self):
        configuration = ['-', '-', '-', '-', '-', '-', '10/May/2013:10:35:32+0200;11/May/2013:10:35:32+0200', 'm', '1', '100']
        query = queryBuilderObject.buildSqlQuery(configuration, self.configurationRows)
        self.assertEqual(query[1], 100)
        self.assertEqual(query[0], "SELECT Count(*) FROM Logs WHERE ( date BETWEEN '10/May/2013:10:35:32+0200' AND '10/May/2013:10:36:32+0200' OR date BETWEEN '11/May/2013:10:35:32+0200' AND '11/May/2013:10:36:32+0200');")

    def test_date_with_1values_day(self):
        configuration = ['-', '-', '-', '-', '-', '-', '11/May/2013:10:35:32+0200', 'd', '1', '100']
        query = queryBuilderObject.buildSqlQuery(configuration, self.configurationRows)
        self.assertEqual(query[1], 100)
        self.assertEqual(query[0], "SELECT Count(*) FROM Logs WHERE date BETWEEN '11/May/2013:10:35:32+0200' AND '12/May/2013:10:35:32+0200';")

    def test_date_with_day_and_path_and_code(self):
        configuration = ['-', '-', '-', '/', '402', '-', '11/May/2013:10:35:32+0200', 'd', '1', '100']
        query = queryBuilderObject.buildSqlQuery(configuration, self.configurationRows)
        self.assertEqual(query[1], 100)
        self.assertEqual(query[0], "SELECT Count(*) FROM Logs WHERE path='/' AND response_code='402' AND date BETWEEN '11/May/2013:10:35:32+0200' AND '12/May/2013:10:35:32+0200';")

    def test_date_with_day_and_2path_and_3code_positive(self):
        configuration = ['-', '-', '-', '/;/image.jpg', '402;403;404', '-', '-', '-', '1', '100']
        query = queryBuilderObject.buildSqlQuery(configuration, self.configurationRows)
        self.assertEqual(query[1], 100)
        self.assertEqual(query[0], "SELECT Count(*) FROM Logs WHERE ( path='/' OR path='/image.jpg' ) AND ( response_code='402' OR response_code='403' OR response_code='404' );")

    def test_date_with_day_and_2path_and_3code_negative(self):
        configuration = ['-', '-', '-', '/;/image.jpg', '402;403;404', '-', '-', '-', '0', '100']
        query = queryBuilderObject.buildSqlQuery(configuration, self.configurationRows)
        self.assertEqual(query[1], 100)
        self.assertEqual(query[0], "SELECT Count(*) FROM Logs WHERE NOT path='/' AND NOT path='/image.jpg' AND NOT response_code='402' AND NOT response_code='403' AND NOT response_code='404';")

if __name__ == '__main__':
    unittest.main()
