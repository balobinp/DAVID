#python3.6

from flask import Flask, abort # pip install Flask
from flask_restful import Resource, Api # pip install Flask-RESTful
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import re
import sqlite3
from os.path import isfile, join
import logging

import david_lib

#from importlib import reload
#reload(logging)

# DavidServer
server_ip_addr = david_lib.ip_addr
server_port = david_lib.port
dir_david = david_lib.dir_david
file_sqlite_db = david_lib.file_sqlite_db
file_sqlite_db_path = join(dir_david, file_sqlite_db)
file_log_web_server = david_lib.file_log_web_server
file_log_web_server_path = join(dir_david, file_log_web_server)

# Create logger
web_server_log = logging.getLogger('web_server')
web_server_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
file_handler = logging.FileHandler(file_log_web_server_path)
file_handler.setFormatter(formatter)
web_server_log.addHandler(file_handler)

# Logger examples

#climate.debug(f'Message=;')
#climate.info(f'Message=;')
#climate.warning(f'Message=;')
#climate.error(f'Message=;')
#climate.critical(f'Message=;')

def check_file(file_name):
    if isfile(file_name):
        web_server_log.info(f'Message=check_file;File={file_name};Result=exists')
    else:
        web_server_log.error(f'Message=check_file;File={file_name};Result=does_not_exist')

def get_request_handler(url_parameters):
    get_url = urlparse(url_parameters)
    get_params = parse_qs(get_url.params, keep_blank_values=True)
    return get_url, get_params

app = Flask(__name__)
api = Api(app)

class DavidWebServerHandler(Resource):
    def get(self, parameters):
        get_url, get_params = get_request_handler(parameters)

        if get_url.path == 'climate':
            sensor_id = get_params.get('sensor')[0]
            attempt = get_params.get('readattempt')[0]
            temperature = get_params.get('temperature')[0]
            humidity = get_params.get('humidity')[0]
            web_server_log.debug(f'Message=read_sensor;Sensor={sensor_id};Attempt={attempt};Temp={temperature};Hum={humidity}')
            try:
                conn = sqlite3.connect(file_sqlite_db_path)
            except Exception as e:
                web_server_log.error(f'Message=db_connect;Exception={e}')
            else:
                cur = conn.cursor()
                cur.execute('''INSERT INTO CLIMATE_SENSORS (REP_DATE, SENSOR_ID, ATTEMPT, TEMPERATURE, HUMIDITY)
                                VALUES (datetime(), ?, ?, ?, ?)''', (sensor_id, attempt, temperature, humidity))
                conn.commit()
                conn.close()
        elif get_url.path == 'connected':
            sensor_id = get_params.get('sensor')[0]
            ip_addr = get_params.get('ip')[0]
            web_server_log.info(f'Message=connected;Sensor={sensor_id};IP={ip_addr}')
        elif get_url.path == 'motion':
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
        else:
            abort(404)

        return 'OK', 200 # Отклик и Status


api.add_resource(DavidWebServerHandler, '/<string:parameters>')

check_file(file_sqlite_db_path)
check_file(file_log_web_server_path)

if __name__ == '__main__':
    app.run(host=server_ip_addr, port=server_port, debug=False)