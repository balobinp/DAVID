#python3.6

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import re
import sqlite3
from os.path import isfile
import logging

#from importlib import reload
#reload(logging)

# DavidServer
ip_addr = '192.168.1.44' 
port = 80
file_sqlite_db = r'/home/user/david/david_db.sqlite'
file_log = r'/home/user/david/log/climate.log'

# For tests
#ip_addr = '192.168.1.52' 
#port = 80
#file_sqlite_db = r'c:\Users\balob\Downloads\DAVID\david_db.sqlite'
#file_log = r'c:\Users\balob\Downloads\DAVID\log\climate.log'

# Create logger
logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(asctime)s;Application=%(name)s;%(levelname)s;%(message)s')
climate = logging.getLogger('climate')

# Logger examples

#climate.debug(f'Message=;')
#climate.info(f'Message=;')
#climate.warning(f'Message=;')
#climate.error(f'Message=;')
#climate.critical(f'Message=;')

def check_file(file_name):
    if isfile(file_name):
        climate.info(f'Message=check_file;File={file_name};Result=exists.')
    else:
        climate.error(f'Message=check_file;File={file_name};Result=does not exist.')


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.get_request_handler()
        finally:
            messagetosend = bytes('OK', 'utf')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(messagetosend)
        
    def get_request_handler(self):
        url = re.findall('GET /(.*) HTTP', self.requestline)
        get_url = urlparse(url[0])
        get_params = parse_qs(get_url.params, keep_blank_values=True)

        if get_url.path == 'climate':
            sensor_id = get_params.get('sensor')[0]
            attempt = get_params.get('readattempt')[0]
            temperature = get_params.get('temperature')[0]
            humidity = get_params.get('humidity')[0]
            climate.info(f'Message=read_sensor;Sensor={sensor_id};Attempt={attempt};Temp={temperature};Hum={humidity}')
            try:
                conn = sqlite3.connect(file_sqlite_db)
                cur = conn.cursor()
                cur.execute('''INSERT INTO CLIMATE_SENSORS (REP_DATE, SENSOR_ID, ATTEMPT, TEMPERATURE, HUMIDITY)
                               VALUES (datetime(), ?, ?, ?, ?)''', (sensor_id, attempt, temperature, humidity))
            except Exception as e:
                climate.error(f'Message=db_connect;Exception={e}')
            finally:
                conn.commit()
                conn.close()
        elif get_url.path == 'connected':
            sensor_id = get_params.get('sensor')[0]
            ip_addr = get_params.get('ip')[0]
            climate.info(f'Message=connected;Sensor={sensor_id};IP={ip_addr}')


check_file(file_sqlite_db)
check_file(file_log)


with HTTPServer((ip_addr, port), MyHandler) as httpd:
    print(f"Serving on port {port}...\nVisit http://{ip_addr}:{port}\nTo kill the server enter 'Ctrl + C'")
    httpd.serve_forever()