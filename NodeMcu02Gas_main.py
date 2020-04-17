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
    print("00 led_buzz red={}, grn={}, buz={}".format(red, grn, buz))
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

delay_rep = 900000 # Regular climate and gas sensors report interval
delay_gas = 5000
delay_mot = 1000 # Check motion sensor interval
delay_swh = 300000 # Delay for the light to switch off
delay_ovn = 10000 # Delay to check the oven
delay_fir = 600000 # No motion and high temperature near oven emergency delay

def read_dht(dht, att=10):
    for i in range(1, att+1):
        print("Read DHT attempt: {}".format(i))
        try:
            dht.measure()
            dht_tem = dht.temperature()
            dht_hum = dht.humidity()
            if dht_tem and dht_hum:
                return dht_tem, dht_hum, i
        except:
            sleep(0.1)
    return None, None, att

def dht_meas(deadline):
    """Read DHT sensor, update the screen and send the data to server"""
    if utime.ticks_diff(utime.ticks_ms(), deadline) > 0:
        dht_tem, dht_hum, att = read_dht(s_dht, att=10)
        print("DHT result in dht_meas: t={}, h={}, att={}".format(dht_tem, dht_hum, att))
        # s_dht.measure()
        # dht_tem = s_dht.temperature()
        # dht_hum = s_dht.humidity()
        clear_sym(oled, pos_x=7, pos_y=pos_tem, num=2, fill=0)
        clear_sym(oled, pos_x=7, pos_y=pos_hum, num=2, fill=0)
        oled.text('Temp.: {:>2} C'.format(dht_tem), 0, pos_tem)
        oled.text('Hum.:  {:>2} %'.format(dht_hum), 0, pos_hum)
        oled.show()
        r = urequests.get(
            'http://{0}:{1}/climate;sensor={2}&readattempt={3}&temperature={4}&humidity={5}'.format(
                ip_server, port_server, sensor_id, att, dht_tem, dht_hum))
        if r.status_code == 200:
            draw_bulet(oled, pos_x=13, pos_y=pos_tem)
            draw_bulet(oled, pos_x=13, pos_y=pos_hum)
        deadline = utime.ticks_add(utime.ticks_ms(), delay_rep)
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
            r = urequests.get(
                'http://{0}:{1}/gas;sensor={2}&sensorValue={3}&type={4}'.format(
                    ip_server, port_server, sensor_id, gaz_val, rep_type))
        elif utime.ticks_diff(utime.ticks_ms(), deadline_rep) > 0:
            r = urequests.get(
                'http://{0}:{1}/gas;sensor={2}&sensorValue={3}&type={4}'.format(
                    ip_server, port_server, sensor_id, gaz_val, rep_type))
            deadline_rep = utime.ticks_add(utime.ticks_ms(), delay_rep)
        deadline_gas = utime.ticks_add(utime.ticks_ms(), delay_gas)
    return deadline_gas, deadline_rep

def read_mot(deadline_mot, deadline_swh, deadline_fir):
    """Read the motion sensor"""
    print("read_mot")
    if utime.ticks_diff(utime.ticks_ms(), deadline_mot) > 0:
        clear_sym(oled, pos_x=1, pos_y=pos_mot, num=1)
        if s_mot.value():
            draw_bulet(oled, pos_x=1, pos_y=pos_mot)
            swh_1.on()
            deadline_swh = utime.ticks_add(utime.ticks_ms(), delay_swh)
            deadline_fir = utime.ticks_add(utime.ticks_ms(), delay_fir)
        elif utime.ticks_diff(utime.ticks_ms(), deadline_swh) > 0:
            swh_1.off()
        deadline_mot = utime.ticks_add(utime.ticks_ms(), delay_rep)
    return deadline_mot, deadline_swh, deadline_fir

def check_oven(deadline_fir):
    dht_tem, dht_hum, att = read_dht(s_dht, att=10)
    print("01 check_oven in DHT result: dht_tem={}, att={}, t={}, d={}, diff={}".format(dht_tem, att,
                                                                    utime.ticks_ms(), deadline_fir,
                                                                    utime.ticks_diff(utime.ticks_ms(), deadline_fir)))
    if utime.ticks_diff(utime.ticks_ms(), deadline_fir) > 0 and dht_tem > tm_th_1:
        print("02 check_oven in inside if cicle")
        led_buzz(red=0, grn=0, buz=1)
        # send http request to the server
        r = urequests.get(
            'http://{0}:{1}/oven;sensor={2}&temperature={3}&type=1'.format(
                ip_server, port_server, sensor_id_tmo_1, dht_tem), timeout=0.1)
    deadline_fir = utime.ticks_add(utime.ticks_ms(), delay_fir)
    print("03 check_oven in after if cicle: t={}, d={}, diff={}".format(utime.ticks_ms(), deadline_fir,
                                                             utime.ticks_diff(utime.ticks_ms(), deadline_fir)))
    return deadline_fir

deadline_rp = 0 # Report deadline
deadline_gs = 0 # Gas sensor deadline
deadline_mo = 0 # Motion sensor deadline
deadline_sw = 10000 # change to max Switching off the light
deadline_ov = 10000 # change to max Oven alert deadline
deadline_fr = 0 # Oven alarm deadline

clear_screen(oled)

# while True:
for _ in range(10):

    # Read DHT sensor every delay_dht interval,  update the screen and send the data to server
    deadline_rp = dht_meas(deadline_rp)

    # Read MQ-4 sensor every delay_gas interval, update the screen, LGB and buzzer
    # Send the report to data server in case of emergency and each delay_rep interval
    deadline_gs, deadline_rp = gas_meas(deadline_gs, deadline_rp)

    # Read the motion sensor every delay_mot interval. Update the screen.
    # Switch on the light for the delay_swh period in case if motion detected
    deadline_mo, deadline_sw, deadline_fr = read_mot(deadline_mo, deadline_sw, deadline_fr)

    # Check motion and the temperature and send the report to the server
    # Switch on the buzzer
    print("00 check_oven before: t={}, d={}, diff={}".format(
        utime.ticks_ms(), deadline_fr, utime.ticks_diff(utime.ticks_ms(), deadline_fr)))
    deadline_fr = check_oven(deadline_fr)
    print("04 check_oven after: t={}, d={}, diff={}".format(
        utime.ticks_ms(), deadline_fr, utime.ticks_diff(utime.ticks_ms(), deadline_fr)))

    utime.sleep(0.1)
