#python3.6

import os
import sqlite3
from os.path import isfile, join
import logging

import david_lib

dir_david = david_lib.dir_david
file_climate_hot_bedroom = david_lib.file_climate_hot_bedroom
file_climate_hot_bedroom_path = join(dir_david, file_climate_hot_bedroom)
file_climate_cold_bedroom = david_lib.file_climate_cold_bedroom
file_climate_cold_bedroom_path = join(dir_david, file_climate_cold_bedroom)
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)
file_log_climate_check = david_lib.file_log_climate_check
file_log_climate_check_path = join(dir_david, file_log_climate_check)

climate_cold_threshold = david_lib.climate_cold_threshold
climate_hot_threshold = david_lib.climate_hot_threshold

# Create logger

climate_check_log = logging.getLogger('climate_check')
climate_check_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
file_handler = logging.FileHandler(file_log_climate_check_path)
file_handler.setFormatter(formatter)
climate_check_log.addHandler(file_handler)

# Logger examples

#climate_check.debug(f'Message=;')
#climate_check.info(f'Message=;')
#climate_check.warning(f'Message=;')
#climate_check.error(f'Message=;')
#climate_check.critical(f'Message=;')

def check_file(file_name):
    if isfile(file_name):
        return None
    else:
        climate_check_log.error(f'Message=check_file;File={file_name};Result=does_not_exist')

def get_climate_data():
    conn = sqlite3.connect(file_sqlite_db_path)
    cur = conn.cursor()
    sql_str = """SELECT s.LOCATION, TEMPERATURE FROM CLIMATE_SENSORS cs, SENSORS s
    WHERE REP_DATE >= DATETIME('now','-15 minute')
    AND TIME(REP_DATE) BETWEEN '05:00:00' AND '18:00:00'
    AND ID IN (SELECT MAX(ID) FROM CLIMATE_SENSORS GROUP BY SENSOR_ID)
    AND s.SENSOR_ID = cs.SENSOR_ID;"""
    cur.execute(sql_str)
    results = cur.fetchall()
    return results

if __name__ == '__main__':
    check_file(file_sqlite_db_path)
    check_file(file_log_climate_check_path)
    check_file(file_climate_hot_bedroom_path)

    results = get_climate_data()
    for result in results:
        climate_check_log.info(f'Message=got_data_from_table_climate_sensors;location={result[0]};t={result[1]}')
        if result and result[0] == 'bedroom' and result[1] > climate_hot_threshold:
            try:
                os.system("mpg123 " + file_climate_hot_bedroom_path)
                climate_check_log.debug(f'Message=playing_file;file={file_climate_hot_bedroom_path}')
            except Exception as e:
                climate_check_log.error(f'Message=playing_file;Exception={e}')
        elif result and result[0] == 'bedroom' and result[1] < climate_cold_threshold:
            try:
                os.system("mpg123 " + file_climate_cold_bedroom_path)
                climate_check_log.debug(f'Message=playing_file;file={file_climate_cold_bedroom_path}')
            except Exception as e:
                climate_check_log.error(f'Message=playing_file;Exception={e}')