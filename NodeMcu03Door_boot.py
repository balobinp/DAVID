# import os
# import uos
import network
from machine import Pin, I2C, ADC
from time import sleep
from ntptime import settime
import urequests
import ujson
import webrepl
import utime

# import ssd1306

s_id_tmp_1 = 1 # temperature in NodeMcu01BedRoom (main sensor)
s_id_gas_1 = 2 # gas in NodeMcu02Gas (main sensor)
s_id_tmo_1 = 7 # temperature and motion in NodeMcu02Gas
s_id_dor_1 = 3 # NodeMcu03Door (main sensor)
s_id_drm_1 = 8 # motion Out of the door in NodeMcu03Door
s_id_drm_2 = 9 # motion Between the doors in NodeMcu03Door
s_id_drm_3 = 10 # motion D4 Inside in NodeMcu03Door

### SET VARIABLES HERE ###

version = 200814

ip_server = '192.168.1.44'
# ip_server = '192.168.1.63'
port_server = 80

s_id_ctr = s_id_dor_1 # NodeMcu03Door

# oled_width = 128
# oled_height = 64

###########################

with open('david_pass.json', "r") as json_file:
    passwords = ujson.load(json_file)

ssid = passwords['ssid']
passwd = passwords['wifi_passwd']

webrepl.start()

# Setup OLED

# i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# def clear_screen(oled):
#     oled.fill(0)
#     oled.show()

def get_req(url):
    try:
        r = urequests.get(url)
        st_cd = r.status_code
        r.close()
        return st_cd
    except:
        return None

# def clear_str(oled, pos=0, fill=0):
#     'OLED display pos=[0-50]'
#     for x in range(oled_width):
#         for y in range(pos, pos+10):
#             oled.pixel(x, y, fill)
#     oled.show()
#
# def clear_sym(oled, pos_x=0, pos_y=0, num=1, fill=0):
#     'OLED display os_x=[0-15], pos_y=[0-50], num=<symbols>'
#     for x in range(8*num):
#         for y in range(pos_y, pos_y+10):
#             oled.pixel(pos_x*8+x, y, fill)
#     oled.show()
#
# def draw_bulet(oled, pos_x=3, pos_y=0):
#     'OLED display os_x=[0-15], pos_y=[0-50], num=<symbols>'
#     bul = [
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,1,1,1,1,0,0],
#     [0,1,1,1,1,1,1,0],
#     [0,1,1,1,1,1,1,0],
#     [0,1,1,1,1,1,1,0],
#     [0,1,1,1,1,1,1,0],
#     [0,0,1,1,1,1,0,0],
#     [0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0],]
#     for y, line in enumerate(bul):
#         for x, fill in enumerate(line):
#             oled.pixel(x+pos_x*8, y+pos_y, fill)
#     oled.show()
#
# def strftime(t, t_form='full', type='utime', utc_sh=0):
#     '''
#     :param t: time tuple
#     :param t_form: time format 'date' / 'time' / 'full' /  'time_hm' / 'full_hm'
#     :param type: time tuple 'rtc' or 'utime'
#     :param utc_sh: utc time shift
#     :return: time string
#     '''
#     if type == 'rtc':
#         return '{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:03d}'.format(t[0], t[1], t[2], t[4], t[5], t[6], t[7])
#     elif type == 'utime':
#         t = utime.localtime(utime.mktime(t) + utc_sh * 3600)
#         if t_form == 'full':
#             return '{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(t[0], t[1], t[2], t[3], t[4], t[5])
#         elif t_form == 'date':
#             return '{}-{:02d}-{:02d}'.format(t[0], t[1], t[2])
#         elif t_form == 'time':
#             return '{:02d}:{:02d}:{:02d}'.format(t[3], t[4], t[5])
#         elif t_form == 'time_hm':
#             return '{:02d}:{:02d}'.format(t[3], t[4], t[5])
#         elif t_form == 'full_hm':
#             return '{}-{:02d}-{:02d} {:02d}:{:02d}'.format(t[0], t[1], t[2], t[3], t[4])

# Connecting to WiFi network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True) # Activate WiFi
sta_if.connect(ssid, passwd)

# clear_screen(oled)
# oled.text('Connecting to', 0, 20)
# oled.text('{} by WiFi...'.format(ssid), 0, 30)
# oled.show()
# sleep(1)

while not sta_if.isconnected():
    sleep(1)
ip_addr = sta_if.ifconfig()[0]

# clear_screen(oled)
# oled.text('Connected:', 0, 20)
# oled.text('{}'.format(ip_addr), 0, 30)
# oled.show()
# sleep(3)

# Time syncro

# clear_screen(oled)

try:
    settime()
    t = utime.localtime()
    # oled.text('Time set:', 24, 20)
    # oled.text(strftime(t, t_form='date', type='utime', utc_sh=3), 24, 30)
    # oled.text(strftime(t, t_form='time', type='utime', utc_sh=3), 24, 40)
except:
    pass
    # oled.text('Time not set.', 16, 30)
# oled.show()
# sleep(3)

# Send the notification to the server

r = get_req('http://{0}:{1}/connected;sensor={2}&ip={3}&ver={4}'.format(
    ip_server, port_server, s_id_ctr, ip_addr, version))

# Display the status on the OLED

# clear_screen(oled)
# oled.text('Server response', 0, 10)
# if r:
#     oled.text('status: {}'.format(r), 0, 20)
# else:
#     oled.text('status: {}'.format(r), 0, 20)
# oled.text('Ver. : {}'.format(version), 0, 40)
# oled.show()
# sleep(3)
# clear_screen(oled)
