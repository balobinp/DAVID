#python3.6
#Author: balobin.p@mail.ru

import os
from os.path import isfile, join
import sqlite3
import logging

import david_lib
import david_user_interface

dir_david = david_lib.dir_david
file_log_gas_check = david_lib.file_log_gas_check
file_log_gas_check_path = join(dir_david, file_log_gas_check)

mp3_files_dict = david_lib.mp3_files_dict
file_gas_danger_path = join(dir_david, mp3_files_dict['gas_danger'])

file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)

gas_emergency_threshold = david_lib.gas_emergency_threshold

# Create logger
gas_check_log = logging.getLogger('gas_check')
gas_check_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
file_handler = logging.FileHandler(file_log_gas_check_path)
file_handler.setFormatter(formatter)
gas_check_log.addHandler(file_handler)

# Logger examples

# gas_check_log.debug(f'Message=;')
# gas_check_log.info(f'Message=;')
# gas_check_log.warning(f'Message=;')
# gas_check_log.error(f'Message=;')
# gas_check_log.critical(f'Message=;')

# Действия (для логирования):
# а. check_file
# temp_log.debug(f'Message=check_file;')
# temp_log.info(f'Message=check_file;')

# б. get_data_from_db
# temp_log.debug(f'Message=get_data_from_db;')
# temp_log.info(f'Message=get_data_from_db;')

# в. playing_file
# temp_log.debug(f'Message=playing_file;')
# temp_log.info(f'Message=playing_file;')

def check_file(file_name):
    if isfile(file_name):
        return None
    else:
        gas_check_log.error(f'Message=check_file;File={file_name};Result=does_not_exist')
    return None

def get_gas_data():
    conn = sqlite3.connect(file_sqlite_db_path)
    cur = conn.cursor()
    sql_str = """SELECT SENSOR_VALUE FROM GAS_SENSORS
    WHERE REP_DATE >= DATETIME('now','-15 minute')
    AND ID = (SELECT MAX(ID) FROM GAS_SENSORS);"""
    cur.execute(sql_str)
    gas_sensor_value = None
    for results in cur:
        gas_sensor_value = results[0]
    conn.close()
    return gas_sensor_value


if __name__ == '__main__':

    check_file(file_sqlite_db_path)
    check_file(file_log_gas_check_path)
    check_file(file_gas_danger_path)

    inform_user = david_user_interface.InformUser()

    gas_sensor_value = get_gas_data()
    gas_check_log.info(f'Message=get_data_from_db;GasSensorValue={gas_sensor_value}')

    if gas_sensor_value and gas_sensor_value > gas_emergency_threshold:
        try:
            result = inform_user.play_file('gas_danger')
            gas_check_log.debug(f'Message=playing_file;file={file_gas_danger_path};Result={result}')
        except Exception as e:
            gas_check_log.error(f'Message=playing_file;Exception={e}')
