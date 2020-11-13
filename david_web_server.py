# python3.6
# Version 0.8.0.dev 200911

from fastapi import BackgroundTasks, FastAPI, HTTPException
import uvicorn

# from flask import Flask, abort  # pip install Flask
# from flask_restful import Resource, Api  # pip install Flask-RESTful

from urllib.parse import parse_qs, urlparse
import sqlite3
from os.path import isfile, join
import logging
import datetime as dt
import time

import david_lib
import david_user_interface

# DavidServer
server_ip_addr = david_lib.ip_addr
server_port = david_lib.port
dir_david = david_lib.dir_david
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)
file_log_web_server = david_lib.file_log_web_server
file_log_web_server_path = join(dir_david, file_log_web_server)
timer_gas_mail_delay = david_lib.timer_gas_mail_delay
timer_oven_mail_delay = david_lib.timer_oven_mail_delay

# Create logger
web_server_log = logging.getLogger('web_server')
web_server_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
file_handler = logging.FileHandler(file_log_web_server_path)
file_handler.setFormatter(formatter)
web_server_log.addHandler(file_handler)

# Logger examples

# web_server_log.debug(f'Message=;')
# web_server_log.info(f'Message=;')
# web_server_log.warning(f'Message=;')
# web_server_log.error(f'Message=;')
# web_server_log.critical(f'Message=;')

inform_user = david_user_interface.InformUser()


def check_file(file_name):
    if isfile(file_name):
        web_server_log.info(f'Message=check_file;File={file_name};Result=exists')
    else:
        web_server_log.error(f'Message=check_file;File={file_name};Result=does_not_exist')


def get_request_handler(url_parameters):
    get_url = urlparse(url_parameters)
    get_params = parse_qs(get_url.params, keep_blank_values=True)
    return get_url, get_params


class Timer:

    def __init__(self, delay: int, deadline: int = 0) -> None:
        """
        Timer class callable is to define timers and delays.
        Return True if the timer has expired and False otherwise.
        :param delay: timer delay in seconds.
        :param deadline: time in seconds since the epoch when the Timer starts (default = 0).
        """
        self.delay = delay
        self.deadline = deadline

    def _diff(self):
        now = time.time()
        diff = self.deadline - now
        return now, diff

    def __call__(self):
        now, diff = self._diff()
        if diff < 0:
            self.deadline = now + self.delay
            return True
        elif diff >= 0:
            return False

    def __repr__(self):
        return f'{self.__class__.__name__}(delay={self.delay}, deadline={int(self.deadline)})'


