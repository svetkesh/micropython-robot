import network, machine, time, math
import ujson

print('Starting boot(try to store wifi).py')

# ssid = 'KVN'
# ssidpss = 'cccccccc'
ssid = ''
ssidpss = ''

try:
    # with open('config.txt') as config_file:
    #     config_text = config_file.read()
    #     config_parced = ujson.loads(config_text)
    #     ssid = config_parced['ssid']
    #     ssidpss = config_parced['ssidpss']
    file = open('config.txt')
    text = file.read()
    config_parced = ujson.loads(text)
    ssid = config_parced['ssid']
    print('DBG got SSID {}'.format(ssid))
    ssidpss = config_parced['ssidpss']
    print('DBG got ssidpss {}'.format(ssidpss))

except:
    print('DBG error reading settings')


# >>> file = open('config.txt')
# >>> text = file.read()
# >>> text
# '{"ssid":"KVN","ssidpss":"cccccccc","trick":"demo"}'
# >>> parced = ujson.loads(text)
# >>> parced
# {'ssid': 'KVN', 'ssidpss': 'cccccccc', 'trick': 'demo'}
# >>> parced['ssid']


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
