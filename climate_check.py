#python3.6

import os
from time import sleep
import sqlite3
from os.path import isfile
import logging

#from importlib import reload
#reload(logging)

file_climate_hot_bedroom = r'/home/pavel/david/VOICE_SAMPLES/climate_hot_bedroom.mp3'
file_sqlite_db = r'/home/user/david/david_db.sqlite'
file_log = r'/home/user/david/log/climate_check.log'

# For tests
#file_sqlite_db = r'c:\Users\balob\Downloads\DAVID\david_db.sqlite'
#file_log = r'c:\Users\balob\Downloads\DAVID\log\climate.log'

# Create logger
logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
climate_check = logging.getLogger('climate_check')

# Logger examples

#climate_check.debug(f'Message=;')
#climate_check.info(f'Message=;')
#climate_check.warning(f'Message=;')
#climate_check.error(f'Message=;')
#climate_check.critical(f'Message=;')

def check_file(file_name):
    if isfile(file_name):
        climate_check.info(f'Message=check_file;File={file_name};Result=exists')
    else:
        climate_check.error(f'Message=check_file;File={file_name};Result=does_not_exist')

def get_climate_data():
    conn = sqlite3.connect(file_sqlite_db)
    cur = conn.cursor()
    sql_str = """SELECT TEMPERATURE FROM CLIMATE_SENSORS
    WHERE REP_DATE >= DATETIME('now','-15 minute')
    AND TIME(REP_DATE) BETWEEN '07:00:00' AND '18:00:00'
    AND ID = (SELECT MAX(ID) FROM CLIMATE_SENSORS);"""
    cur.execute(sql_str)
    t = None
    for results in cur:
        t = results[0]
    conn.close()
    return t

check_file(file_sqlite_db)
check_file(file_log)
check_file(file_climate_hot_bedroom)

while True:
    t = get_climate_data()
    climate_check.info(f'Message=got_data_from_table_climate_sensors;t={t}')
    if t and t > 25:
        try:
            os.system("mpg123 " + file_climate_hot_bedroom)
            climate_check.debug(f'Message=playing_file;file={file_climate_hot_bedroom}')
        except Exception as e:
            climate_check.error(f'Message=playing_file;Exception={e}')
        finally:
            sleep(15*60)
    else:
        sleep(15*60)