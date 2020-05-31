import dht
import utime

# Define pins for sensors and outputs
s_dht = dht.DHT11(Pin(0)) # 0|D3 DHT sensor
s_gaz = ADC(0) # Gaz sensor
s_mot = Pin(14, Pin.IN) # 14|D5 Motion sensor
led_r = Pin(13, Pin.OUT) # 13|D7 RGB LED red
led_g = Pin(15, Pin.OUT) # 15|D8 RGB LED green
buz_1 = Pin(16, Pin.OUT) # 16|D0 Buzzer
swh_1 = Pin(2, Pin.OUT) # 2|D4 switch

def led_buzz(red=0, grn=0, buz=0):
    led_r.on() if red == 1 else led_r.off()
    led_g.on() if grn == 1 else led_g.off()
    buz_1.on() if buz == 1 else buz_1.off()

led_buzz()

mq_th_1 = 250 # Gaz threshold level 1
mq_th_2 = 500 # Gaz threshold level 2

tm_th_1 = 30 # temperature oven alert threshold

pos_tem = 10
pos_hum = 20
pos_gas = 30
pos_mot = 40

# Prod delays
d_rep = 900000 # Regular climate and gas sensors report interval to server
d_gas = 5000 # Gas check interval
d_mot = 1000 # Check motion sensor interval
d_swh = 300000 # Delay for the light to switch off
d_ovn = 10000 # Delay to check the oven
d_fir = 600000 # No motion and high temperature near oven emergency delay

# Testing delays
# d_rep = 6000 # Regular climate and gas sensors report interval to server
# d_gas = 3000 # Gas check interval
# d_mot = 1000 # Check motion sensor interval
# d_swh = 3000 # Delay for the light to switch off
# d_ovn = 2000 # Delay to check the oven
# d_fir = 7000 # No motion and high temperature near oven emergency delay

def read_dht(dht, att=10):
    for i in range(1, att+1):
        try:
            dht.measure()
            dht_tem = dht.temperature()-2
            dht_hum = dht.humidity()
            if dht_tem and dht_hum:
                return dht_tem, dht_hum, i
        except:
            sleep(0.1)
    return 0, 0, att

def dht_meas(deadline):
    """Read DHT sensor, update the screen and send the data to server"""
    if utime.ticks_diff(utime.ticks_ms(), deadline) > 0:
        dht_tem, dht_hum, att = read_dht(s_dht, att=10)
        # s_dht.measure()
        # dht_tem = s_dht.temperature()
        # dht_hum = s_dht.humidity()
        clear_sym(oled, pos_x=7, pos_y=pos_tem, num=2, fill=0)
        clear_sym(oled, pos_x=7, pos_y=pos_hum, num=2, fill=0)
        oled.text('Temp.: {:>2} C'.format(dht_tem), 0, pos_tem)
        oled.text('Hum.:  {:>2} %'.format(dht_hum), 0, pos_hum)
        oled.show()
        r = get_req('http://{0}:{1}/climate;sensor={2}&readattempt={3}&temperature={4}&humidity={5}'.format(
                ip_server, port_server, s_id_tmp_2, att, dht_tem, dht_hum))
        if r == 200:
            draw_bulet(oled, pos_x=13, pos_y=pos_tem)
            draw_bulet(oled, pos_x=13, pos_y=pos_hum)
        deadline = utime.ticks_add(utime.ticks_ms(), d_rep)
    return deadline

def gas_meas(deadline_gas, deadline_rep):
    """Read Gaz sensor, update the screen, LGB and buzzer and send the emergency data to server"""
    if utime.ticks_diff(utime.ticks_ms(), deadline_gas) > 0:
        gaz_val = s_gaz.read()
        rep_type = 0
        if gaz_val > mq_th_2:
            rep_type = 1
            led_buzz(red=1, grn=0, buz=1)
        elif gaz_val > mq_th_1:
            led_buzz(red=1, grn=0, buz=0)
        elif gaz_val <= mq_th_1:
            led_buzz(red=0, grn=1, buz=0)
        clear_sym(oled, pos_x=6, pos_y=pos_gas, num=3)
        oled.text('Gaz:  {:>3}'.format(gaz_val), 0, pos_gas)
        oled.show()
        if rep_type == 1:
            get_req('http://{0}:{1}/gas;sensor={2}&sensorValue={3}&type={4}'.format(
                    ip_server, port_server, s_id_gas_1, gaz_val, rep_type))
        elif utime.ticks_diff(utime.ticks_ms(), deadline_rep) > 0:
            get_req('http://{0}:{1}/gas;sensor={2}&sensorValue={3}&type={4}'.format(
                    ip_server, port_server, s_id_gas_1, gaz_val, rep_type))
            deadline_rep = utime.ticks_add(utime.ticks_ms(), d_rep)
        deadline_gas = utime.ticks_add(utime.ticks_ms(), d_gas)
    return deadline_gas, deadline_rep

def read_mot(deadline_mot, deadline_swh, deadline_fir):
    """Read the motion sensor"""
    if utime.ticks_diff(utime.ticks_ms(), deadline_mot) > 0:
        clear_sym(oled, pos_x=1, pos_y=pos_mot, num=1)
        if s_mot.value():
            draw_bulet(oled, pos_x=1, pos_y=pos_mot)
            swh_1.on()
            deadline_swh = utime.ticks_add(utime.ticks_ms(), d_swh)
            deadline_fir = utime.ticks_add(utime.ticks_ms(), d_fir)
            buz_1.off() if buz_1.value() == 1 else None
        elif utime.ticks_diff(utime.ticks_ms(), deadline_swh) > 0:
            swh_1.off()
        deadline_mot = utime.ticks_add(utime.ticks_ms(), d_mot)
    return deadline_mot, deadline_swh, deadline_fir

def check_oven(deadline_fir, deadline_ovn):
    if utime.ticks_diff(utime.ticks_ms(), deadline_fir) > 0:
        dht_tem, dht_hum, att = read_dht(s_dht, att=10)
        if dht_tem > tm_th_1:
            buz_1.on()
            # send http request to the server
            get_req('http://{0}:{1}/oven;sensor={2}&temperature={3}&type=1'.format(
                    ip_server, port_server, s_id_tmo_1, dht_tem))
    deadline_ovn = utime.ticks_add(utime.ticks_ms(), d_ovn)
    return deadline_ovn

dl_tr = 0 # Report temperature deadline
dl_gr = 0 # Report gas deadline
dl_gs = 0 # Gas sensor deadline
dl_mo = 0 # Motion sensor deadline
dl_sw = 100000 # Switching off the light
dl_ov = 0 # Oven check deadline
dl_fr = 0 # Oven fire alarm deadline

clear_screen(oled)

while True:
# for _ in range(600):

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
