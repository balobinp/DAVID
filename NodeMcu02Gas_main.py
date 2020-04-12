import webrepl_setup
# Выбрать E и установить пароль
E
y
123456
123456
y
#import webrepl
#webrepl.start()

import os
for item in os.listdir('/lib'):
    print(item)
os.remove('my_lib.py')
os.rmdir('temp')

import upip
upip.install('schedule')
upip.install("micropython-schedule")
upip.help()

import dht
import machine
import utime
d = dht.DHT11(machine.Pin(0))
d.measure()

from machine import ADC, Pin
mq = ADC(0)

led_b= Pin(12, Pin.OUT) # 12|D6
led_r= Pin(13, Pin.OUT) # 13|D7
led_g= Pin(15, Pin.OUT) # 15|D8

mq_th_1 = 150
mq_th_2 = 500

t_dht = utime.ticks_add(utime.ticks_ms(), 3000)
t_mq = utime.ticks_add(utime.ticks_ms(), 3000)
for _ in range(21):

    t_dht = t_meas(t_dht)
    t_mq = mq_meas(t_mq)
    utime.sleep(1)
    clear_screen(oled)

def t_meas(t_int):
    if utime.ticks_diff(utime.ticks_ms(), t_int) > 0:
        dh_temp = d.temperature()
        dh_hum = d.humidity()
        t_int = utime.ticks_add(utime.ticks_ms(), 5000)
        oled.text('Temp.: {} C'.format(dh_temp), 0, 20)
        oled.text('Hum.: {} %'.format(dh_hum), 0, 30)
        oled.show()
    return t_int

def mq_meas(t_int):
    if utime.ticks_diff(utime.ticks_ms(), t_int) > 0:
        mq_v = mq.read()
        if mq_v > mq_th_2:
            led_g.off()
            led_b.off()
            led_r.on()
        elif mq_v > mq_th_1:
            led_g.off()
            led_r.off()
            led_b.on()
        elif mq_v <= mq_th_1:
            led_b.off()
            led_r.off()
            led_g.on()
        t_int = utime.ticks_add(utime.ticks_ms(), 5000)
        oled.text('MQ-4.: {}'.format(mq_v), 0, 40)
        oled.show()
    return t_int

mq.read()

led_g.on()
led_g.off()

led_r.on()
led_r.off()

led_b.on()
led_b.off()