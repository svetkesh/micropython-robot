import network, machine, time  #, math
SMALL_TIMEOUT = 200
networkpin = machine.Pin(2, machine.Pin.OUT)
headlight = machine.Pin(16, machine.Pin.OUT)
headlight.on()
networkpin.on()
time.sleep_ms(SMALL_TIMEOUT)
networkpin.off()
headlight.off()
print('DBG: end boot.py')

