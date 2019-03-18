#python3.5

import sqlite3

conn = sqlite3.connect('david_db.sqlite') 
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS CLIMATE_SENSORS')
cur.execute('''CREATE TABLE CLIMATE_SENSORS (REP_DATE TEXT
            ,ID INTEGER PRIMARY KEY AUTOINCREMENT
            ,SENSOR_ID INTEGER
            ,ATTEMPT INTEGER
            ,TEMPERATURE NUMERIC
            ,HUMIDITY NUMERIC)''')
conn.commit()
