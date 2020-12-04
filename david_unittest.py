import unittest
import requests
from os.path import isfile, isdir, join
import datetime as dt
import shutil
import sqlite3
from pandas import DataFrame
from sys import platform
import pytest

import david_lib
import david_currency_check
import david_climate_check
import david_gas_check
import david_healthcheck
import david_user_interface
import time

dont_test_list = ['play_file', 'mail', 'check_timer']  # 'play_file', 'mail', 'check_timer'
# dont_test_list = []  # 'play_file', 'mail', 'check_timer'

server_ip_addr = david_lib.ip_addr
server_port = david_lib.port
dir_david = david_lib.dir_david

file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)
file_sqlite_db_backup = f'david_db_{dt.datetime.now().strftime("%Y%m%d")}.sqlite'

currency_usd_threshold_high = david_lib.currency_usd_threshold_high
currency_usd_threshold_low = david_lib.currency_usd_threshold_low

mp3_files_dict = david_lib.mp3_files_dict
file_climate_hot_bedroom_path = join(dir_david, mp3_files_dict['climate_hot_bedroom'])
file_climate_cold_bedroom_path = join(dir_david, mp3_files_dict['climate_cold_bedroom'])
file_gas_danger_path = join(dir_david, mp3_files_dict['gas_danger'])
file_check_oven_path = join(dir_david, mp3_files_dict['check_oven'])

# file_climate_hot_bedroom = david_lib.file_climate_hot_bedroom
# file_climate_hot_bedroom_path = join(dir_david, file_climate_hot_bedroom)
# file_climate_cold_bedroom = david_lib.file_climate_cold_bedroom
# file_climate_cold_bedroom_path = join(dir_david, file_climate_cold_bedroom)
# file_gas_danger = david_lib.file_gas_danger
# file_gas_danger_path = join(dir_david, file_gas_danger)

file_log_climate_check = david_lib.file_log_climate_check
file_log_climate_check_path = join(dir_david, file_log_climate_check)
file_log_currency_check = david_lib.file_log_currency_check
file_log_currency_check_path = join(dir_david, file_log_currency_check)
file_log_healthcheck = david_lib.file_log_healthcheck
file_log_healthcheck_path = join(dir_david, file_log_healthcheck)
file_log_user_interface = david_lib.file_log_user_interface
file_log_user_interface_path = join(dir_david, file_log_user_interface)

file_log_web_server = david_lib.file_log_web_server
file_log_web_server_path = join(dir_david, file_log_web_server)

file_log_gas_check = david_lib.file_log_gas_check
file_log_gas_check_path = join(dir_david, file_log_gas_check)


# Check files

