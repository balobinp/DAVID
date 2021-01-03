import dht
import utime
import math

s_dht = dht.DHT22(Pin(0))  # 0|D3 DHT sensor
s_gaz = ADC(0)  # Gaz sensor
s_mot = Pin(14, Pin.IN)  # 14|D5 Motion sensor
led_r = Pin(13, Pin.OUT)  # 13|D7 RGB LED red
led_g = Pin(15, Pin.OUT)  # 15|D8 RGB LED green
swh_1 = Pin(16, Pin.OUT, value=0)  # 16|D0 switch


def led_sw(red=0, grn=0):
    led_r.on() if red == 1 else led_r.off()
    led_g.on() if grn == 1 else led_g.off()


led_sw()

mq_th_1 = 200  # Gaz threshold level 1
mq_th_2 = 400  # Gaz threshold level 2

tm_th_1 = 28  # temperature oven alert threshold

pos_tem = 10
pos_hum = 20
pos_gas = 30
pos_mot = 40

# Prod delays
d_rep = 900000  # Regular climate and gas sensors report interval to server
d_gas = 5000  # Gas check interval
d_mot = 1000  # Check motion sensor interval
d_swh = 300000  # Delay for the light to switch off
d_ovn = 10000  # Delay to check the oven
d_fir = 600000  # No motion and high temperature near oven emergency delay


# Test delays
# d_rep = 6000 # Regular climate and gas sensors report interval to server
# d_gas = 3000 # Gas check interval
# d_mot = 1000 # Check motion sensor interval
# d_swh = 3000 # Delay for the light to switch off
# d_ovn = 2000 # Delay to check the oven
# d_fir = 7000 # No motion and high temperature near oven emergency delay


def read_dht(dht, att=10):
    for i in range(1, att + 1):
        try:
            dht.measure()
            dht_tem = dht.temperature() - 2
            dht_hum = dht.humidity()
            if dht_tem and dht_hum:
                return dht_tem, dht_hum, i
        except:
            sleep(0.1)
    return 0, 0, att


def dht_meas(deadline):
    if utime.ticks_diff(utime.ticks_ms(), deadline) > 0:
        dht_tem, dht_hum, att = read_dht(s_dht, att=10)
        if oled:
            clear_sym(oled, pos_x=7, pos_y=pos_tem, num=8, fill=0)
            clear_sym(oled, pos_x=7, pos_y=pos_hum, num=8, fill=0)
            oled.text('Temp.: {:.1f} C'.format(dht_tem), 0, pos_tem)
            oled.text('Hum.:  {:.1f} %'.format(dht_hum), 0, pos_hum)
            oled.show()
        r = get_req('http://{0}:{1}/climate;sensor={2}&readattempt={3}&temperature={4}&humidity={5}'.format(
            ip_server, port_server, s_id_tmp_2, att, dht_tem, dht_hum))
        if r == 200 and oled:
            draw_bulet(oled, pos_x=14, pos_y=pos_tem)
            draw_bulet(oled, pos_x=14, pos_y=pos_hum)
        deadline = utime.ticks_add(utime.ticks_ms(), d_rep)
        gc.collect()
    return deadline


def gas_ppm(val):
    m = -0.318
    b = 1.133
    R0 = 17  # for val 120
    sensor_volt = val * (5 / 1023.0)
    RS_gas = ((5 * 10.0) / sensor_volt) - 10.0
    ratio = RS_gas / R0
    ppm_log = (math.log(ratio, 10) - b) / m
    ppm = pow(10, ppm_log)
    percentage = round(ppm * 100 / 10000, 1)
    return str(percentage)[0:5]


