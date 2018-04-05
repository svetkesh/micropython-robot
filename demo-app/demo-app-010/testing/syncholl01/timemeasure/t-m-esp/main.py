'''
This is main.py for running on ESP8266 MicroPython

Handles request of type:

http://192.168.101.102/?headx=0.5&handy=0.5&turnx=0.5&runy=0.5

Not requires all
 headx, handy, turnx, runy

regex pattern:
import ure
rh = re.compile("headx=0\.(\d+)")

# >>> print('not') if None != rh.search(s) else print('yes')
# not
print('not') if None != rh.search(not_s) else print('yes')
yes

ver 0.7.9.1 - accepting separate commands
0.7.9.1 - version for RoboHand 0.7.9.1

ver 0.7.9.1 + minor fix for y axis for hand - joystick

ver 0.7.9.3 reply html with current IP
ver 0.7.9.4 add catch (catch-release is working)
ver 0.7.9.7 -dev variant of (0.7.9.4) - preparation for exhibition version (0.7.9.8)
ver 0.7.9.8 - exhibition version, disabled wifi station, just access point
ver 0.7.9.8h01 - exhibition version, added Hall
ver 0.7.9.8h01usocket with usocket
ver 0.7.9.8h01usocket with usocket, speed boot adapted , and inverse turn X axis


compatable with:
esp8266-20171101-v1.9.3.bin (not bad)
esp8266-20180129-v1.9.3-240-ga275cb0f.bin (somehow...)
esp8266-20180212-v1.9.3-289-g8e1cb58a.bin (+)

incompatable with micropython:
esp8266-20180316-v1.9.3-456-g0db49c37.bin
...
esp8266-20180326-v1.9.3-479-gb63cc1e9.bin

'''

import sys, machine, network
import utime as time
import ure as re
try:
    import usocket as socket
except ImportError:
    import socket

# from machine import webrepl

LONG_SLEEP = 3
SHORT_SLEEP = 1
BLINK_SLEEP = 0.3
BLACKOUT = 0
HOLD_LOOSE_TIMEOUT = 5
time_loose = 0
robot_ip = '192.168.4.1'

sta_if = network.WLAN(network.STA_IF)

html_ok = """<html><body>OK</body></html>"""


# Setup drives
# LE0 = machine.Pin(0, machine.Pin.OUT)
# LED2 = machine.Pin(2, machine.Pin.OUT)
motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
servo_direction = machine.PWM(machine.Pin(12), freq=50)
servo_head_x = machine.PWM(machine.Pin(14), freq=50)
servo_hand_y = machine.PWM(machine.Pin(13), freq=50)
servo_catch = machine.PWM(machine.Pin(15), freq=50)

hall_sensor = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

networkpin = machine.Pin(2, machine.Pin.OUT)
networkpin.off()

n_factor = 100
n_probes = n_factor * 1000
tiks_factor = 1000
ms_factor = 1000

print('DBG: start measuring')

try:
    start_timer = time.ticks_ms()
    for i in range(0, n_probes):
        pass
    print(time.ticks_ms())
except Exception as e:
    print('EXC: type: {},\n exception: {}\n '.format(type(e), str(e)))
finally:
    print('MSG for command {}\n'
          'cycles {}\n'
          'run in {} s\n'
          'meantime: {} ms\n'.format('pass',
                                     i + 1,
                                     time.ticks_diff(time.ticks_ms(), start_timer) / tiks_factor,
                                     ms_factor * time.ticks_diff(time.ticks_ms(), start_timer)/((i + 1) * tiks_factor)))

#

try:
    start_timer = time.ticks_ms()
    for i in range(0, n_probes):
        hall_sensor.value()
    print(time.ticks_ms())
except Exception as e:
    print('EXC: type: {},\n exception: {}\n '.format(type(e), str(e)))
finally:
    print('MSG for command {}\n'
          'cycles {}\n'
          'run in {} s\n'
          'meantime: {} ms\n'.format('pass',
                                     i + 1,
                                     time.ticks_diff(time.ticks_ms(), start_timer) / tiks_factor,
                                     ms_factor * time.ticks_diff(time.ticks_ms(), start_timer)/((i + 1) * tiks_factor)))

#