class TestFiles(unittest.TestCase):

    def test_check_file(self):
        self.assertEqual(isdir(dir_david), True)
        self.assertEqual(isfile(file_climate_hot_bedroom_path), True)
        self.assertEqual(isfile(file_climate_cold_bedroom_path), True)
        self.assertEqual(isfile(file_gas_danger_path), True)
        self.assertEqual(isfile(file_check_oven_path), True)
        self.assertEqual(isfile(file_sqlite_db_path), True)
        self.assertEqual(isfile(file_log_web_server_path), True)
        self.assertEqual(isfile(file_log_climate_check_path), True)
        self.assertEqual(isfile(file_log_currency_check_path), True)
        self.assertEqual(isfile(file_log_gas_check_path), True)
        self.assertEqual(isfile(file_log_healthcheck_path), True)
        self.assertEqual(isfile(file_log_user_interface_path), True)


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
        url_02 = f'http://{server_ip_addr}:{server_port}/connected;sensor=2&ip=192.168.1.64'
        url_03 = f'http://{server_ip_addr}:{server_port}/connected;sensor=3&ip=192.168.1.65'
        url_04 = f'http://{server_ip_addr}:{server_port}/connected;sensor=4&ip=192.168.1.66'
        url_05 = f'http://{server_ip_addr}:{server_port}/connected;sensor=1&ip=192.168.1.63&ver=190720'
        url_06 = f'http://{server_ip_addr}:{server_port}/connected;sensor=2&ip=192.168.1.64&ver=190720'
        url_07 = f'http://{server_ip_addr}:{server_port}/connected;sensor=3&ip=192.168.1.65&ver=190720'
        url_08 = f'http://{server_ip_addr}:{server_port}/connected;sensor=4&ip=192.168.1.66&ver=190720'
        urls = [url_01, url_02, url_03, url_04,url_05, url_06, url_07, url_08]
        for url in urls:
            r = requests.get(url, timeout=3)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')

    def test_01_get_gas(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/gas;sensor=2&sensorValue=666'
        url_02 = f'http://{server_ip_addr}:{server_port}/gas;sensor=2&sensorValue=666&type=0'
        urls = [url_01, url_02]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')

    @pytest.mark.skipif('mail' in dont_test_list, reason='mail')
    def test_01_get_gas_emergency(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/gas;sensor=2&sensorValue=666&type=1'
        urls = [url_01]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')

    @pytest.mark.skipif('check_timer' in dont_test_list, reason='check_timer')
    def test_01_get_gas_check_timer(self):
        url = f'http://{server_ip_addr}:{server_port}/gas;sensor=2&sensorValue=666&type=1'
        for _ in range(10):
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')
            time.sleep(1)

    def test_02_fetch_gas_data(self):
        conn = sqlite3.connect(file_sqlite_db_path)
        cur = conn.cursor()
        sql_str = """SELECT SENSOR_ID, SENSOR_VALUE FROM GAS_SENSORS
        WHERE REP_DATE >= DATETIME('now','-1 minute')
        AND ID = (SELECT MAX(ID) FROM GAS_SENSORS);"""
        cur.execute(sql_str)
        result = None
        for results in cur:
            result = results
        conn.close()
        self.assertEqual(result, (2, 666))

    @pytest.mark.skipif('mail' in dont_test_list, reason='mail')
    def test_get_motion(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/motion;sensor=3'
        urls = [url_01]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')

    @pytest.mark.skipif('mail' in dont_test_list, reason='mail')
    def test_get_oven(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/oven;sensor=7&temperature=66&type=1'
        urls = [url_01]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')

    @pytest.mark.skipif('check_timer' in dont_test_list, reason='check_timer')
    def test_get_oven_check_timer(self):
        url = f'http://{server_ip_addr}:{server_port}/oven;sensor=7&temperature=66&type=1'
        for _ in range(10):
            r = requests.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')
            time.sleep(1)

    def test_get_not_found(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/any_text'
        urls = [url_01]
        for url in urls:
            r = requests.get(url)
            self.assertEqual(r.status_code, 404)

    def test_01_get_climate(self):
        url_01 = f'http://{server_ip_addr}:{server_port}/climate;sensor=1&readattempt=10&temperature=21.0&humidity=31.0'
        url_02 = f'http://{server_ip_addr}:{server_port}/climate;sensor=1&readattempt=10&temperature=nan&humidity=31.0'
        url_03 = f'http://{server_ip_addr}:{server_port}/climate;sensor=1&readattempt=6&temperature=6.0&humidity=6.0'
        url_04 = f'http://{server_ip_addr}:{server_port}/climate;sensor=4&readattempt=10&temperature=22.0&humidity=32.0'
        url_05 = f'http://{server_ip_addr}:{server_port}/climate;sensor=4&readattempt=10&temperature=nan&humidity=32.0'
        url_06 = f'http://{server_ip_addr}:{server_port}/climate;sensor=4&readattempt=7&temperature=7.0&humidity=7.0'
        urls = [url_01, url_02, url_03, url_04, url_05, url_06]
        for url in urls:
            r = requests.get(url)
            time.sleep(0.5)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.text.strip(), '"OK"')

    def test_02_fetch_climate_data(self):
        conn = sqlite3.connect(file_sqlite_db_path)
        cur = conn.cursor()
        sql_str = """SELECT SENSOR_ID, ATTEMPT, TEMPERATURE, HUMIDITY FROM CLIMATE_SENSORS
        WHERE REP_DATE >= DATETIME('now','-1 minute')
        AND ID IN (SELECT MAX(ID) FROM CLIMATE_SENSORS GROUP BY SENSOR_ID);"""
        cur.execute(sql_str)
        results = cur.fetchall()
        conn.close()
        correct_results = [(1, 6, 6, 6), (4, 7, 7, 7)]
        for correct_result, result in zip(correct_results, results):
            self.assertTupleEqual(result, correct_result)

    # david_climate_check.py

    def test_02_get_climate_data(self):
        results = david_climate_check.get_climate_data()
        correct_results = [('bedroom', 6), ('childrenroom', 7)]
        for correct_result, result in zip(correct_results, results):
            self.assertTupleEqual(result, correct_result)

    # david_currency_check.py

    def test_currency_rate_increase(self):
        david_currency_check.currency_rate_db_insert('USD', str(currency_usd_threshold_high - 1))
        david_currency_check.currency_rate_db_insert('USD', str(currency_usd_threshold_high + 1))
        currency_check_result, _, _, _ = david_currency_check.currency_check()
        assert currency_check_result == 'currency_abnormal_increase'

    def test_currency_rate_decrease(self):
        david_currency_check.currency_rate_db_insert('USD', str(currency_usd_threshold_low + 1))
        david_currency_check.currency_rate_db_insert('USD', str(currency_usd_threshold_low - 1))
        currency_check_result, rate, _, _ = david_currency_check.currency_check()
        print(rate)
        assert currency_check_result == 'currency_abnormal_decrease'

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
        currency_check_result, _, _, _ = david_currency_check.currency_check()
        self.assertTrue(currency_check_result in currency_check_variants)

    def test_currency_change_inform_user(self):
        currency_check_result, currency_rate, _, _ = david_currency_check.currency_check()
        if 'currency' in currency_check_result: result = True
        self.assertEqual(result, True)

    # david_gas_check.py

    def test_02_get_gas_data(self):
        result = david_gas_check.get_gas_data()
        if result:
            self.assertEqual(result, 666)
        else:
            self.assertIsNone(result)

    # david_healthcheck.py

    def test_02_healthcheck_fetch_climate_data(self):
        result = david_healthcheck.fetch_climate_data()
        self.assertEqual(result, {'bedroom': 6, 'childrenroom': 7})

    def test_02_healthcheck_fetch_gas_data(self):
        result = david_healthcheck.fetch_gas_data()
        self.assertEqual(result, 666)

    def test_get_system_data(self):
        if platform == "win32":
            pass
        else:
            result = david_healthcheck.get_system_data()
            self.assertIsInstance(result, dict)
            self.assertIsInstance(result['percent'], float)
            self.assertIsInstance(result['cpu'], float)


class UserInterface(unittest.TestCase):

    # david_user_interface.py
    # InformUser.mail

    @pytest.mark.skipif('mail' in dont_test_list, reason='mail')
    def test_inform_user_mail(self):
        message = """\
        <html>
          <body>
            <div>
                <table class=MsoNormalTable border=0 cellspacing=5 cellpadding=0
                width="100%" style='width:100.0%;mso-cellspacing:1.5pt;mso-yfti-tbllook:
                1184'>
                <tr style='mso-yfti-irow:1;mso-yfti-lastrow:yes'>
                <td style='padding:10.5pt 0cm 0cm 0cm'>
                <p class=MsoNormal align=center style='text-align:center'><span
                style='font-size:15.0pt;font-family:ArialMT;mso-fareast-font-family:"Times New Roman";
                color:#0E909A'>This is test message<o:p></o:p></span></p>
                </td>
                </tr>
                </table>
            </div>
          </body>
        </html>
        """
        inform_user = david_user_interface.InformUser()
        result = inform_user.mail("Test message", message, ["balobin.p@mail.ru", "pavel@roamability.com"])
        self.assertEqual(result, True)

    # InformUser.play_file

    @pytest.mark.skipif('play_file' in dont_test_list, reason='play_file')
    def test_inform_user_play_file(self):
        if platform == "win32":
            pass
        else:
            inform_user = david_user_interface.InformUser()
            for mp3_file in mp3_files_dict:
                result = inform_user.play_file(mp3_file)
                self.assertEqual(result, True)
                time.sleep(1)


class TestCurrencyCheck(unittest.TestCase):

    def test_get_valuta_success(self):
        char_code, usd_rate = david_currency_check.get_valuta('USD')
        assert char_code == 'USD'
        assert usd_rate

    def test_get_valuta_error(self):
        char_code, usd_rate = david_currency_check.get_valuta('USD', url='http://')
        assert char_code == 'USD'
        assert usd_rate is None

    def test_01_parameters_ok(self):
        status, df = david_currency_check.get_iis_shares(market='foreign', tickers=david_currency_check.tickers_foreign)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (True,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE', 'LAST'],
                          sorted(david_currency_check.tickers_foreign),
                          ))

    def test_02_parameters_ok(self):
        status, df = david_currency_check.get_iis_shares(market='russian', tickers=david_currency_check.tickers_russian)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist(),
                          ),
                         (True,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE', 'LAST'],
                          sorted(david_currency_check.tickers_russian),
                          ))

    def test_03_parameters_nok_wrong_combination(self):
        status, df = david_currency_check.get_iis_shares(market='russian', tickers=david_currency_check.tickers_foreign)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist(),
                          ),
                         (True,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE', 'LAST'],
                          [],
                          ))

    def test_04_parameters_nok_wrong_combination(self):
        status, df = david_currency_check.get_iis_shares(market='foreign', tickers=david_currency_check.tickers_russian)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (True,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE', 'LAST'],
                          [],
                          ))

    def test_05_parameters_nok_wrong_values(self):
        status, df = david_currency_check.get_iis_shares(market='wrong', tickers=david_currency_check.tickers_russian)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (False,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE', 'LAST'],
                          [],
                          ))

    def test_06_parameters_nok_wrong_values(self):
        status, df = david_currency_check.get_iis_shares(market='foreign', tickers=['wrong'])
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (True,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE', 'LAST'],
                          [],
                          ))

    def test_07_parameters_nok_wrong_types(self):
        status, df = david_currency_check.get_iis_shares(market=666, tickers=david_currency_check.tickers_russian)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (False,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE', 'LAST'],
                          [],
                          ))

    def test_08_parameters_nok_wrong_types(self):
        status, df = david_currency_check.get_iis_shares(market='foreign', tickers=666)
        self.assertEqual((status,
                          isinstance(df, DataFrame),
                          df.columns.tolist(),
                          df.SECID.values.tolist()
                          ),
                         (False,
                          True,
                          ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE', 'LAST'],
                          [],
                          ))

if __name__ == '__main__':
    unittest.main(verbosity=1)

# suite = unittest.TestLoader().loadTestsFromTestCase(TestFiles)
# runner = unittest.TextTestRunner(verbosity=2)
# runner.run(suite)

# suite = unittest.TestLoader().loadTestsFromTestCase(TestWebServer)
# runner = unittest.TextTestRunner(verbosity=2)
# runner.run(suite)