#python3.6
#Author: balobin.p@mail.ru
import sqlite3
from os.path import isfile, join
import requests
import xml.etree.ElementTree as ET
import logging
from twilio.rest import Client
import datetime as dt

import david_lib
import david_user_interface

#from importlib import reload

#reload(logging)

dir_david = david_lib.dir_david
file_log_currency_check = david_lib.file_log_currency_check
file_log_currency_check_path = join(dir_david, file_log_currency_check)
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)
url_cbrf = 'https://www.cbr.ru/scripts/XML_daily.asp'
currency_threshold_increase_per = david_lib.currency_threshold_increase_per
currency_usd_threshold_high = david_lib.currency_usd_threshold_high
currency_usd_threshold_low = david_lib.currency_usd_threshold_low

# Create logger

currency_check_log = logging.getLogger('currency_check')
currency_check_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
file_handler = logging.FileHandler(file_log_currency_check_path)
file_handler.setFormatter(formatter)
currency_check_log.addHandler(file_handler)

# Logger examples

#currency_check_log.debug(f'Message=;')
#currency_check_log.info(f'Message=;')
#currency_check_log.warning(f'Message=;')
#currency_check_log.error(f'Message=;')
#currency_check_log.critical(f'Message=;')

#Действия (для логирования):
#а. Получает курс валют с сайта ЦБРФ. http_currency_request
#currency_check_log.info(f'Message=http_currency_request;')
#currency_check_log.error(f'Message=http_currency_request;')
#б. Записывает в базу данных. currency_rate_db_insert
#currency_check_log.debug(f'Message=currency_rate_db_insert;')
#currency_check_log.info(f'Message=currency_rate_db_insert;')
#currency_check_log.warning(f'Message=currency_rate_db_insert;')
#currency_check_log.error(f'Message=currency_rate_db_insert;')
#в. Читает базу данных. Выполняет проверку полученных данных. currency_check
#currency_check_log.debug(f'Message=currency_check;')
#currency_check_log.info(f'Message=currency_check;')
#currency_check_log.warning(f'Message=currency_check;')
#currency_check_log.error(f'Message=currency_check;')
#г. Отправляет сообщение в WA. send_wa_notify
#currency_check_log.debug(f'Message=send_wa_notify;')
#currency_check_log.info(f'Message=send_wa_notify;')
#currency_check_log.warning(f'Message=send_wa_notify;')
#currency_check_log.error(f'Message=send_wa_notify;')

def check_file(file_name):
    if isfile(file_name):
        currency_check_log.info(f'Message=check_file;File={file_name};Result=exists')
    else:
        currency_check_log.error(f'Message=check_file;File={file_name};Result=does_not_exist')
    return None

def get_valute(valute_name='USD'):
    try:
        resp = requests.get(url_cbrf, timeout=3)
        currency_check_log.info(f'Message=http_currency_request;Response_ok={resp.ok};Reason={resp.reason};Status={resp.status_code}')
    except Exception as err:
        currency_check_log.error(f'Message=http_currency_request;Error={err}')
    else:
        tree = ET.fromstring(resp.content)
        for valute in tree.iter('Valute'):
            if valute.find('CharCode').text == valute_name:
                char_code = valute.find('CharCode').text
                rate = valute.find('Value').text
                currency_check_log.info(f'Message=http_currency_request;CharCode={char_code};Rate={rate}')
                return char_code, rate

def currency_rate_db_insert(char_code, rate):
    try:
        conn = sqlite3.connect(file_sqlite_db_path)
    except Exception as e:
        currency_check_log.error(f'Message=currency_rate_db_insert;Exception={e}')
    else:
        cur = conn.cursor()
        cur.execute('''INSERT INTO CURRENCY_RATES (REP_DATE, CURRENCY_NAME, CURRENCY_RATE)
                        VALUES (datetime(), ?, ?)''', (char_code, rate))
        conn.commit()
        conn.close()
    return None

def currency_check():
    try:
        conn = sqlite3.connect(file_sqlite_db_path)
    except Exception as e:
        currency_check_log.error(f'Message=currency_check;Exception={e}')
    else:
        cur = conn.cursor()
        cur.execute('''SELECT
            a.REP_DATE, a.CURRENCY_NAME, a.CURRENCY_RATE, b.CURRENCY_RATE AS PREV_CURRENCY_RATE
            ,IFNULL((a.CURRENCY_RATE - b.CURRENCY_RATE) * 100 / NULLIF(b.CURRENCY_RATE, 0), 0) AS CURRENCY_CHANGE_PER
            FROM CURRENCY_RATES a
            LEFT JOIN CURRENCY_RATES b ON b.ID = a.ID - 1
            WHERE a.CURRENCY_NAME = 'USD' AND b.CURRENCY_NAME = 'USD'
            ORDER BY a.REP_DATE DESC
            LIMIT 1''')
        rep_date, currency_name, currency_rate, prev_currency_rate, currency_change_per = cur.fetchone()
        rep_date = dt.datetime.strptime(rep_date, '%Y-%m-%d %H:%M:%S')
        conn.close()

        if type(currency_rate) is str:
            currency_rate = float(currency_rate.replace(',', '.'))
        if type(currency_change_per) is str:
            currency_change_per = float(currency_change_per.replace(',', '.'))

    if currency_change_per and \
            (currency_change_per > currency_threshold_increase_per or currency_rate > currency_usd_threshold_high):
        return 'currency_abnormal_increase', currency_rate, currency_name, rep_date
    elif currency_change_per and \
            (currency_change_per < currency_threshold_increase_per or currency_rate < currency_usd_threshold_low):
        return 'currency_abnormal_decrease', currency_rate, currency_name, rep_date
    else:
        return 'currency_normal', currency_rate, currency_name, rep_date


if __name__ == '__main__':
    check_file(file_log_currency_check_path)
    char_code, usd_rate = get_valute('USD')
    currency_rate_db_insert(char_code, usd_rate)
    currency_check_result, currency_rate, _, _ = currency_check()
    inform_user_mail = david_user_interface.InformUser()
    message = f"<div>Result: {currency_check_result}, Value: {currency_rate}</div>"
    inform_user_mail.mail('Currency Check', message, ["balobin.p@mail.ru", "pavel@roamability.com"])
