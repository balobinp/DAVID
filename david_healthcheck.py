#python3.6
#Author: balobin.p@mail.ru

from os.path import isfile, join
import logging
import sqlite3
import psutil
import datetime as dt

from david_currency_check import currency_check
from david_climate_check import get_climate_data
import david_user_interface
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
    climate_data_results = get_climate_data()
    result = {}
    for results in climate_data_results:
        result.update({results[0]: results[1]})
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

def fetch_motion_data():
    conn = sqlite3.connect(file_sqlite_db_path)
    cur = conn.cursor()
    sql_str = """SELECT REP_DATE, LOCATION
    FROM V_MOTION_SENSORS WHERE REP_DATE >= DATETIME('now','-1 day');"""
    cur.execute(sql_str)
    result = []
    for results in cur:
        result.append(results)
    conn.close()
    healthcheck_logger.debug(f'Message=get_data_from_db;motion={result}')
    if not result:
        return None
    else:
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
    motion_data = fetch_motion_data()

    healthcheck_report_dict = {'gas_sensor_data': gas_sensor_value,
                               'climate_data': climate_data,
                               'currency_data': {currency_name: {'rep_date': rep_date,
                                                                 'currency_check_result': currency_check_result,
                                                                 'currency_rate': currency_rate,} },
                               'system_data': system_data_dict}

    healthcheck_logger.debug(f'Message=healthcheck_report;report={healthcheck_report_dict}')

    dt_today = dt.date.today()

    message_subject = f"David report {dt_today}\n"
    message = """
<div>
<table class=MsoNormalTable border=0 cellspacing=5 cellpadding=0
width="100%" style='width:100.0%;mso-cellspacing:1.5pt;mso-yfti-tbllook:
1184'>
<tr style='mso-yfti-irow:1;mso-yfti-lastrow:yes'>
<td style='padding:10.5pt 0cm 0cm 0cm'>
<p class=MsoNormal align=center style='text-align:center'><span
style='font-size:15.0pt;font-family:ArialMT;mso-fareast-font-family:"Times New Roman";
color:#0E909A'>David Report for {current_date}<o:p></o:p></span></p>
</td>
</tr>
</table>
</div>
    """.format(current_date = dt_today)

    if healthcheck_report_dict['gas_sensor_data'] is None:
        message += "<div>No data from Gas sensors.</div>"
        print("Отсутствуют данные с датчика газа.")
    else:
        message += f"<div>Gas sensors data: {healthcheck_report_dict['gas_sensor_data']}</div>"
        print(f"Данные с датчика газа: {healthcheck_report_dict['gas_sensor_data']}")

    if healthcheck_report_dict['climate_data'] is None:
        message += "<div>No data from Climate sensors.</div>"
        print("Отсутствуют данные с датчика температуры.")
    else:
        message += f"<div>Climate sensors data: {healthcheck_report_dict['climate_data']}</div>"
        print(f"Данные с датчиов температуры: {healthcheck_report_dict['climate_data']}")

    dt_last_currency_check = healthcheck_report_dict['currency_data']['USD']['rep_date'].date()
    dt_diff_currency_check = (dt_last_currency_check - dt_today).days

    if dt_last_currency_check != dt_today:
        message += f"<div>No Currency data. The last update {abs(dt_diff_currency_check)} days ago.</div>"
        print(f"Отсутствуют данные по курсу доллара. Последнее обновление {abs(dt_diff_currency_check)} дней назад.")
    elif healthcheck_report_dict['currency_data']['USD']['currency_check_result'] == 'currency_normal':
        message += "<div>USD rate is normal.</div>"
        message += f"<div>Current rate {healthcheck_report_dict['currency_data']['USD']['currency_rate']} rubles.</div>"
        print(f"Курс доллара в норме. "
              f"Текущий курс {healthcheck_report_dict['currency_data']['USD']['currency_rate']} рублей.")
    else:
        message +=f"<div>Ubnormal USD rate.</div>"
        message += f"<div>Current rate {healthcheck_report_dict['currency_data']['USD']['currency_rate']} rubles.</div>"
        print(f"Превышены пороги изменения курса доллара."
              f"Текущий курс {healthcheck_report_dict['currency_data']['USD']['currency_rate']} рублей.")

    if healthcheck_report_dict['system_data']['cpu'] < 40:
        message += f"<div>CPU load is normal. Current value {healthcheck_report_dict['system_data']['cpu']}%.</div>"
        print(f"Загрузка CPU в норме. Текущее значение {healthcheck_report_dict['system_data']['cpu']}%.")
    else:
        message += f"<div>Ubnormal CPU load. Current value {healthcheck_report_dict['system_data']['cpu']}%.</div>"
        print(f"Превышена загрузка CPU. Текущее значение {healthcheck_report_dict['system_data']['cpu']}%.")

    if healthcheck_report_dict['system_data']['percent'] < 70:
        message += f"<div>Memory load is normal. Current value: {healthcheck_report_dict['system_data']['percent']}%.</div>"
        print(f"Загрузка памяти в норме. Текущее значение {healthcheck_report_dict['system_data']['percent']}%.")
    else:
        message += f"<div>Ubnormal memory load. Current value: {healthcheck_report_dict['system_data']['percent']}%.</div>"
        print(f"Превышена загрузка памяти. Текущее значение {healthcheck_report_dict['system_data']['percent']}%.")

    if motion_data:
        message += "<div>Motion detected:</div>"
        print("Обнаружены движения:")
        for iter, motion in enumerate(motion_data):
            message += f"<li>{iter}: {motion[0]} - {motion[1]}</li>"
            print(f"{iter}: {motion[0]} - {motion[1]}")
    else:
        message += "<div>No Motion detected.</div>"
        print("Движения не обнаружены.")

    inform_user_mail = david_user_interface.InformUser()
    inform_user_mail.mail(message_subject, message, ["balobin.p@mail.ru", "pavel@roamability.com"])

    # import pprint
    # pprint.pprint(message)


