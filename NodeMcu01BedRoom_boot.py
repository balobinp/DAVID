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
from machine import Pin, I2C
from time import sleep
import urequests
import ssd1306

version = 200404
ssid = 'Home'
passwd = 'ASDFGHQWERTY'
sensor_id = 1
ip_server = '192.168.1.44'
port_server = 80

def clear_screen(oled):
    oled.fill(0)
    oled.show()

# Setup OLED
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

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
r = urequests.get('http://{0}:{1}/connected;sensor={2}&ip={3}&ver={4}'.format(ip_server, port_server,
                                                                           sensor_id, ip_addr, version))

clear_screen(oled)
oled.text('Server response', 0, 10)
oled.text('status: {}'.format(r.status_code), 0, 20)
oled.text('Ver. : {}'.format(version), 0, 40)
oled.show()
r.close()
sleep(3)
clear_screen(oled)
