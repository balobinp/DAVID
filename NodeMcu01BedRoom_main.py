# main.py
# This file is executed after boot.py on every boot

# Actions:
# Read DHT sensor periodically
# Send the data from the sensor to the server
# Display the data from the sensor on the OLED

import dht

d = dht.DHT11(Pin(0))

while True:
    d.measure()
    r = urequests.get(
        'http://{0}:{1}/climate;sensor={2}&readattempt=0&temperature={3}&humidity={4}'.format(
            ip_server, port_server, sensor_id, d.temperature(), d.humidity()))
    clear_screen(oled)
    oled.text('Temp.:  {} C'.format(d.temperature()), 0, 20)
    oled.text('Hum.:   {} %'.format(d.humidity()), 0, 30)
    if r.status_code == 200:
        oled.text('Server: OK', 0, 50)
    else:
        oled.text('Server: {}'.format(r.status_code), 0, 50)
    oled.show()
    r.close()
    sleep(900)