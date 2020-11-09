import network
from machine import Pin, I2C, ADC
from time import sleep
from ntptime import settime
import urequests
import ujson
import webrepl
import utime

s_id_tmp_1 = 1 # temperature in NodeMcu01BedRoom (main sensor)
s_id_gas_1 = 2 # gas in NodeMcu02Gas (main sensor)
s_id_tmo_1 = 7 # temperature and motion in NodeMcu02Gas
s_id_dor_1 = 3 # NodeMcu03Door (main sensor)
s_id_drm_1 = 8 # motion Out of the door in NodeMcu03Door
s_id_drm_2 = 9 # motion Between the doors in NodeMcu03Door
s_id_drm_3 = 10 # motion D4 Inside in NodeMcu03Door

### SET VARIABLES HERE ###

version = 201109

ip_server = '192.168.1.44'
# ip_server = '192.168.1.63'
port_server = 80

s_id_ctr = s_id_dor_1 # NodeMcu03Door

###########################

with open('david_pass.json', "r") as json_file:
    passwords = ujson.load(json_file)

ssid = passwords['ssid']
passwd = passwords['wifi_passwd']

webrepl.start()


def get_req(url):
    try:
        r = urequests.get(url)
        st_cd = r.status_code
        r.close()
        return st_cd
    except:
        return None

# Connecting to WiFi network


sta_if = network.WLAN(network.STA_IF)
sta_if.active(True) # Activate WiFi
sta_if.connect(ssid, passwd)

while not sta_if.isconnected():
    sleep(1)
ip_addr = sta_if.ifconfig()[0]

# Time syncro

try:
    settime()
    t = utime.localtime()
except:
    pass

# Send the notification to the server

r = get_req('http://{0}:{1}/connected;sensor={2}&ip={3}&ver={4}'.format(
    ip_server, port_server, s_id_ctr, ip_addr, version))