class GetActions:
    timer_gas = Timer(delay=timer_gas_mail_delay)
    timer_oven = Timer(delay=timer_oven_mail_delay)

    def climate(self, get_params):
        sensor_id = get_params.get('sensor')[0]
        attempt = get_params.get('readattempt')[0]
        temperature = get_params.get('temperature')[0]
        humidity = get_params.get('humidity')[0]
        web_server_log.debug(
            f'Message=read_sensor;Sensor={sensor_id};Attempt={attempt};Temp={temperature};Hum={humidity}')
        try:
            conn = sqlite3.connect(file_sqlite_db_path)
        except Exception as e:
            web_server_log.error(f'Message=db_connect;Exception={e}')
        else:
            cur = conn.cursor()
            cur.execute('''INSERT INTO CLIMATE_SENSORS (REP_DATE, SENSOR_ID, ATTEMPT, TEMPERATURE, HUMIDITY)
                                        VALUES (datetime(), ?, ?, ?, ?)''',
                        (sensor_id, attempt, temperature, humidity))
            conn.commit()
            conn.close()

    def connected(self, get_params):
        sensor_id = get_params.get('sensor')[0]
        ip_addr = get_params.get('ip')[0]
        sensor_soft_version = get_params.get('ver', ['unk'])[0]
        web_server_log.info(f'Message=connected;Sensor={sensor_id};IP={ip_addr};Version={sensor_soft_version}')

    def motion(self, get_params):
        sensor_id = get_params.get('sensor')[0]
        web_server_log.debug(f'Message=read_sensor;Sensor={sensor_id}')
        try:
            conn = sqlite3.connect(file_sqlite_db_path)
        except Exception as e:
            web_server_log.error(f'Message=db_connect;Exception={e}')
        else:
            cur = conn.cursor()
            cur.execute('''INSERT INTO MOTION_SENSORS (REP_DATE, SENSOR_ID) VALUES (datetime(), ?)''', (sensor_id))
            conn.commit()
            conn.close()
        if sensor_id == '3':  # NodeMcu03Door
            try:
                dt_now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                subject = f"Motion detected {dt_now}"
                message = f"David indore motion detected at {dt_now}"
                # inform_user = david_user_interface.InformUser()
                inform_user.mail(subject, message, ["balobin.p@mail.ru", "pavel@roamability.com"])
                web_server_log.info(f'Message=inform_user_mail;Sensor={sensor_id};Sent=done')
            except Exception as e:
                web_server_log.error(f'Message=inform_user_mail;Exception={e}')

    def gas(self, get_params):
        sensor_id = get_params.get('sensor')[0]
        sensor_value = get_params.get('sensorValue')[0]
        gas_report_type_id = get_params.get('type', [0])[0]
        gas_report_type = 'emergency' if get_params.get('type', [0])[0] == '1' else 'regular'
        web_server_log.debug(
            f'Message=read_sensor;Sensor={sensor_id};GasSensorValue={sensor_value};Type={gas_report_type}')
        try:
            conn = sqlite3.connect(file_sqlite_db_path)
        except Exception as e:
            web_server_log.error(f'Message=db_connect;Exception={e}')
        else:
            cur = conn.cursor()
            cur.execute('''INSERT INTO GAS_SENSORS (REP_DATE, SENSOR_ID, SENSOR_VALUE)
                                        VALUES (datetime(), ?, ?)''', (sensor_id, sensor_value))
            conn.commit()
            conn.close()
        if gas_report_type == 'emergency' and self.timer_gas():
            try:
                dt_now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                subject = f"Gas emergency {dt_now}"
                message = f"David gas sensor emergency value detected at {dt_now}"
                result = inform_user.mail(subject, message, ["balobin.p@mail.ru", "pavel@roamability.com"])
                web_server_log.info(f'Message=inform_user_mail;Sensor={sensor_id};Result={result}')
                result = inform_user.play_file('gas_danger')
                web_server_log.info(f'Message=inform_user_play_file;Sensor={sensor_id};Result={result}')
            except Exception as e:
                web_server_log.error(f'Message=inform_user;Exception={e}')

    def oven(self, get_params):
        sensor_id = get_params.get('sensor')[0]
        temperature = get_params.get('temperature')[0]
        web_server_log.debug(f'Message=oven_control;Sensor={sensor_id};Temp={temperature}')
        if self.timer_oven():
            try:
                dt_now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                subject = f"Oven check {dt_now}"
                message = f"David high temperature over the oven at {dt_now}"
                result = inform_user.mail(subject, message, ["balobin.p@mail.ru", "pavel@roamability.com"])
                web_server_log.info(f'Message=inform_user_mail;Sensor={sensor_id};Result={result}')
                result = inform_user.play_file('check_oven')
                web_server_log.info(f'Message=inform_user_play_file;Sensor={sensor_id};Result={result}')
            except Exception as e:
                web_server_log.error(f'Message=inform_user;Sensor={sensor_id};Exception={e}')


app = FastAPI()

# app = Flask(__name__)
# api = Api(app)


get_actions = GetActions()


@app.get("/{parameters}")
async def get(parameters: str, background_tasks: BackgroundTasks):
    get_url, get_params = get_request_handler(parameters)

    if get_url.path == 'climate':
        background_tasks.add_task(get_actions.climate, get_params)
        # get_actions.climate(get_params)

    elif get_url.path == 'connected':
        background_tasks.add_task(get_actions.connected, get_params)
        # get_actions.connected(get_params)

    elif get_url.path == 'motion':
        background_tasks.add_task(get_actions.motion, get_params)
        # get_actions.motion(get_params)

    elif get_url.path == 'gas':
        background_tasks.add_task(get_actions.gas, get_params)
        # get_actions.gas(get_params)

    elif get_url.path == 'oven':
        background_tasks.add_task(get_actions.oven, get_params)
        # get_actions.oven(get_params)

    else:
        raise HTTPException(status_code=404)

    return 'OK'  # Отклик


# class DavidWebServerHandler(Resource):
#
#     get_actions = GetActions()
#
#     def get(self, parameters):
#         get_url, get_params = get_request_handler(parameters)
#
#         if get_url.path == 'climate':
#             self.get_actions.climate(get_params)
#
#         elif get_url.path == 'connected':
#             self.get_actions.connected(get_params)
#
#         elif get_url.path == 'motion':
#             self.get_actions.motion(get_params)
#
#         elif get_url.path == 'gas':
#             self.get_actions.gas(get_params)
#
#         elif get_url.path == 'oven':
#             self.get_actions.oven(get_params)
#
#         else:
#             abort(404)
#         return 'OK', 200  # Отклик и Status


if __name__ == '__main__':
    check_file(file_sqlite_db_path)
    check_file(file_log_web_server_path)

    uvicorn.run("david_web_server:app", host=server_ip_addr, port=server_port)

    # api.add_resource(DavidWebServerHandler, '/<string:parameters>')
    # app.run(host=server_ip_addr, port=server_port, debug=False)
