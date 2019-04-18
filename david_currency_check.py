#python3.6
#Author: balobin.p@mail.ru

from os.path import isfile
import requests
import xml.etree.ElementTree as ET
import logging
#from importlib import reload

#reload(logging)

file_log = r'/home/david/log/currency_check.log'
url_cbrf = 'http://www.cbr.ru/scripts/XML_daily.asp'

# Create logger
logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
currency_check = logging.getLogger('currency_check')

# Logger examples

#currency_check.debug(f'Message=;')
#currency_check.info(f'Message=;')
#currency_check.warning(f'Message=;')
#currency_check.error(f'Message=;')
#currency_check.critical(f'Message=;')

#Действия (для логирования):
#а. http_currency_request
#currency_check.info(f'Message=http_currency_request;')
#currency_check.error(f'Message=http_currency_request;')
#б. Записывает в базу данных.
#currency_check.debug(f'Message=;')
#currency_check.info(f'Message=;')
#currency_check.warning(f'Message=;')
#currency_check.error(f'Message=;')
#в. db_connect_write
#currency_check.debug(f'Message=;')
#currency_check.info(f'Message=;')
#currency_check.warning(f'Message=;')
#currency_check.error(f'Message=;')
#г. db_connect_read
#currency_check.debug(f'Message=;')
#currency_check.info(f'Message=;')
#currency_check.warning(f'Message=;')
#currency_check.error(f'Message=;')
#д. send_wa_notify
#currency_check.debug(f'Message=;')
#currency_check.info(f'Message=;')
#currency_check.warning(f'Message=;')
#currency_check.error(f'Message=;')

def check_file(file_name):
    if isfile(file_name):
        currency_check.info(f'Message=check_file;File={file_name};Result=exists')
    else:
        currency_check.error(f'Message=check_file;File={file_name};Result=does_not_exist')
    return None

def get_valute(valute_name='USD'):
    try:
        resp = requests.get(url_cbrf)
        currency_check.info(f'Message=http_currency_request;Response_ok={resp.ok};Reason={resp.reason};Status={resp.status_code}')
    except Exception as err:
        currency_check.error(f'Message=http_currency_request;Error={err}')
    else:
        tree = ET.fromstring(resp.content)
        for valute in tree.iter('Valute'):
            if valute.find('CharCode').text == valute_name:
                char_code = valute.find('CharCode').text
                rate = valute.find('Value').text
                currency_check.info(f'Message=http_currency_request;CharCode={char_code};Rate={rate}')
                return char_code, rate

check_file(file_log)

usd_rate = get_valute('USD')