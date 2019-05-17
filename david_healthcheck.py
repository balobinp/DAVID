#python3.6
#Author: balobin.p@mail.ru

from os.path import isfile, join
import logging
import sqlite3
import psutil
import datetime as dt

from david_currency_check import currency_check
import david_lib

dir_david = david_lib.dir_david
file_log_healthcheck = david_lib.file_log_healthcheck
file_log_healthcheck_path = join(dir_david, file_log_healthcheck)
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)

# Create logger
healthcheck_logger = logging.getLogger('healthcheck')
healthcheck_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
file_handler = logging.FileHandler(file_log_healthcheck_path)
file_handler.setFormatter(formatter)
healthcheck_logger.addHandler(file_handler)

# Logger examples

# healthcheck_logger.debug(f'Message=;')
# healthcheck_logger.info(f'Message=;')
# healthcheck_logger.warning(f'Message=;')
# healthcheck_logger.error(f'Message=;')
# healthcheck_logger.critical(f'Message=;')

# Действия (для логирования):
# а. check_file
# healthcheck_logger.debug(f'Message=check_file;')
#
# б. get_data_from_db
# healthcheck_logger.debug(f'Message=get_data_from_db;')
#
# в. system_check
# # healthcheck_logger.debug(f'Message=system_check;')
#
# г. healthcheck_report
# healthcheck_logger.debug(f'Message=healthcheck_report;')

def check_file(file_name):
    if isfile(file_name):
        return None
    else:
        healthcheck_logger.error(f'Message=check_file;File={file_name};Result=does_not_exist')
    return None

def fetch_climate_data():
    conn = sqlite3.connect(file_sqlite_db_path)
    cur = conn.cursor()
    sql_str = """SELECT s.LOCATION, cs.TEMPERATURE
                FROM CLIMATE_SENSORS cs
                LEFT JOIN SENSORS s ON cs.SENSOR_ID = s.SENSOR_ID
                WHERE cs.REP_DATE >= DATETIME('now','-15 minute')
                AND s.SENSOR_TYPE = 'climate'
                AND cs.ID IN (SELECT MAX(ID) FROM CLIMATE_SENSORS GROUP BY SENSOR_ID);"""
    cur.execute(sql_str)
    result = {}
    for results in cur:
        # result = results
        result.update({results[0]: results[1]})
    conn.close()
    healthcheck_logger.debug(f'Message=get_data_from_db;climate={result}')
    if not result:
        return None
    else:
        return result

def fetch_gas_data():
    conn = sqlite3.connect(file_sqlite_db_path)
    cur = conn.cursor()
    sql_str = """SELECT SENSOR_VALUE FROM GAS_SENSORS
    WHERE REP_DATE >= DATETIME('now','-15 minute')
    AND ID = (SELECT MAX(ID) FROM GAS_SENSORS);"""
    cur.execute(sql_str)
    result = None
    for results in cur:
        result = results[0]
    conn.close()
    healthcheck_logger.debug(f'Message=get_data_from_db;gas={result}')
    return result

def get_system_data():
    system_data_dict = dict(psutil.virtual_memory()._asdict())
    system_data_dict.update({'cpu': psutil.cpu_percent()})
    healthcheck_logger.debug(f"Message=system_check;cpu={system_data_dict['cpu']}%;mem:{system_data_dict['percent']}%")
    return system_data_dict

if __name__ == '__main__':
    check_file(file_sqlite_db_path)
    check_file(file_log_healthcheck_path)
    gas_sensor_value = fetch_gas_data()
    climate_data = fetch_climate_data()
    currency_check_result, currency_rate, currency_name, rep_date = currency_check()
    system_data_dict = get_system_data()

    healthcheck_report_dict = {'gas_sensor_data': gas_sensor_value,
                               'climate_data': climate_data,
                               'currency_data': {currency_name: {'rep_date': rep_date,
                                                                 'currency_check_result': currency_check_result,
                                                                 'currency_rate': currency_rate,} },
                               'system_data': system_data_dict}

    healthcheck_logger.debug(f'Message=healthcheck_report;report={healthcheck_report_dict}')

    if healthcheck_report_dict['gas_sensor_data'] is None:
        print("Отсутствуют данные с датчика газа.")
    else:
        print(f"Данные с датчика газа: {healthcheck_report_dict['gas_sensor_data']}")

    if healthcheck_report_dict['climate_data'] is None:
        print("Отсутствуют данные с датчика температуры.")
    else:
        print(f"Данные с датчиов температуры: {healthcheck_report_dict['climate_data']}")

    dt_today = dt.date.today()
    dt_last_currency_check = healthcheck_report_dict['currency_data']['USD']['rep_date'].date()
    dt_diff_currency_check = (dt_last_currency_check - dt_today).days

    if dt_last_currency_check != dt_today:
        print(f"Отсутствуют данные по курсу доллара. Последнее обновление {abs(dt_diff_currency_check)} дней назад.")
    elif healthcheck_report_dict['currency_data']['USD']['currency_check_result'] == 'currency_normal':
        print(f"Курс доллара в норме. "
              f"Текущий курс {healthcheck_report_dict['currency_data']['USD']['currency_rate']} рублей.")
    else:
        print(f"Превышены пороги изменения курса доллара."
              f"Текущий курс {healthcheck_report_dict['currency_data']['USD']['currency_rate']} рублей.")

    if healthcheck_report_dict['system_data']['cpu'] < 40:
        print(f"Загрузка CPU в норме. Текущее значение {healthcheck_report_dict['system_data']['cpu']}%.")
    else:
        print(f"Превышена загрузка CPU. Текущее значение {healthcheck_report_dict['system_data']['cpu']}%.")

    if healthcheck_report_dict['system_data']['percent'] < 70:
        print(f"Загрузка памяти в норме. Текущее значение {healthcheck_report_dict['system_data']['percent']}%.")
    else:
        print(f"Превышена загрузка памяти. Текущее значение {healthcheck_report_dict['system_data']['percent']}%.")

    # import pprint
    # pprint.pprint(healthcheck_report_dict)

