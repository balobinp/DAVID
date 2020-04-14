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

pos_tem = 10
pos_hum = 20
pos_gas = 30
pos_mot = 40

delay_rep = 900000 # delay for regular climate and gas sensors report
delay_gas = 5000
delay_mot = 1000
delay_swh = 300000 # delay for the switch
delay_ovn = 60000 # Delay to check the oven

def dht_meas(deadline):
    """Read DHT sensor, update the screen and send the data to server"""
    if utime.ticks_diff(utime.ticks_ms(), deadline) > 0:
        s_dht.measure()
        dht_tem = s_dht.temperature()
        dht_hum = s_dht.humidity()
        clear_sym(oled, pos_x=7, pos_y=pos_tem, num=2, fill=0)
        clear_sym(oled, pos_x=7, pos_y=pos_hum, num=2, fill=0)
        oled.text('Temp.: {:>2} C'.format(dht_tem), 0, pos_tem)
        oled.text('Hum.:  {:>2} %'.format(dht_hum), 0, pos_hum)
        oled.show()
        r = urequests.get(
            'http://{0}:{1}/climate;sensor={2}&readattempt=0&temperature={3}&humidity={4}'.format(
                ip_server, port_server, sensor_id, dht_tem, dht_hum))
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

def read_mot(deadline_mot, deadline_swh):
    """Read the motion sensor"""
    if utime.ticks_diff(utime.ticks_ms(), deadline_mot) > 0:
        clear_sym(oled, pos_x=1, pos_y=pos_mot, num=1)
        if s_mot.value():
            draw_bulet(oled, pos_x=1, pos_y=pos_mot)
            swh_1.on()
            deadline_swh = utime.ticks_add(utime.ticks_ms(), delay_swh)
        elif utime.ticks_diff(utime.ticks_ms(), deadline_swh) > 0:
            swh_1.off()
        deadline_mot = utime.ticks_add(utime.ticks_ms(), delay_rep)
    return deadline_mot, deadline_swh

def check_oven():
    s_dht.measure()
    dht_tem = s_dht.temperature()
    pass

deadline_rp = 0 # Report deadline
deadline_gs = 0 # Gas sensor deadline
deadline_mo = 0 # change to max Motion
deadline_sw = 0 # change to max Switching off the light
deadline_ov = 0 # change to max Oven alert deadline

clear_screen(oled)

# while True:
for _ in range(600):

    # Read DHT sensor every delay_dht interval,  update the screen and send the data to server
    deadline_rp = dht_meas(deadline_rp)

    # Read MQ-4 sensor every delay_gas interval, update the screen, LGB and buzzer
    # Send the report to data server in case of emergency and each delay_rep interval
    deadline_gs, deadline_rp = gas_meas(deadline_gs, deadline_rp)

    # Read the motion sensor every delay_mot interval. Update the screen.
    # Switch on the light for the delay_swh period in case if motion detected
    deadline_mo, deadline_sw = read_mot(deadline_mo, deadline_sw)

    # Check motion and the temperature and send the report to the server
    # Switch on the buzzer

    utime.sleep(0.1)
