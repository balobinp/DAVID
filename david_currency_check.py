import sqlite3
import pandas as pd  # type: ignore
from pandas import DataFrame
from os.path import isfile, join
import requests
import xml.etree.ElementTree as ET
import logging
import datetime as dt
from typing import Optional, Tuple

import david_lib
from david_lib import check_file
import david_user_interface

dir_david = david_lib.dir_david
file_log_currency_check = david_lib.file_log_currency_check
file_log_currency_check_path = join(dir_david, file_log_currency_check)
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)
tickers_foreign = david_lib.tickers_foreign
tickers_russian = david_lib.tickers_russian
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


def get_iis_shares(market: str = 'foreign', tickers: list = []) -> Tuple[bool, DataFrame]:
    """
    Get price of shares from IIS MOEX.

    :param market: IIS market. Values: 'foreign', 'russian'. Default is 'foreign'.
    :param tickers: list of tickers. Leave empty to get all. Default empty list.
    :return: status, DataFrame[['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE', 'LAST']]

    Examples
    -----
    >>> status, df = get_iis_shares(market='foreign', tickers=['AAPL-RM'])
    >>> if status:
    >>>    display(df)
    """

    urls = {'russian': r'https://iss.moex.com/iss/engines/stock/markets/shares/boards/tqbr/securities.xml',
            'foreign': r'https://iss.moex.com/iss/engines/stock/markets/foreignshares/securities.xml'}

    url = urls.get(market, '')

    iis_shares = []
    iis_shares_cols = ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE']
    iis_shares_last = []
    iis_shares_last_cols = ['SECID', 'LAST']
    iis_shares_return_cols = ['SECID', 'PREVPRICE', 'SECNAME', 'PREVDATE', 'LAST']

    try:
        resp = requests.get(url, timeout=3)
        currency_check_log.info(
            f'Message=http_currency_request;Response_ok={resp.ok};Reason={resp.reason};Status={resp.status_code}')
    except Exception as err:
        currency_check_log.error(f'Message=http_currency_request;Error={err}')
        return False, DataFrame(columns=iis_shares_return_cols)
    else:
        tree = ET.fromstring(resp.content)

        for data in tree.findall('data'):
            if data.attrib['id'] == 'securities':
                for row in data.find('rows').findall('row'):  # type: ignore
                    iis_shares.append([row.attrib.get(name) for name in iis_shares_cols])
            if data.attrib['id'] == 'marketdata':
                for row in data.find('rows').findall('row'):  # type: ignore
                    iis_shares_last.append([row.attrib.get(name) for name in iis_shares_last_cols])

        iis_shares_df = pd.merge(DataFrame(iis_shares, columns=iis_shares_cols),
                                 DataFrame(iis_shares_last, columns=iis_shares_last_cols),
                                 how='left', on='SECID')

        if isinstance(tickers, list) and tickers:
            return True, iis_shares_df.loc[iis_shares_df.SECID.isin(tickers)]
        elif isinstance(tickers, list):
            return True, iis_shares_df
        else:
            return False, DataFrame(columns=iis_shares_return_cols)


def get_valuta(valuta_name: str = 'USD', url: str = url_cbrf) -> Tuple[str, Optional[str]]:
    """
    Get currency rate from Url.

    :param valuta_name: Currency ticker. Default value is 'USD'.
    :param url: Url to get currency rate. Default 'https://www.cbr.ru/scripts/XML_daily.asp'
    :return: (Currency ticker, Currency rate) or (Currency ticker, None) in case of error.
    """
    try:
        resp = requests.get(url, timeout=3)
        currency_check_log.info(f'Message=http_currency_request;Response_ok={resp.ok};Reason={resp.reason};Status={resp.status_code}')
    except Exception as err:
        currency_check_log.error(f'Message=http_currency_request;Error={err}')
        return valuta_name, None
    else:
        tree = ET.fromstring(resp.content)
        for valute in tree.iter('Valute'):
            if valute.find('CharCode').text == valuta_name:  # type: ignore
                char_code = valute.find('CharCode').text  # type: ignore
                rate = valute.find('Value').text  # type: ignore
                currency_check_log.info(f'Message=http_currency_request;CharCode={char_code};Rate={rate}')
                if isinstance(char_code, str) and isinstance(rate, str):
                    return char_code, rate
        return valuta_name, None


def currency_rate_db_insert(char_code: str, rate: str) -> None:
    """
    Insert currency rate in database.

    :param char_code: Currency ticker.
    :param rate: Currency rate.
    :return: None
    """
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
        currency_check_log.info(f'Message=currency_rate_db_insert;CharCode={char_code};Rate={rate}')
    return None


def currency_check() -> Tuple[str, str, str, str]:
    """
    Fetch the last nd the previous USD rate a from database and check the difference.

    :return: Tuple[status, currency_rate, currency_name, rep_date].
    status can be 'currency_abnormal_increase' / 'currency_abnormal_decrease' / 'currency_normal'
    """
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
            ORDER BY a.ID DESC
            LIMIT 1''')
        rep_date, currency_name, currency_rate, prev_currency_rate, currency_change_per = cur.fetchone()
        rep_date = dt.datetime.strptime(rep_date, '%Y-%m-%d %H:%M:%S')
        conn.close()
        if currency_name and currency_rate and prev_currency_rate and currency_change_per:
            currency_check_log.debug(
                f'Message=currency_check;{currency_name};{currency_rate};{prev_currency_rate};{currency_change_per}')
        else:
            currency_check_log.error(f'Message=currency_check;not_all_data_collected')

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

    check_file(currency_check_log, file_log_currency_check_path)

    char_code, usd_rate = get_valuta('USD')

    if usd_rate:
        currency_rate_db_insert(char_code, usd_rate)

    currency_check_result, currency_rate, _, _ = currency_check()

    status, df = get_iis_shares(market='foreign', tickers=tickers_foreign)
    if status:
        html_foreign = df.sort_values(by='SECID').to_html()

    status, df = get_iis_shares(market='russian', tickers=tickers_russian)
    if status:
        html_russian = df.sort_values(by='SECID').to_html()

    inform_user_mail = david_user_interface.InformUser()

    message = f"""
<div>Result: {currency_check_result}, Value: {currency_rate}</div>
{html_foreign}
{html_russian}
"""
    inform_user_mail.mail('Currency Check', message, ["balobin.p@mail.ru", "pavel@roamability.com"])
