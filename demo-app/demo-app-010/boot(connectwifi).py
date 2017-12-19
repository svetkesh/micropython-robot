import network, machine
import time, math

print('Starting boot.py')

ssid = 't4m'
ssidpss = 'zamaha402'

s_timeout = 200
l_timeout = 2000


networkpin = machine.Pin(2, machine.Pin.OUT)
networkpin.on()

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

time.sleep_ms(s_timeout)

sta_if.active(True)
sta_if.connect(ssid, ssidpss)

time.sleep_ms(l_timeout)

if sta_if.isconnected():
    networkpin.off()
    print('Network connected')
else:
    time.sleep_ms(s_timeout)
    networkpin.off()
    time.sleep_ms(s_timeout)
    networkpin.on()
    time.sleep_ms(s_timeout)
    networkpin.off()
    time.sleep_ms(s_timeout)
    networkpin.on()
    print('not connected to wifi, opening AP')
    time.sleep_ms(l_timeout)
    sta_if.active(False)
    time.sleep_ms(l_timeout)
    ap_if.active(True)
    time.sleep_ms(l_timeout)

    if ap_if.isconnected():
        networkpin.off()
        print('AP connected')

print('End boot.py')
