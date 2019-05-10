#python3.6
#Author: balobin.p@mail.ru

from os.path import isfile, join
import logging
import sqlite3

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
                AND cs.ID IN (SELECT MAX(ID) FROM CLIMATE_SENSORS GROUP BY SENSOR_ID);"""
    cur.execute(sql_str)
    result = []
    for results in cur:
        # result = results
        result.append(results)
    conn.close()
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
    return result

if __name__ == '__main__':
    check_file(file_sqlite_db_path)
    check_file(file_log_healthcheck_path)
    gas_sensor_value = fetch_gas_data()
    climate_data = fetch_climate_data()
    currency_check_result, currency_rate, currency_name, rep_date = currency_check()

    healthcheck_report_dict = {'gas_sensor_data': gas_sensor_value,
                               'climate_data': climate_data,
                               'currency_data': [rep_date, currency_check_result, currency_rate, currency_name]}

    print(healthcheck_report_dict)