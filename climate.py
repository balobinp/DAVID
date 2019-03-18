#python3.6

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import re
import sqlite3

ip_addr = '192.168.1.44'
port = 80


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.get_climat_handler()
        finally:
            messagetosend = bytes('OK', 'utf')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(messagetosend)
        
    def get_climat_handler(self):
        url = re.findall('GET /(.*) HTTP', self.requestline)
        get_url = urlparse(url[0])
        get_params = parse_qs(get_url.params, keep_blank_values=True)
        if get_url.path == 'climate':
            sensor_id = get_params.get('sensor')[0]
            attempt = get_params.get('readattempt')[0]
            temperature = get_params.get('temperature')[0]
            humidity = get_params.get('humidity')[0]
            conn = sqlite3.connect('david_db.sqlite')
            cur = conn.cursor()
            cur.execute('''INSERT INTO CLIMATE_SENSORS (REP_DATE, SENSOR_ID, ATTEMPT, TEMPERATURE, HUMIDITY)
                           VALUES (datetime(), ?, ?, ?, ?)''', (sensor_id, attempt, temperature, humidity))
            conn.commit()
            conn.close()

with HTTPServer((ip_addr, port), MyHandler) as httpd:
    print(f"Serving on port {port}...\nVisit http://{ip_addr}:{port}\nTo kill the server enter 'Ctrl + C'")
    httpd.serve_forever()
