
import socket
try:
    import machine
    print('DBG: import "machine" library - done')
except ImportError:
    print('DBG: Could not import "machine" library')

try:
    import ure as re
    print('DBG: import microRE "ure" library successful')
except ImportError:
    try:
        import re
        print('DBG: import standard library RE "re" successful')
    except ImportError:
        print('DBG: import could not be done neither re neither micro "ure"')
        raise SystemExit
import utime as time
import sys

import network


LONG_SLEEP = 3
SHORT_SLEEP = 1
BLINK_SLEEP = 0.3
BLACKOUT = 0
HOLD_LOOSE_TIMEOUT = 5

time_loose = 0


robot_ip = '192.168.4.1'

sta_if = network.WLAN(network.STA_IF)

# if sta_if.active():
#     print('sta_if: {}, {}, {}'.format(sta_if.active(), type(sta_if.ifconfig()), sta_if.ifconfig()))
#     robot_ip = sta_if.ifconfig()[0]
#     print('robot_ip : {}'. format(robot_ip))

print('Robot IP robot_ip : {}'. format(robot_ip))
#
# # HTML to send to browsers
# # hardcoded ip address html reply
#
# html = """<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Title</title>
# </head>
# <body>
# <br>Robot IP:
# """ + robot_ip + """
# <br>
# </body>
# </html>
#
# """



# Setup drives
# LE0 = machine.Pin(0, machine.Pin.OUT)
# LED2 = machine.Pin(2, machine.Pin.OUT)
motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
motor_a_p.duty(p_duty)
motor_a_m.duty(m_duty)