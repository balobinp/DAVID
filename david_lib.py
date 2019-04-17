#python3.6

import requests
import xml.etree.ElementTree as ET

# DavidServer
ip_addr = '192.168.1.44'
port = 80
dir_david = r'/home/david'
file_climate_hot_bedroom = r'./VOICE_SAMPLES/climate_hot_bedroom.mp3'
file_sqlite_db = r'david_db.sqlite'
file_log_web_server = r'./log/david_web_server.log'
file_log_climate_check = r'./log/climate_check.log'

url_cbrf = 'http://www.cbr.ru/scripts/XML_daily.asp'

# For tests
#ip_addr = '192.168.1.52'
#port = 80
#dir_david = r'c:\Users\balob\Downloads\DAVID'
#file_climate_hot_bedroom = r'c:\Users\balob\Documents\DAVID\VOICE_SAMPLES\climate_hot_bedroom.mp3'
#file_sqlite_db = r'david_db.sqlite'
#file_log_web_server = r'.\log\david_web_server.log'
#file_log_climate_check = r'.\log\climate.log'

def get_valute(valute_name='USD'):
    resp = requests.get(url_cbrf)
    tree = ET.fromstring(resp.content)
    for valute in tree.iter('Valute'):
        if valute.find('CharCode').text == valute_name:
            return valute.find('CharCode').text, valute.find('Value').text