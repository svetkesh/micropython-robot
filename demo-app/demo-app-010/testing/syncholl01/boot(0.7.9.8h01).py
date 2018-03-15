'''
Booting params for Robot

ver 0.7.9.4 add catch (catch-release is working)

ver 0.7.9.7 -dev variant of (0.7.9.4) - preparation for exhibition version (0.7.9.8)

ver 0.7.9.8 - exhibition version, disabled wifi station, just access point
ver 0.7.9.8h01 - exhibition version, added Hall
'''

import network, machine, time, math

print('DBG: Starting boot.py')

# #ssid = 'KVN'
# # ssidpss = ''
# ssid = 't4m'
# ssidpss = ''

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

# sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

# print(ap_if.ifconfig())
# print(ssid, ssidpss)

# sta_if.active(True)
# sta_if.connect(ssid, ssidpss)

time.sleep_ms(l_timeout)
# time.sleep_ms(l_timeout)  # 4 s
# time.sleep_ms(l_timeout)  # 6 S

print('AP configuration: {}'.format(ap_if.ifconfig()))
# print('STATION configuration {}:'.format(sta_if.ifconfig()))

networkpin.off()
print('DBG: end boot.py')
