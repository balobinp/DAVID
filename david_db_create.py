#python3.6

import sqlite3
import datetime as dt
from os.path import join
import shutil

import david_lib

# DavidServer
dir_david = david_lib.dir_david
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)
file_sqlite_db_backup = f'david_db_{dt.datetime.now().strftime("%Y%m%d")}.sqlite'
file_sqlite_db_backup_path = join(dir_david, file_sqlite_db_backup)

# For tests
#file_sqlite_db = r'c:\Users\balob\Downloads\DAVID\david_db.sqlite'

shutil.copy(file_sqlite_db_path, file_sqlite_db_backup_path)

conn = sqlite3.connect(file_sqlite_db_path)
cur = conn.cursor()

# Tables

# cur.execute('DROP TABLE IF EXISTS CLIMATE_SENSORS')

cur.execute('''CREATE TABLE IF NOT EXISTS CLIMATE_SENSORS (REP_DATE TEXT
            ,ID INTEGER PRIMARY KEY AUTOINCREMENT
            ,SENSOR_ID INTEGER NOT NULL
            ,ATTEMPT INTEGER
            ,TEMPERATURE NUMERIC
            ,HUMIDITY NUMERIC)''')

cur.execute('DROP TABLE IF EXISTS SENSORS')

cur.execute('''CREATE TABLE IF NOT EXISTS SENSORS (SENSOR_ID INTEGER NOT NULL UNIQUE
            ,SENSOR_TYPE NVARCHAR(15)
            ,LOCATION NVARCHAR(55))''')

cur.execute('''INSERT INTO SENSORS (SENSOR_ID, SENSOR_TYPE, LOCATION) VALUES (?, ?, ?)''', (1, 'climate', 'bedroom'))
cur.execute('''INSERT INTO SENSORS (SENSOR_ID, SENSOR_TYPE, LOCATION) VALUES (?, ?, ?)''', (2, 'gas', 'kitchen'))
cur.execute('''INSERT INTO SENSORS (SENSOR_ID, SENSOR_TYPE, LOCATION) VALUES (?, ?, ?)''', (3, 'motion', 'indoor'))

#cur.execute('DROP TABLE IF EXISTS MOTION_SENSORS')

cur.execute('''CREATE TABLE IF NOT EXISTS MOTION_SENSORS (REP_DATE TEXT
            ,ID INTEGER PRIMARY KEY AUTOINCREMENT
            ,SENSOR_ID INTEGER NOT NULL)''')

#cur.execute('DROP TABLE IF EXISTS CURRENCY_RATES')

cur.execute('''CREATE TABLE IF NOT EXISTS CURRENCY_RATES (REP_DATE TEXT
            ,ID INTEGER PRIMARY KEY AUTOINCREMENT
            ,CURRENCY_NAME VARCHAR(3)
            ,CURRENCY_RATE FLOAT)''')

#cur.execute('DROP TABLE IF EXISTS GAS_SENSORS')

cur.execute('''CREATE TABLE IF NOT EXISTS GAS_SENSORS (REP_DATE TEXT
            ,ID INTEGER PRIMARY KEY AUTOINCREMENT
            ,SENSOR_ID INTEGER NOT NULL
            ,SENSOR_VALUE NUMERIC)''')

# Views

cur.execute('DROP VIEW IF EXISTS V_CLIMATE_SENSORS')

cur.execute('''CREATE VIEW V_CLIMATE_SENSORS AS
            SELECT
            strftime('%Y-%m-%d %H:%M:%S', datetime(cs.REP_DATE, 'localtime')) AS REP_DATE
            ,s.LOCATION
            ,cs.TEMPERATURE
            ,cs.HUMIDITY
            FROM CLIMATE_SENSORS cs, SENSORS s
            WHERE cs.SENSOR_ID = s.SENSOR_ID
            ORDER BY s.LOCATION, cs.REP_DATE DESC''')

cur.execute('DROP VIEW IF EXISTS V_MOTION_SENSORS')

cur.execute('''CREATE VIEW V_MOTION_SENSORS AS
            SELECT
            strftime('%Y-%m-%d %H:%M:%S', datetime(ms.REP_DATE, 'localtime')) AS REP_DATE
            ,s.LOCATION
            FROM MOTION_SENSORS ms, SENSORS s
            WHERE ms.SENSOR_ID = s.SENSOR_ID
            ORDER BY s.LOCATION, ms.REP_DATE DESC''')

cur.execute('DROP VIEW IF EXISTS V_GAS_SENSORS')

cur.execute('''CREATE VIEW V_GAS_SENSORS AS
            SELECT
            strftime('%Y-%m-%d %H:%M', datetime(gs.REP_DATE, 'localtime')) AS REP_DATE
            ,s.LOCATION
            ,gs.SENSOR_VALUE
            FROM GAS_SENSORS gs, SENSORS s
            WHERE gs.SENSOR_ID = s.SENSOR_ID
            ORDER BY s.LOCATION, gs.REP_DATE DESC''')

cur.execute('DROP VIEW IF EXISTS V_CHILDREN_MATH_TASK01')

