# main.py
# This file is executed after boot.py on every boot

# Actions:
# Read DHT sensor periodically
# Send the data from the sensor to the server
# Display the data from the sensor on the OLED

import dht

s_dht = dht.DHT22(Pin(0))
d_rep = 900

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

while True:
    dht_tem, dht_hum, att = read_dht(s_dht, att=10)
    r = get_req(
        'http://{0}:{1}/climate;sensor={2}&readattempt={3}&temperature={4}&humidity={5}'.format(
            ip_server, port_server, s_id_tmp_1, att, dht_tem, dht_hum))
    clear_screen(oled)
    oled.text('Temp.:  {} C'.format(dht_tem), 0, 20)
    oled.text('Hum.:   {} %'.format(dht_hum), 0, 30)
    if r == 200:
        oled.text('Server: OK', 0, 50)
    else:
        oled.text('Server: {}'.format(r), 0, 50)
    oled.show()
    sleep(d_rep)