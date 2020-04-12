import dht
import utime

# Define pins for sensors and outputs
s_dht = dht.DHT11(Pin(0)) # DHT sensor
s_gaz = ADC(0) # Gaz sensor
s_mot = Pin(14, Pin.IN) # 14|D5 Motion sensor
led_r = Pin(13, Pin.OUT) # 13|D7 RGB LED red
led_g = Pin(15, Pin.OUT) # 15|D8 RGB LED green
buzz = Pin(16, Pin.OUT) # 16|D0 Buzzer

led_r.off()
led_g.off()
buzz.off()

mq_th_1 = 250 # Gaz threshold level 1
mq_th_2 = 500 # Gaz threshold level 2

pos_tem = 20
pos_hum = 30
pos_gaz = 40
pos_mot = 50

delay_dht = 900000
delay_gaz = 5000
delay_mot = 1000 # Read delay for motion sensor

# Read DHT sensor, update the screen and send the data to server
def dht_meas(deadline):
    if utime.ticks_diff(utime.ticks_ms(), deadline) > 0:
        s_dht.measure()
        dht_tem = s_dht.temperature()
        dht_hum = s_dht.humidity()
        clear_str(oled, pos=pos_tem)
        clear_str(oled, pos=pos_hum)
        oled.text('Temp.: {} C'.format(dht_tem), 0, pos_tem)
        oled.text('Hum.: {} %'.format(dht_hum), 0, pos_hum)
        oled.show()
        deadline = utime.ticks_add(utime.ticks_ms(), delay_dht)
    return deadline

# Read Gaz sensor, update the screen, LGB and buzzer and send the emergency data to server
def gaz_meas(deadline):
    if utime.ticks_diff(utime.ticks_ms(), deadline) > 0:
        gaz_val = s_gaz.read()
        if gaz_val > mq_th_2:
            led_g.off()
            led_r.on()
            buzz.on()
        elif gaz_val > mq_th_1:
            buzz.off()
            led_g.off()
            led_r.on()
        elif gaz_val <= mq_th_1:
            buzz.off()
            led_r.off()
            led_g.on()
        clear_str(oled, pos=pos_gaz)
        oled.text('MQ-4.: {}'.format(gaz_val), 0, pos_gaz)
        oled.show()
        deadline = utime.ticks_add(utime.ticks_ms(), delay_gaz)
    return deadline

# Read motion sensor
def mot_read(deadline):
    if utime.ticks_diff(utime.ticks_ms(), deadline) > 0:
        clear_str(oled, pos=pos_mot)
        if s_mot.value():
            clear_str(oled, pos=pos_mot)
            oled.text('Motion detected', 0, pos_mot)
            oled.show()
        deadline = utime.ticks_add(utime.ticks_ms(), delay_dht)
    return deadline

deadline_dh = utime.ticks_add(utime.ticks_ms(), delay_dht)
deadline_mq = utime.ticks_add(utime.ticks_ms(), delay_gaz)
deadline_mo = utime.ticks_add(utime.ticks_ms(), delay_mot)

clear_screen(oled)

# while True:
for _ in range(210):
    deadline_dh = dht_meas(deadline_dh)
    deadline_mq = gaz_meas(deadline_mq)
    deadline_mo = mot_read(deadline_mo)
    utime.sleep(0.1)
