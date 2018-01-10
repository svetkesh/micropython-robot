import network, machine, time, math

print('Starting boot.py')

ssid = 't4m'
ssidpss = ''

s_timeout = 200
l_timeout = 2000

networkpin = machine.Pin(2, machine.Pin.OUT)
networkpin.on()
time.sleep_ms(s_timeout)
networkpin.off()
time.sleep_ms(s_timeout)
networkpin.on()
time.sleep_ms(s_timeout)
networkpin.off()
time.sleep_ms(s_timeout)
networkpin.on()
time.sleep_ms(s_timeout)
networkpin.off()
time.sleep_ms(s_timeout)
networkpin.on()
time.sleep_ms(s_timeout)

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

print(ap_if.ifconfig())
print(ssid, ssidpss)

sta_if.active(True)
sta_if.connect(ssid, ssidpss)

time.sleep_ms(l_timeout)
time.sleep_ms(l_timeout)  # 4 s
time.sleep_ms(l_timeout)  # 6 S

print('AP:')
print(ap_if.ifconfig())
print('STATION:')
print(sta_if.ifconfig())

networkpin.off()
