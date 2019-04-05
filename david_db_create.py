#python3.5

import sqlite3

# DavidServer
file_sqlite_db = r'/home/user/david/david_db.sqlite'

# For tests
file_sqlite_db = r'c:\Users\balob\Downloads\DAVID\david_db.sqlite'

conn = sqlite3.connect(file_sqlite_db)
cur = conn.cursor()

# cur.execute('DROP TABLE IF EXISTS CLIMATE_SENSORS')

cur.execute('''CREATE TABLE IF NOT EXISTS CLIMATE_SENSORS (REP_DATE TEXT
            ,ID INTEGER PRIMARY KEY AUTOINCREMENT
            ,SENSOR_ID INTEGER NOT NULL
            ,ATTEMPT INTEGER
            ,TEMPERATURE NUMERIC
            ,HUMIDITY NUMERIC)''')

cur.execute('DROP TABLE IF EXISTS SENSORS')

cur.execute('''CREATE TABLE IF NOT EXISTS SENSORS (SENSOR_ID INTEGER PRIMARY KEY
            ,SENSOR_TYPE NVARCHAR(15)
            ,LOCATION NVARCHAR(55))''')

cur.execute('''INSERT INTO SENSORS (SENSOR_ID, SENSOR_TYPE, LOCATION) VALUES (?, ?, ?)''', (1, 'climate', 'bedroom'))
cur.execute('''INSERT INTO SENSORS (SENSOR_ID, SENSOR_TYPE, LOCATION) VALUES (?, ?, ?)''', (3, 'motion', 'indoor'))

#cur.execute('DROP TABLE IF EXISTS MOTION_SENSORS')

cur.execute('''CREATE TABLE IF NOT EXISTS MOTION_SENSORS (REP_DATE TEXT
            ,ID INTEGER PRIMARY KEY AUTOINCREMENT
            ,SENSOR_ID INTEGER NOT NULL)''')

cur.execute('DROP VIEW IF EXISTS V_CLIMATE_SENSORS')

cur.execute('''CREATE VIEW V_CLIMATE_SENSORS AS
            SELECT
            strftime('%Y-%m-%d %H:%M', datetime(cs.REP_DATE, 'localtime')) AS REP_DATE
            ,s.LOCATION
            ,cs.TEMPERATURE
            ,cs.HUMIDITY
            FROM CLIMATE_SENSORS cs, SENSORS s
            WHERE cs.SENSOR_ID = s.SENSOR_ID
            ORDER BY s.LOCATION, cs.REP_DATE DESC''')

cur.execute('DROP VIEW IF EXISTS V_MOTION_SENSORS')

cur.execute('''CREATE VIEW V_MOTION_SENSORS AS
            SELECT
            strftime('%Y-%m-%d %H:%M', datetime(ms.REP_DATE, 'localtime')) AS REP_DATE
            ,s.LOCATION
            FROM MOTION_SENSORS ms, SENSORS s
            WHERE ms.SENSOR_ID = s.SENSOR_ID
            ORDER BY s.LOCATION, ms.REP_DATE DESC''')

conn.commit()
conn.close()
