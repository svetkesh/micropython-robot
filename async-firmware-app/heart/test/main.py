"""
to load settings:
        http://192.168.4.1/?load=default

0.8.1 -using uasyncio
      suits firmware versions 2018 04 +
0.8.4.7 - save gear factor
.7 for trike/quadro fixed forward move through zero
0.8.6.1 - add smooth switch
"""

try:
    import uasyncio as asyncio
    import machine
    import ure as re
    import ujson as json
    import utime as time
    import urandom as random
    # import sys
    import network
    print('DBG: import micro libraries successful')
except ImportError:
    raise SystemExit

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
if sta_if.active():
    robot_ip = sta_if.ifconfig()[0]
else:
    robot_ip = ap_if.ifconfig()[0]

print('Robot IP robot_ip: {}'. format(robot_ip))

# HTML to send to browsers

html = "HTTP/1.0 200 OK\r\n\r\nI Am Robot\r\n"

# Setup drives
motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
servo_turn_x = machine.PWM(machine.Pin(12), freq=50)

# Setup leds
network_pin = machine.Pin(2, machine.Pin.OUT)
forward_led2 = machine.PWM(machine.Pin(4), freq=50)
left_led7 = machine.PWM(machine.Pin(13), freq=50)
right_led8 = machine.PWM(machine.Pin(15), freq=50)
back_led5 = machine.PWM(machine.Pin(14), freq=50)


cycles = 10000
center = 500
rand_factor = .1
rand_value = round(center * rand_factor)

rgb = [center for x in range(3)]

new_rgb = [random.randint(rand_value*(-1), rand_value) for x in range(3)]

print(rgb, new_rgb)

rgb = [rgb[x]+new_rgb[x] for x in range(3)]
print(rgb)
rgb = [rgb[x] - center for x in range(3)]
print(rgb)
rgb = [round((rgb[x]) * ((center - rand_value)/center)) for x in range(3)]
# rgb = [int(((center-rand_value)/center)*rgb[x]) for x in range(3)]
print(rgb)
rgb = [rgb[x] + center for x in range(3)]
print(rgb)
new_rgb = [random.randint(rand_value*(-1), rand_value) for x in range(3)]
rgb = [rgb[x]+new_rgb[x] for x in range(3)]
print(rgb)
# print(rgb)

for cycle in range(cycles):
    new_rgb = [random.randint(rand_value * (-1), rand_value) for x in range(3)]
    # rgb = [rgb[x] + new_rgb[x] for x in range(3)]
    rgb = [round((rgb[x] - center) * ((center - rand_value)/center)) + center + new_rgb[x] for x in range(3)]
    print(rgb, new_rgb)
    left_led7.duty(rgb[0])
    right_led8.duty(rgb[1])