print('DBG: end measuring')



####
#
# try:
#     # compile regex
#     # compile re number
#     r_number = re.compile("0\.(\d+)")
#     # # get head position
#     r_headx = re.compile("headx=0\.(\d+)")
#     # # get hand position
#     r_handy = re.compile("handy=0\.(\d+)")  #
#     # get body direction turnx
#     r_turnx = re.compile("turnx=0\.(\d+)")  #
#     # get body speed runy
#     r_runy = re.compile("runy=0\.(\d+)")  #
#     #  get catch-relase trigger
#     r_catch = re.compile("catch=catch")  #
# except:
#     print('DBG: error compiling regex')
#
# # Setup Socket WebServer
# try:
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(('', 80))
#     s.listen(5)
#     while True:
#         if hall_sensor.value() == 1:
#             time_loose = time.time()
#             networkpin.on()
#         try:
#             conn, addr = s.accept()
#             request = conn.recv(64)
#             request = str(request)
#             # robot in action!
#             if (time.time() - time_loose) > HOLD_LOOSE_TIMEOUT:
#                 # robot in action!
#
#                 # compile re number
#                 # r_number = re.compile("0\.(\d+)")
#
#                 # # get head position
#                 m_headx = r_headx.search(request)
#                 # # get hand position
#                 m_handy = r_handy.search(request)
#                 # get body direction turnx
#                 m_turnx = r_turnx.search(request)
#                 # get body speed runy
#                 m_runy = r_runy.search(request)
#                 # get catch-release trigger
#                 m_catch = r_catch.search(request)
#
#                 try:
#                     # default values for positions and speed and direction
#                     f_headx = 0.5
#                     f_handy = 0.5
#                     f_turnx = 0.5
#                     f_runy = 0.5
#
#                     if r_headx.search(request) is not None:
#                         s_headx = str(m_headx.group(0))
#                         headx = r_number.search(s_headx)
#                         f_headx = float(headx.group(0))
#                         posx = int(f_headx * 75 + 40)
#                         servo_head_x.duty(posx)
#
#                     if r_handy.search(request) is not None:
#                         s_handy = str(m_handy.group(0))
#                         handy = r_number.search(s_handy)
#                         f_handy = 1 - float(handy.group(0))               # inverse hand Y axis
#                         posy = int(f_handy * 75 + 40)
#                         servo_hand_y.duty(posy)
#
#                     if r_turnx.search(request) is not None:
#                         s_turnx = str(m_turnx.group(0))
#                         turnx = r_number.search(s_turnx)
#                         f_turnx =  1 - float(turnx.group(0))               # inverse turn X axis
#                         directionx = int(f_turnx * 75 + 40)
#                         servo_direction.duty(directionx)
#
#                     if r_runy.search(request) is not None:
#                         s_runy = str(m_runy.group(0))
#                         runy = r_number.search(s_runy)
#                         f_runy = float(runy.group(0))
#
#                         if f_runy < 0.5:
#                             m_duty = -1
#                         else:
#                             m_duty = 1
#
#                         p_duty = int(abs(f_runy * 3000) - 1500)
#                         motor_a_p.duty(p_duty)
#                         motor_a_m.duty(m_duty)
#                         # networkpin.off()
#
#                     if r_catch.search(request) is not None:
#                         if servo_catch.duty() < 75:
#                             servo_catch.duty(110)
#                         else:
#                             servo_catch.duty(40)
#
#                 except Exception as e:
#                     print('Error searching exact values in received command , {}'.format(type(e), e))
#                 response = html_ok
#                 conn.send(response)
#                 conn.close()
#             else:
#                 # loose actions give up!
#                 servo_head_x.duty(75)
#                 servo_hand_y.duty(40)
#                 networkpin.on()
#                 conn.close()
#
#         except Exception as e:
#             print('ERR: Catch Exception while processing requests: {} , {}'.format(type(e), e))
#             print('DBG: about to reset in few seconds')
#             # # hard reset
#             # machine.reset()
#             # soft reset
#             sys.exit()
#
# except Exception as e:
#     print('ERR: Catch Exception with running Web server: {} , {}'.format(type(e), e))
#     machine.reset()
#     # soft reset
#     # sys.exit()
#
####
####