cur.execute('''CREATE VIEW V_CHILDREN_MATH_TASK01 AS
            SELECT
            strftime('%Y-%m-%d', REP_DATE) AS REP_DATE
            ,USER_NAME
            ,COUNT(*) AS ATTEMPTS
            ,SUM(CASE WHEN SCORE = 5 THEN 1 ELSE 0 END) AS SCORE_FIVE
            FROM
            (
            SELECT strftime('%Y-%m-%d %H:%M:%S', mt.date) AS REP_DATE
            ,au.username AS USER_NAME
            ,SUM(CASE
            WHEN mt.sign = '+' AND (mt.first + mt.second) = mt.user_answer THEN 1
            WHEN mt.sign = '-' AND (mt.first - mt.second) = mt.user_answer THEN 1
            WHEN mt.sign = '*' AND (mt.first * mt.second) = mt.user_answer THEN 1
            ELSE 0 END) AS SCORE
            FROM children_math_task01 mt, auth_user au
            WHERE mt.user_id = au.id
            GROUP BY 1, 2
            )
            GROUP BY 1, 2
            ORDER BY USER_NAME, REP_DATE DESC''')

cur.execute('DROP VIEW IF EXISTS V_CHILDREN_MATH_TASK01_DETAILED')

cur.execute('''CREATE VIEW V_CHILDREN_MATH_TASK01_DETAILED AS
            SELECT mt.date  AS REP_DATE
            ,au.username AS USER_NAME
            ,CASE
            WHEN mt.sign = '+' AND (mt.first + mt.second) = mt.user_answer THEN 1
            WHEN mt.sign = '-' AND (mt.first - mt.second) = mt.user_answer THEN 1
            WHEN mt.sign = '*' AND (mt.first * mt.second) = mt.user_answer THEN 1
            ELSE 0 END AS ANSWER
            ,mt.first, mt.sign,mt.second
            FROM children_math_task01 mt, auth_user au
            WHERE mt.user_id = au.id
            ORDER BY REP_DATE DESC''')

cur.execute('DROP VIEW IF EXISTS V_CHILDREN_MATH_TASK02')

cur.execute('''CREATE VIEW V_CHILDREN_MATH_TASK02 AS
            SELECT
            strftime('%Y-%m-%d', t.date) AS REP_DATE,
            au.username AS USER_NAME,
            MAX(CASE WHEN c.answer = t.user_answer THEN 1 ELSE 0 END) AS USER_RESULT
            FROM children_math_contest01 c, children_math_task02 t, auth_user au
            WHERE c.id = t.contest01_task_id
            AND t.user_id = au.id
            GROUP BY 1, 2
            ORDER BY USER_NAME, REP_DATE DESC''')

cur.execute('DROP VIEW IF EXISTS V_CHILDREN_MATH_TASK02_DETAILED')

cur.execute('''CREATE VIEW V_CHILDREN_MATH_TASK02_DETAILED AS
            SELECT
            strftime('%Y-%m-%d %H:%M:%S', t.date) AS REP_DATE,
            au.username AS USER_NAME,
            c.id AS TASK_ID,
            CASE WHEN c.answer = t.user_answer THEN 1 ELSE 0 END AS USER_RESULT,
            t.user_answer AS USER_ANSWER, c.answer AS CORRECT_ANSWER
            FROM children_math_contest01 c, children_math_task02 t, auth_user au
            WHERE c.id = t.contest01_task_id
            AND t.user_id = au.id
            ORDER BY REP_DATE DESC''')

cur.execute('DROP VIEW IF EXISTS V_CHILDREN_ENG_IRR_VER_DETAILED')

cur.execute('''CREATE VIEW V_CHILDREN_ENG_IRR_VER_DETAILED AS
            SELECT
            strftime('%Y-%m-%d %H:%M:%S', vr.date) AS REP_DATE
            ,au.username AS USER_NAME
            ,v.infinitive ||','|| v.past ||','|| v.participle ||','|| v.translation AS VERB
            ,vr.user_answer AS USER_ANSWER
            ,CASE WHEN v.infinitive ||','|| v.past ||','|| v.participle ||','|| v.translation = vr.user_answer THEN '1' ELSE '0' END AS SCORE
            FROM english_irregularverbsresults vr
            INNER JOIN english_irregularverbs v ON vr.verb_id = v.id
            INNER JOIN auth_user au ON vr.user_id = au.id''')

cur.execute('DROP VIEW IF EXISTS V_CHILDREN_ENG_IRR_VER')

cur.execute('''CREATE VIEW V_CHILDREN_ENG_IRR_VER AS
            SELECT
            strftime('%Y-%m-%d', REP_DATE) AS REP_DATE
            ,USER_NAME
            ,COUNT(*) AS ATTEMPTS
            ,SUM(CASE WHEN SCORE = 3 THEN 1 ELSE 0 END) AS SCORE_HIGH FROM
            (
            SELECT
            strftime('%Y-%m-%d %H:%M:%S', vr.date) AS REP_DATE
            ,au.username AS USER_NAME
            ,SUM(CASE WHEN v.infinitive ||','|| v.past ||','|| v.participle ||','|| v.translation = vr.user_answer THEN '1' ELSE '0' END) AS SCORE
            FROM english_irregularverbsresults vr
            INNER JOIN english_irregularverbs v ON vr.verb_id = v.id
            INNER JOIN auth_user au ON vr.user_id = au.id
            GROUP BY 1,2
            )
            GROUP BY 1,2
            ORDER BY USER_NAME, REP_DATE DESC''')

conn.commit()
conn.close()
