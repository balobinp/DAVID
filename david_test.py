from flask import Flask # pip install Flask
from flask_restful import Resource, Api # pip install Flask-RESTful
from urllib.parse import parse_qs, urlparse

import david_lib

server_ip_addr = david_lib.ip_addr
server_ip_addr = '192.168.1.53'
server_port = david_lib.port

app = Flask(__name__)
api = Api(app)

def get_request_handler(url_parameters):
    get_url = urlparse(url_parameters)
    get_params = parse_qs(get_url.params, keep_blank_values=True)
    return get_url, get_params


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
                cur = conn.cursor()
                cur.execute('''INSERT INTO CLIMATE_SENSORS (REP_DATE, SENSOR_ID, ATTEMPT, TEMPERATURE, HUMIDITY)
                               VALUES (datetime(), ?, ?, ?, ?)''', (sensor_id, attempt, temperature, humidity))
            except Exception as e:
                web_server_log.error(f'Message=db_connect;Exception={e}')
            finally:
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
                cur = conn.cursor()
                cur.execute('''INSERT INTO MOTION_SENSORS (REP_DATE, SENSOR_ID)
                               VALUES (datetime(), ?)''', (sensor_id))
            except Exception as e:
                web_server_log.error(f'Message=db_connect;Exception={e}')
            finally:
                conn.commit()
                conn.close()

        return 'OK', 200 # Отклик и Status

api.add_resource(DavidWebServerHandler, '/<string:parameters>')

if __name__ == '__main__':
    app.run(host=server_ip_addr, port=server_port, debug=True)