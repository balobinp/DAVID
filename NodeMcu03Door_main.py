# Actions:

version = 200803

# Switches

sw1 = Pin(16, Pin.OUT) # D0 Out of the door
sw1.off()
sw1.on()

sw2 = Pin(0, Pin.OUT) # D3 Between the doors
sw2.off()
sw2.on()

sw3 = Pin(2, Pin.OUT) # D4 Inside
sw3.off()
sw3.on()

# Motion sensors

mt1 = Pin(12, Pin.IN) # D6 Out of the door
mt1.value()

mt2 = Pin(13, Pin.IN) # D7 Between the doors
mt2.value()

mt3 = Pin(15, Pin.IN) # D8 Inside
mt3.value()

# Camera control

cam = Pin(14, Pin.OUT) # D5
cam.off()
cam.on()

# Light Resistor

ldr = ADC(0)
ldr.read()

#while True:
for _ in range(1):

    pass
