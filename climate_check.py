#python3.6

import os
from time import sleep
import sqlite3

file = "./VOICE_SAMPLES/climate_hot_bedroom.mp3"

def get_climate_data():
    conn = sqlite3.connect('../david/david_db.sqlite')
    cur = conn.cursor()
    sql_str = """SELECT REP_DATE, TEMPERATURE FROM CLIMATE_SENSORS
    WHERE REP_DATE >= DATETIME('now','-15 minute')
    AND TIME(REP_DATE) BETWEEN '07:00:00' AND '18:00:00'
    AND ID = (SELECT MAX(ID) FROM CLIMATE_SENSORS);"""
    cur.execute(sql_str)
    for results in cur:
        date = results[0]
        t = results[1]
    conn.close()
    return t

while True:
    t = get_climate_data()
    if t > 25:
        try:
            os.system("mpg123 " + file)
        finally:
            sleep(15*60)
    else:
        sleep(15*60)
