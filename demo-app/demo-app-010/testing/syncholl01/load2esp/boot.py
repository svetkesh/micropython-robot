import network, machine, time  #, math
SMALL_TIMEOUT = 200
networkpin = machine.Pin(2, machine.Pin.OUT)
networkpin.on()
time.sleep_ms(SMALL_TIMEOUT)
networkpin.off()
print('DBG: end boot.py')

