# main.py
# This file is executed after boot.py on every boot

# Actions:
# Read DHT sensor periodically
# Send the data from the sensor to the server
# Display the data from the sensor on the OLED

import dht

s_dht = dht.DHT22(Pin(0))
pos_tem = 20
pos_hum = 30
pos_dat = 50

# Prod delays
d_rep = 900000 # report temperature deadline
d_dat = 60000  # update date on the screen delay
d_sdt = 86400000   # syncro date delay

# # Test delays
# d_rep = 10000
# d_dat = 1000
# d_sdt = 5000

version = 200717

def read_dht(dht, att=10):
    for i in range(1, att+1):
        try:
            dht.measure()
            dht_tem = dht.temperature()-3.6
            dht_hum = dht.humidity()
            if dht_tem and dht_hum:
                return dht_tem, dht_hum, i
        except:
            sleep(0.1)
    return 0, 0, att

def dht_meas(deadline):
    if utime.ticks_diff(utime.ticks_ms(), deadline) > 0:
        dht_tem, dht_hum, att = read_dht(s_dht, att=10)
        clear_sym(oled, pos_x=7, pos_y=pos_tem, num=8, fill=0)
        clear_sym(oled, pos_x=7, pos_y=pos_hum, num=8, fill=0)
        oled.text('Temp.: {:.1f} C'.format(dht_tem), 0, pos_tem)
        oled.text('Hum.:  {:.1f} %'.format(dht_hum), 0, pos_hum)
        oled.show()
        r = get_req('http://{0}:{1}/climate;sensor={2}&readattempt={3}&temperature={4}&humidity={5}'.format(
                ip_server, port_server, s_id_tmp_2, att, dht_tem, dht_hum))
        if r == 200:
            draw_bulet(oled, pos_x=14, pos_y=pos_tem)
            draw_bulet(oled, pos_x=14, pos_y=pos_hum)
        deadline = utime.ticks_add(utime.ticks_ms(), d_rep)
        gc.collect()
    return deadline

def scr_dt(deadline):
    if utime.ticks_diff(utime.ticks_ms(), deadline) > 0:
        t = utime.localtime()
        clear_str(oled, pos=pos_dat, fill=0)
        oled.text(strftime(t, t_form='full_hm', type='utime', utc_sh=3), 0, pos_dat)
        oled.show()
        deadline = utime.ticks_add(utime.ticks_ms(), d_dat)
    return deadline

def syn_dt(deadline):
    try:
        settime()
        t = utime.localtime()
    except:
        pass
    deadline = utime.ticks_add(utime.ticks_ms(), d_sdt)
    return deadline

dl_tr = 0 # Report temperature deadline
dl_dt = 0 # Date and time screen update delay
dl_ds = 0 # Date and time syncro delay

clear_screen(oled)

while True:

    # Read DHT sensor every delay_dht interval,  update the screen and send the data to server
    dl_tr = dht_meas(dl_tr)

    # Update date and time on the screen
    dl_dt = scr_dt(dl_dt)

    # Syncro date and time
    dl_ds = syn_dt(dl_ds)

    utime.sleep(0.1)