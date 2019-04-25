#python3.6
#Author: balobin.p@mail.ru
import sqlite3
from os.path import isfile, join
import requests
import xml.etree.ElementTree as ET
import logging

import david_lib

#from importlib import reload

#reload(logging)

dir_david = david_lib.dir_david
file_log_currency_check = david_lib.file_log_currency_check
file_log_currency_check_path = join(dir_david, file_log_currency_check)
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)
url_cbrf = 'http://www.cbr.ru/scripts/XML_daily.asp'

# Create logger
logging.basicConfig(filename=file_log_currency_check_path, level=logging.DEBUG, format='%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
currency_check_log = logging.getLogger('currency_check')

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
        resp = requests.get(url_cbrf)
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

if __name__ == '__main__':
    check_file(file_log_currency_check_path)
    char_code, usd_rate = get_valute('USD')
    currency_rate_db_insert(char_code, usd_rate)