def gas_meas(deadline_gas, deadline_rep):
    """Read Gaz sensor, update the screen, LGB and buzzer and send the emergency data to server"""
    if utime.ticks_diff(utime.ticks_ms(), deadline_gas) > 0:
        gaz_val = s_gaz.read()
        ppm = gas_ppm(gaz_val)
        rep_type = 0
        if gaz_val > mq_th_2:
            rep_type = 1
            led_sw(red=1, grn=0)
        elif gaz_val > mq_th_1:
            led_sw(red=1, grn=0)
        elif gaz_val <= mq_th_1:
            led_sw(red=0, grn=1)
        if oled:
            clear_sym(oled, pos_x=6, pos_y=pos_gas, num=9)
            oled.text('Gaz:  {:>5} %'.format(ppm), 0, pos_gas)
            oled.show()
        if rep_type == 1:
            get_req('http://{0}:{1}/gas;sensor={2}&sensorValue={3}&type={4}'.format(
                ip_server, port_server, s_id_gas_1, gaz_val, rep_type))
        elif utime.ticks_diff(utime.ticks_ms(), deadline_rep) > 0:
            r = get_req('http://{0}:{1}/gas;sensor={2}&sensorValue={3}&type={4}'.format(
                ip_server, port_server, s_id_gas_1, gaz_val, rep_type))
            if r == 200 and oled:
                draw_bulet(oled, pos_x=14, pos_y=pos_gas)
            deadline_rep = utime.ticks_add(utime.ticks_ms(), d_rep)
        deadline_gas = utime.ticks_add(utime.ticks_ms(), d_gas)
    return deadline_gas, deadline_rep


def read_mot(deadline_mot, deadline_swh, deadline_fir):
    """Read the motion sensor"""
    if utime.ticks_diff(utime.ticks_ms(), deadline_mot) > 0:
        if oled:
            clear_sym(oled, pos_x=1, pos_y=pos_mot, num=1)
        if s_mot.value():
            if oled:
                draw_bulet(oled, pos_x=1, pos_y=pos_mot)
            swh_1.on()
            get_req('http://{0}:{1}/motion;sensor=6'.format(ip_server, port_server))
            deadline_swh = utime.ticks_add(utime.ticks_ms(), d_swh)
            deadline_fir = utime.ticks_add(utime.ticks_ms(), d_fir)
            # buz_1.off() if buz_1.value() == 1 else None
        elif utime.ticks_diff(utime.ticks_ms(), deadline_swh) > 0:
            swh_1.off()
        deadline_mot = utime.ticks_add(utime.ticks_ms(), d_mot)
    return deadline_mot, deadline_swh, deadline_fir


def check_oven(deadline_fir, deadline_ovn):
    if utime.ticks_diff(utime.ticks_ms(), deadline_fir) > 0:
        dht_tem, dht_hum, att = read_dht(s_dht, att=10)
        if dht_tem > tm_th_1:
            # buz_1.on()
            # send http request to the server
            get_req('http://{0}:{1}/oven;sensor={2}&temperature={3}&type=1'.format(
                ip_server, port_server, s_id_tmo_1, dht_tem))
    deadline_ovn = utime.ticks_add(utime.ticks_ms(), d_ovn)
    return deadline_ovn


dl_tr = 0  # Report temperature deadline
dl_gr = 0  # Report gas deadline
dl_gs = 0  # Gas sensor deadline
dl_mo = 0  # Motion sensor deadline
dl_sw = 100000  # Switching off the light
dl_ov = 0  # Oven check deadline
dl_fr = 0  # Oven fire alarm deadline

if oled:
    clear_screen(oled)

while True:
    # Read DHT sensor every delay_dht interval,  update the screen and send the data to server
    dl_tr = dht_meas(dl_tr)

    # Read MQ-4 sensor every delay_gas interval, update the screen, LGB and buzzer
    # Send the report to data server in case of emergency and each delay_rep interval
    dl_gs, dl_gr = gas_meas(dl_gs, dl_gr)

    # Read the motion sensor every delay_mot interval. Update the screen.
    # Switch on the light for the delay_swh period in case if motion detected
    dl_mo, dl_sw, dl_fr = read_mot(dl_mo, dl_sw, dl_fr)

    # Check motion and the temperature and send the report to the server
    # Switch on the buzzer
    dl_ov = check_oven(dl_fr, dl_ov)

    utime.sleep(0.1)
