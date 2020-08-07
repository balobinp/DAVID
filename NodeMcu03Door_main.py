# Actions:

version = 200807

ldr_th = 100  # Light Resistor value threshold

# Switches
sw1 = Pin(16, Pin.OUT) # D0 Out of the door
sw2 = Pin(0, Pin.OUT) # D3 Between the doors
sw3 = Pin(2, Pin.OUT) # D4 Inside

# Motion sensors
mt1 = Pin(12, Pin.IN) # D6 Out of the door
mt2 = Pin(13, Pin.IN) # D7 Between the doors
mt3 = Pin(14, Pin.IN) # D5 Inside

# Camera control
cam = Pin(15, Pin.OUT) # D8

# Light Resistor
ldr = ADC(0)
ldr.read()

sw_mt_d = {1:[mt1, sw1], 2:[mt2, sw2], 3:[mt3, sw3]}

def sw(s_id, mt, sw, ldr, cam):
    if s_id == 1 and mt.value():
        if ldr.read() > ldr_th:
            sw.on()
            cam.on()
            get_req('http://{0}:{1}/motion;sensor={2}'.format(ip_server, port_server, s_id))
    elif mt_val:
        sw.on()
        get_req('http://{0}:{1}/motion;sensor={2}'.format(ip_server, port_server, s_id))

# while True:
for _ in range(1):
    
    for s_id, mt_sw in sw_mt_d.items():
        sw(s_id, mt_sw[0], mt_sw[1], ldr, cam)
