import unittest
import requests
from os.path import isfile, isdir, join
import datetime as dt
import shutil

import david_lib
import david_currency_check

#reload(david_lib)

server_ip_addr = david_lib.ip_addr
server_port = david_lib.port
dir_david = david_lib.dir_david
file_climate_hot_bedroom = david_lib.file_climate_hot_bedroom
file_sqlite_db = david_lib.file_sqlite_db
file_log_web_server = david_lib.file_log_web_server
file_log_climate_check = david_lib.file_log_climate_check

file_sqlite_db_backup = f'david_db_{dt.datetime.now().strftime("%Y%m%d")}.sqlite'


class TestFiles(unittest.TestCase):

    def test_check_file(self):
        self.assertEqual(isdir(dir_david), True)
        self.assertEqual(isfile(join(dir_david, file_climate_hot_bedroom)), True)
        self.assertEqual(isfile(join(dir_david, file_sqlite_db)), True)
        self.assertEqual(isfile(join(dir_david, file_log_web_server)), True)
        self.assertEqual(isfile(join(dir_david, file_log_climate_check)), True)


class TestWebServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        shutil.copy(join(dir_david, file_sqlite_db), join(dir_david, file_sqlite_db_backup))

    @classmethod
    def tearDownClass(cls):
        shutil.copy(join(dir_david, file_sqlite_db_backup), join(dir_david, file_sqlite_db))

    def test_get_connect(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/connected;sensor=1&ip=192.168.1.63'
        url_02 = f'http://{server_ip_addr}:{server_port}/connected;sensor=3&ip=192.168.1.64'
        urls = [url_01, url_02]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'OK')

    def test_get_climate(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/climate;sensor=1&readattempt=10&temperature=24.0&humidity=35.0'
        url_02 = f'http://{server_ip_addr}:{server_port}/climate;sensor=1&readattempt=10&temperature=nan&humidity=35.0'
        url_03 = f'http://{server_ip_addr}:{server_port}/motion;sensor=3'
        urls = [url_01, url_02, url_03]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text, 'OK')


class TestDavidLib(unittest.TestCase):

    def test_get_valute(self):
        usd = david_currency_check.get_valute('USD')
        self.assertEqual(usd[0], 'USD')
        self.assertTrue(usd[1])


if __name__ == '__main__':
    unittest.main()

# suite = unittest.TestLoader().loadTestsFromTestCase(TestFiles)
# runner = unittest.TextTestRunner(verbosity=2)
# runner.run(suite)

# suite = unittest.TestLoader().loadTestsFromTestCase(TestWebServer)
# runner = unittest.TextTestRunner(verbosity=2)
# runner.run(suite)