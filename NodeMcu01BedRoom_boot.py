# Connections:
# OLED     NodeMcu
#  SDA <-> D2 (4)
#  SCL <-> D1 (5)

# DHT11     NodeMcu
#   OUT <-> D3 (0)

# boot.py
# This file is executed on every boot (including wake-boot from deepsleep)
# Actions:
# Connecting to the WiFi network
# Send the notification to the server
# Display the status on the OLED

import os
import uos
import network
from machine import Pin, I2C, ADC
from time import sleep
import urequests
import ujson
import webrepl

import ssd1306

with open('david_pass.json', "r") as json_file:
    passwords = ujson.load(json_file)

ssid = passwords['ssid']
passwd = passwords['wifi_passwd']

version = 200404
sensor_id = 1 # main sensor
sensor_id_gas_1 = 2 # gas sensor in the kitchen
sensor_id_tmo_1 = 4 # temperature and motion sensors in the kitchen
# ip_server = '192.168.1.44'
ip_server = '192.168.1.63'
port_server = 80

webrepl.start()

# Setup OLED
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def clear_screen(oled):
    oled.fill(0)
    oled.show()

def get_req(url):
    try:
        urequests.get(url)
        st_cd = r.status_code
        r.close()
        return st_cd
    except:
        return None

def clear_str(oled, pos=0, fill=0):
    'OLED display pos=[0-50]'
    for x in range(oled_width):
        for y in range(pos, pos+10):
            oled.pixel(x, y, fill)
    oled.show()

def clear_sym(oled, pos_x=0, pos_y=0, num=1, fill=0):
    'OLED display os_x=[0-15], pos_y=[0-50], num=<symbols>'
    for x in range(8*num):
        for y in range(pos_y, pos_y+10):
            oled.pixel(pos_x*8+x, y, fill)
    oled.show()

def draw_bulet(oled, pos_x=3, pos_y=0):
    'OLED display os_x=[0-15], pos_y=[0-50], num=<symbols>'
    bul = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],]
    for y, line in enumerate(bul):
        for x, fill in enumerate(line):
            oled.pixel(x+pos_x*8, y+pos_y, fill)
    oled.show()

# Connect to WiFi
sta_if = network.WLAN(network.STA_IF) 
sta_if.active(True) # Activate WiFi
sta_if.connect(ssid, passwd)
clear_screen(oled)
oled.text('Connecting to', 0, 20)
oled.text('{} by WiFi...'.format(ssid), 0, 30)
oled.show()
sleep(1)
while not sta_if.isconnected():
    sleep(1)
ip_addr = sta_if.ifconfig()[0]
clear_screen(oled)
oled.text('Connected:', 0, 20)
oled.text('{}'.format(ip_addr), 0, 30)
oled.show()
sleep(3)
r = get_req('http://{0}:{1}/connected;sensor={2}&ip={3}&ver={4}'.format(
    ip_server, port_server, sensor_id, ip_addr, version))
clear_screen(oled)
oled.text('Server response', 0, 10)
if r:
    oled.text('status: {}'.format(r), 0, 20)
else:
    oled.text('status: {}'.format(r), 0, 20)
oled.text('Ver. : {}'.format(version), 0, 40)
oled.show()
sleep(3)
clear_screen(oled)
