print('DBG: starting main.py')

# todo: add WDT 1 s

# import socket
import usocket as socket
try:
    import machine
    # print('DBG: import "machine" library - done')
except ImportError:
    pass
    # print('DBG: Could not import "machine" library')

try:
    import ure as re
    # print('DBG: import microRE "ure" library successful')
except ImportError:
    try:
        import re
        # print('DBG: import standard library RE "re" successful')
    except ImportError:
        # print('DBG: import could not be done neither re neither micro "ure"')
        raise SystemExit
import utime as time
# import sys
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

# print('Robot IP robot_ip : {}'. format(robot_ip))

# HTML to send to browsers
html_ok = """OK"""

# Setup drives
motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
servo_direction = machine.PWM(machine.Pin(12), freq=50)
servo_head_x = machine.PWM(machine.Pin(14), freq=50)
servo_hand_y = machine.PWM(machine.Pin(13), freq=50)
servo_catch = machine.PWM(machine.Pin(15), freq=50)
networkpin = machine.Pin(2, machine.Pin.OUT)
headlight = machine.Pin(16, machine.Pin.OUT)
hall_sensor = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
headlight.on()


def give_up():
    servo_head_x.duty(75)
    servo_hand_y.duty(40)
    networkpin.on()
    motor_a_p.duty(0)
    # print('DBG: # give_up')


try:
    # compile re number
    r_number = re.compile("0\.(\d+)")
    r_headx = re.compile("headx=0\.(\d+)")
    r_handy = re.compile("handy=0\.(\d+)")  #
    r_turnx = re.compile("turnx=0\.(\d+)")  #
    r_runy = re.compile("runy=0\.(\d+)")  #
    r_catch = re.compile("catch=catch")  #
except:
    # print('DBG: error compiling regex')
    raise SystemExit

# Setup Socket WebServer
try:
    f_headx = 0.5
    f_handy = 0.5
    f_turnx = 0.5
    f_runy = 0.5

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    # print('DBG: opened connection to port 80')
    s.listen(5)

    while True:
        try:
            conn, addr = s.accept()
            request = conn.recv(64)  # change 1024 - 64
            request = str(request)
            response = html_ok  # change html - html_ok
            conn.send(response)
            conn.close()
        except:
            # print('ERR near conn.recv()')
            # break
            # # hard reset
            machine.reset()
            # soft reset
            # sys.exit()

        try:
            if hall_sensor.value() == 1:  # just caught !
                time_loose = time.time()
                give_up()
                # print('DBG: # just caught !')
            else:
                if (time.time() - time_loose) < HOLD_LOOSE_TIMEOUT:
                    pass
                    # still give_up
                    # print('DBG: # still give_up')
                else:
                    # print('DBG: # robot in action!')
                    networkpin.off()
                    # robot in action!

                    m_headx = r_headx.search(request)
                    m_handy = r_handy.search(request)
                    m_turnx = r_turnx.search(request)
                    m_runy = r_runy.search(request)
                    m_catch = r_catch.search(request)

                    if r_headx.search(request) is not None:

                        s_headx = str(m_headx.group(0))
                        headx = r_number.search(s_headx)
                        f_headx = float(headx.group(0))
                        posx = int(f_headx * 75 + 40)
                        servo_head_x.duty(posx)

                    if r_handy.search(request) is not None:
                        s_handy = str(m_handy.group(0))
                        handy = r_number.search(s_handy)
                        f_handy = 1 - float(handy.group(0))  # inverse Y axis
                        posy = int(f_handy * 75 + 40)
                        servo_hand_y.duty(posy)

                    if r_turnx.search(request) is not None:
                        s_turnx = str(m_turnx.group(0))
                        turnx = r_number.search(s_turnx)
                        f_turnx = float(turnx.group(0))
                        directionx = int(f_turnx * 75 + 40)
                        servo_direction.duty(directionx)

                    if r_runy.search(request) is not None:
                        s_runy = str(m_runy.group(0))
                        runy = r_number.search(s_runy)
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

                    if r_catch.search(request) is not None:
                        # print('DBG servo_catch.duty() : {}'.format(
                        #     servo_catch.duty()))

                        if servo_catch.duty() < 75:
                            servo_catch.duty(110)
                        else:
                            servo_catch.duty(40)

        except Exception as e:
            # print('Error searching exact values in received command , {}'.format(type(e), e))
            # # hard reset
            machine.reset()
            # soft reset
            # sys.exit()

except Exception as e:
    # print('ERR: Catch Exception with running Web server: {} , {}'.format(type(e), e))
    # # hard reset
    machine.reset()
    # soft reset
    # sys.exit()

