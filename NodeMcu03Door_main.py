# NodeMcu03Door_main

version = 200814

from utime import ticks_diff, ticks_ms, ticks_add, sleep

# Prod delays
t_sw1 = 30000
t_sw2 = 30000
t_sw3 = 60000

# Test delays
# t_sw1 = 5000
# t_sw2 = 5000
# t_sw3 = 9000

ldr_th = 800  # Light Resistor value threshold

# Switches
sw1 = Pin(16, Pin.OUT)  # D0 Out of the door
sw2 = Pin(0, Pin.OUT)   # D3 Between the doors
sw3 = Pin(2, Pin.OUT)   # D4 Inside

# Motion sensors
mt1 = Pin(12, Pin.IN)  # D6 Out of the door
mt2 = Pin(13, Pin.IN)  # D7 Between the doors
mt3 = Pin(14, Pin.IN)  # D5 Inside

# Camera control
cam = Pin(15, Pin.OUT, value=0)  # D8

# Light Resistor
ldr = ADC(0)

def sw(s_id, mt, sw, ldr, cam, dl, t):
    if ticks_diff(ticks_ms(), dl) > 0:
        if s_id == s_id_drm_1 and mt.value():
            cam.on()
            if ldr.read() > ldr_th:
                sw.on()
            dl = ticks_add(ticks_ms(), t)
            get_req('http://{0}:{1}/motion;sensor={2}'.format(ip_server, port_server, s_id))
        elif mt.value():
            sw.on()
            dl = ticks_add(ticks_ms(), t)
            get_req('http://{0}:{1}/motion;sensor={2}'.format(ip_server, port_server, s_id))
        else:
            sw.off()
            if s_id == s_id_drm_1:
                cam.off()
    return dl

# deadlines
dl_sw1 = 0
dl_sw2 = 0
dl_sw3 = 0

sw_mt_d = {s_id_drm_1:[mt1, sw1, dl_sw1, t_sw1],
           s_id_drm_2:[mt2, sw2, dl_sw2, t_sw2],
           s_id_drm_3:[mt3, sw3, dl_sw3, t_sw3]}

while True:
# for _ in range(100):
    for s_id, v in sw_mt_d.items():
        v[2] = sw(s_id, v[0], v[1], ldr, cam, v[2], v[3])

    # Test printouts
    # clear_screen(oled)
    # s = 'sw: {0} {1} {2}'.format(sw1.value(), sw2.value(), sw3.value())
    # m = 'mt: {0} {1} {2} {3}'.format(mt1.value(), mt2.value(), mt3.value(), ldr.read())
    # oled.text(s, 8, 20)
    # oled.text(m, 8, 30)
    # oled.show()

    sleep(0.5)
