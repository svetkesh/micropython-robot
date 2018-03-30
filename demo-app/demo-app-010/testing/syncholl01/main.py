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

compatable with:
esp8266-20171101-v1.9.3.bin (not bad)
esp8266-20180129-v1.9.3-240-ga275cb0f.bin (somehow...)
esp8266-20180212-v1.9.3-289-g8e1cb58a.bin (+)

incompatable with micropython:
esp8266-20180316-v1.9.3-456-g0db49c37.bin
...
esp8266-20180326-v1.9.3-479-gb63cc1e9.bin

'''
print('DBG: starting main.py')

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

# HTML to send to browsers
# hardcoded ip address html reply

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<br>Robot IP:
""" + robot_ip + """
<br>
</body>
</html>

"""



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

def blink_report(n_blinks):
    networkpin.off()
    time.sleep(SHORT_SLEEP*2)
    for blinks in range (n_blinks):
        networkpin.on()
        time.sleep(BLINK_SLEEP)
        networkpin.off()

try:
    # compile regex
    # compile re number
    r_number = re.compile("0\.(\d+)")
    # # get head position
    r_headx = re.compile("headx=0\.(\d+)")
    # # get hand position
    r_handy = re.compile("handy=0\.(\d+)")  #
    # get body direction turnx
    r_turnx = re.compile("turnx=0\.(\d+)")  #
    # get body speed runy
    r_runy = re.compile("runy=0\.(\d+)")  #
    #  get catch-relase trigger
    r_catch = re.compile("catch=catch")  #
except:
    print('DBG: error compiling regex')
    # blink_report(4)
    # blink_report(4)

# Setup Socket WebServer
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    print('DBG: opened connection to port 80')
    while True:
        networkpin.off()
        print('DBG: hall_sensor.value(): {}, '
              'at : {} '
              'since last loose: {}'.format(hall_sensor.value(),
                                            time.time(),
                                            time.time() - time_loose))  # analogue

        # if time.time() - time_loose > HOLD_LOOSE_TIMEOUT:
        #     # this robot never looses before or looses long ago
        #
        #     ###
        # else:
        #     # this robot just looses game
        #     print('DBG: hall_sensor.value() != 1')
        #     networkpin.on()
        #     break

        if hall_sensor.value() == 1:
            time_loose = time.time()
            networkpin.on()
            print('DBG: hall_sensor.value() != 1')

        #
        # else:
        #     time_loose = time.time()
        #     # robot loses game right now
        #     # time.sleep(1)
        #     # light switch off .. for looser
        #     break

        try:
            # networkpin.on()
            conn, addr = s.accept()
            # print("Got a connection from %s" % str(addr))
            request = conn.recv(1024)
            # print("Content = %s" % str(request))  # print full request
            request = str(request)

            # robot in action!
            if (time.time() - time_loose) > HOLD_LOOSE_TIMEOUT:
                # robot in action!

                # compile re number
                # r_number = re.compile("0\.(\d+)")

                # # get head position
                # r_headx = re.compile("headx=0\.(\d+)")
                m_headx = r_headx.search(request)
                #
                # # get hand position
                # r_handy = re.compile("handy=0\.(\d+)")  #
                m_handy = r_handy.search(request)

                # get body direction turnx
                # r_turnx = re.compile("turnx=0\.(\d+)")  #
                m_turnx = r_turnx.search(request)

                # get body speed runy
                # r_runy = re.compile("runy=0\.(\d+)")  #
                m_runy = r_runy.search(request)

                # get catch-release trigger
                # r_catch = re.compile("catch=catch")  #
                m_catch = r_catch.search(request)

                try:
                    # default values for positions and speed and direction
                    f_headx = 0.5
                    f_handy = 0.5
                    f_turnx = 0.5
                    f_runy = 0.5

                    # selecting only actual commands without defaults values
                    # >>> print('not') if None != re_compiled.search(search_string) else print('yes')
                    # not

                    if r_headx.search(request) is not None:

                        s_headx = str(m_headx.group(0))
                        # print('source string: {}'.format(s_headx))
                        headx = r_number.search(s_headx)
                        # print('  value found: {}'.format(headx.group(0)))
                        f_headx = float(headx.group(0))
                        # print('  float value: {} , value+2 = {} '.format(f_headx, f_headx + 2))  # testing float conv
                        posx = int(f_headx * 75 + 40)
                        servo_head_x.duty(posx)

                        # print('got position from joystick hand x,y : {} , {}\n'
                        #       'got position from joystick run turn : {} \n'
                        #       'direction , speed : {} , {}'.format(posx,
                        #                                            '-',
                        #                                            '-',
                        #                                            '-',
                        #                                            '-'))
                    #
                    if r_handy.search(request) is not None:
                        s_handy = str(m_handy.group(0))
                        # print('source string: {}'.format(s_handy))
                        handy = r_number.search(s_handy)
                        # print('  value found: {}'.format(handy.group(0)))
                        f_handy = 1 - float(handy.group(0))               # inverse Y axis
                        posy = int(f_handy * 75 + 40)
                        servo_hand_y.duty(posy)

                        # print('got position from joystick hand x,y : {} , {}'
                        #       'got position from joystick run turn : {} \n'
                        #       'direction , speed : {} , {}'.format('-',
                        #                                            posy,
                        #                                            '-',
                        #                                            '-',
                        #                                            '-'))

                    if r_turnx.search(request) is not None:
                        s_turnx = str(m_turnx.group(0))
                        # print('source string: {}'.format(s_turnx))
                        turnx = r_number.search(s_turnx)
                        # print('  value found: {}'.format(turnx.group(0)))
                        f_turnx = float(turnx.group(0))
                        directionx = int(f_turnx * 75 + 40)
                        servo_direction.duty(directionx)

                        # print('got position from joystick hand x,y : {} , {}'
                        #       'got position from joystick run turn : {} \n'
                        #       'direction , speed : {} , {}'.format('-',
                        #                                            '-',
                        #                                            directionx,
                        #                                            '-',
                        #                                            '-'))

                    if r_runy.search(request) is not None:
                        s_runy = str(m_runy.group(0))
                        # print('source string: {}'.format(s_runy))
                        runy = r_number.search(s_runy)
                        # print('  value found: {}'.format(runy.group(0)))
                        f_runy = float(runy.group(0))

                        if f_runy < 0.5:
                            m_duty = -1
                        else:
                            m_duty = 1

                        p_duty = int(abs(f_runy * 3000) - 1500)

                        # print('got position from joystick hand x,y : {} , {}'
                        #       'got position from joystick run turn : {} \n'
                        #       'direction , speed : {} , {}'.format('-',
                        #                                            '-',
                        #                                            '-',
                        #                                            m_duty,
                        #                                            p_duty))
                        motor_a_p.duty(p_duty)
                        motor_a_m.duty(m_duty)
                        # networkpin.off()

                    if r_catch.search(request) is not None:
                        # print('DBG servo_catch.duty() : {}'.format(
                        #     servo_catch.duty()))

                        if servo_catch.duty() < 75:
                            servo_catch.duty(110)
                        else:
                            servo_catch.duty(40)
                        # time.sleep(0.05)

                except Exception as e:
                    print('Error searching exact values in received command , {}'.format(type(e), e))
                    # blink_report(5)
                    # blink_report(5)

                # networkpin.off()

                response = html
                conn.send(response)
                conn.close()
            else:
                # loose actions give up!
                servo_head_x.duty(75)
                servo_hand_y.duty(40)
                networkpin.on()
                conn.close()

        except Exception as e:
            print('ERR: Catch Exception while processing requests: {} , {}'.format(type(e), e))
            print('DBG: about to reset in few seconds')
            # blink_report(6)
            # blink_report(6)
            # networkpin.off()
            #
            # utime.sleep(LONG_SLEEP)
            #
            time.sleep(SHORT_SLEEP)
            # # hard reset
            # machine.reset()
            # soft reset
            sys.exit()


except Exception as e:
    print('ERR: Catch Exception with running Web server: {} , {}'.format(type(e), e))
    # blink_report(7)
    # blink_report(7)
    # networkpin.off()

    print('DBG: about to reset in few seconds')
    # blink_report(6)
    # blink_report(6)
    # networkpin.off()
    #
    # utime.sleep(LONG_SLEEP)
    #
    time.sleep(SHORT_SLEEP)
    # # hard reset
    machine.reset()
    # soft reset
    # sys.exit()

