import unittest
import requests
from os.path import isfile, isdir, join
import datetime as dt
import shutil
import sqlite3

import david_lib
import david_currency_check
import david_climate_check

#reload(david_lib)

server_ip_addr = david_lib.ip_addr
server_port = david_lib.port
dir_david = david_lib.dir_david
file_climate_hot_bedroom = david_lib.file_climate_hot_bedroom
file_sqlite_db = david_lib.file_sqlite_db
file_log_web_server = david_lib.file_log_web_server
file_log_climate_check = david_lib.file_log_climate_check

file_sqlite_db_path = join(dir_david, file_sqlite_db)

file_sqlite_db_backup = f'david_db_{dt.datetime.now().strftime("%Y%m%d")}.sqlite'


class TestFiles(unittest.TestCase):

    def test_check_file(self):
        self.assertEqual(isdir(dir_david), True)
        self.assertEqual(isfile(join(dir_david, file_climate_hot_bedroom)), True)
        self.assertEqual(isfile(file_sqlite_db_path), True)
        self.assertEqual(isfile(join(dir_david, file_log_web_server)), True)
        self.assertEqual(isfile(join(dir_david, file_log_climate_check)), True)


class TestWebServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        shutil.copy(join(dir_david, file_sqlite_db), join(dir_david, file_sqlite_db_backup))

    @classmethod
    def tearDownClass(cls):
        shutil.copy(join(dir_david, file_sqlite_db_backup), join(dir_david, file_sqlite_db))

    # david_web_server.py

    def test_get_connect(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/connected;sensor=1&ip=192.168.1.63'
        url_02 = f'http://{server_ip_addr}:{server_port}/connected;sensor=3&ip=192.168.1.64'
        urls = [url_01, url_02]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')

    def test_get_motion(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/motion;sensor=3'
        urls = [url_01]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')

    def test_get_not_found(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/any_text'
        urls = [url_01]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 404)

    def test_01_get_climate(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/climate;sensor=1&readattempt=10&temperature=24.0&humidity=35.0'
        url_02 = f'http://{server_ip_addr}:{server_port}/climate;sensor=1&readattempt=10&temperature=nan&humidity=35.0'
        url_03 = f'http://{server_ip_addr}:{server_port}/climate;sensor=1&readattempt=6&temperature=6.0&humidity=6.0'
        urls = [url_01, url_02, url_03]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')

    def test_02_fetch_climate_data(self):
        conn = sqlite3.connect(file_sqlite_db_path)
        cur = conn.cursor()
        sql_str = """SELECT SENSOR_ID, ATTEMPT, TEMPERATURE, HUMIDITY FROM CLIMATE_SENSORS
        WHERE REP_DATE >= DATETIME('now','-1 minute')
        AND ID = (SELECT MAX(ID) FROM CLIMATE_SENSORS);"""
        cur.execute(sql_str)
        result = None
        for results in cur:
            result = results
        conn.close()
        self.assertEqual(result, (1, 6, 6, 6))

    # david_climate_check.py

    def test_03_get_climate_data(self):
        result = david_climate_check.get_climate_data()
        if result:
            self.assertEqual(result, 6)
        else:
            self.assertIsNone(result)

    # david_currency_check.py

    def test_get_valute(self):
        char_code, usd_rate = david_currency_check.get_valute('USD')
        self.assertEqual(char_code, 'USD')
        self.assertTrue(usd_rate)

    def test_currency_rate_db_insert(self):
        david_currency_check.currency_rate_db_insert('USD', 666)
        conn = sqlite3.connect(file_sqlite_db_path)
        cur = conn.cursor()
        sql_str = """SELECT CURRENCY_NAME, CURRENCY_RATE FROM CURRENCY_RATES
                WHERE REP_DATE >= DATETIME('now','-1 minute')
                AND ID = (SELECT MAX(ID) FROM CURRENCY_RATES);"""
        cur.execute(sql_str)
        result = None
        for results in cur:
            result = results
        conn.close()
        self.assertEqual(result, ('USD', 666))

    def test_currency_check(self):
        currency_check_variants = ['currency_abnormal_increase', 'currency_normal', 'currency_abnormal_decrease']
        currency_check_result, _ = david_currency_check.currency_check()
        self.assertTrue(currency_check_result in currency_check_variants)

    def test_currency_change_inform_user(self):
        currency_check_result, currency_rate = david_currency_check.currency_check()
        result = david_currency_check.currency_change_inform_user(currency_check_result, currency_rate)
        self.assertEqual(result, 'OK')


if __name__ == '__main__':
    unittest.main()

# suite = unittest.TestLoader().loadTestsFromTestCase(TestFiles)
# runner = unittest.TextTestRunner(verbosity=2)
# runner.run(suite)

# suite = unittest.TestLoader().loadTestsFromTestCase(TestWebServer)
# runner = unittest.TextTestRunner(verbosity=2)
# runner.run(suite)