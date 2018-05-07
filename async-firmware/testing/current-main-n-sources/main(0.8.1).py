import uasyncio as asyncio


def _handler(reader, writer):
    print('New connection')
    line = yield from reader.readline()
    # print(line)
    # driverobot(line)
    robotlistener(line)
    yield from writer.awrite('Gotcha!')
    yield from writer.aclose()


# def run(host="127.0.0.1", port=8081, loop_forever=True, backlog=16): # orig
def run(host="192.168.4.1", port=80, loop_forever=True, backlog=16):
    loop = asyncio.get_event_loop()
    print("* Starting Server at {}:{}".format(host, port))
    loop.create_task(asyncio.start_server(_handler, host, port, backlog=backlog))
    if loop_forever:
        loop.run_forever()
        loop.close()


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
ok
</html>

"""

# set game timers
HOLD_LOOSE_TIMEOUT = 5
# time_loose = 0


# Setup drives
motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
servo_direction = machine.PWM(machine.Pin(12), freq=50)
servo_head_x = machine.PWM(machine.Pin(14), freq=50)
servo_hand_y = machine.PWM(machine.Pin(13), freq=50)
servo_catch = machine.PWM(machine.Pin(15), freq=50)
networkpin = machine.Pin(2, machine.Pin.OUT)
# headlight = machine.Pin(16, machine.Pin.OUT)
hall_sensor = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)


def give_up():
    servo_head_x.duty(75)
    servo_hand_y.duty(40)
    networkpin.on()
    motor_a_p.duty(0)
    # print('DBG: # give_up')

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


def robotlistener(request):  # test to ensure command passes to robot driver

    global motor_a_p
    global motor_a_m
    global servo_direction
    global servo_head_x
    global servo_hand_y
    global servo_catch
    global networkpin

    global HOLD_LOOSE_TIMEOUT

    time_loose = 0  # initial time out since last game loose - hall sensor trigger

    request = str(request)
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
    # m_catch = r_catch.search(request)    # for future catch manipulation
    # m_catch = r_catch.search(request)    # just catch is boolean "catch-release"

    # try:
    #     print('robot gets this: {}\n{}\n{}\n{}\n{}\n{}'.format(request,
    #                                                        m_headx,
    #                                                        m_handy,
    #                                                        m_turnx,
    #                                                        m_runy,
    #                                                        m_catch))
    # except:
    #     print('robot gets request: {}'.format(request))

    # this is seems to be running OK (v01)

    # try:
    #     if r_headx.search(request) is not None:
    #         s_headx = str(m_headx.group(0))
    #         # print('source string: {}'.format(s_headx))
    #         headx = r_number.search(s_headx)
    #         # print('  value found: {}'.format(headx.group(0)))
    #         f_headx = float(headx.group(0))
    #         # print('  float value: {} , value+2 = {} '.format(f_headx, f_headx + 2))  # testing float conv
    #         posx = int(f_headx * 75 + 40)
    #         servo_head_x.duty(posx)
    #         print('DBG processing request for servo_head_x posx {}'.format(posx))
    #
    #     if r_headx.search(request) is not None:
    #         s_headx = str(m_headx.group(0))
    #         # print('source string: {}'.format(s_headx))
    #         headx = r_number.search(s_headx)
    #         # print('  value found: {}'.format(headx.group(0)))
    #         f_headx = float(headx.group(0))
    #         # print('  float value: {} , value+2 = {} '.format(f_headx, f_headx + 2))  # testing float conv
    #         posx = int(f_headx * 75 + 40)
    #         servo_head_x.duty(posx)
    #
    #         # print('got position from joystick hand x,y : {} , {}\n'
    #         #       'got position from joystick run turn : {} \n'
    #         #       'direction , speed : {} , {}'.format(posx,
    #         #                                            '-',
    #         #                                            '-',
    #         #                                            '-',
    #         #                                            '-'))
    #     #
    #     if r_handy.search(request) is not None:
    #         s_handy = str(m_handy.group(0))
    #         # print('source string: {}'.format(s_handy))
    #         handy = r_number.search(s_handy)
    #         # print('  value found: {}'.format(handy.group(0)))
    #         f_handy = 1 - float(handy.group(0))  # inverse Y axis
    #         posy = int(f_handy * 75 + 40)
    #         servo_hand_y.duty(posy)
    #
    #         # print('got position from joystick hand x,y : {} , {}'
    #         #       'got position from joystick run turn : {} \n'
    #         #       'direction , speed : {} , {}'.format('-',
    #         #                                            posy,
    #         #                                            '-',
    #         #                                            '-',
    #         #                                            '-'))
    #
    #     if r_turnx.search(request) is not None:
    #         s_turnx = str(m_turnx.group(0))
    #         # print('source string: {}'.format(s_turnx))
    #         turnx = r_number.search(s_turnx)
    #         # print('  value found: {}'.format(turnx.group(0)))
    #         f_turnx = float(turnx.group(0))
    #         directionx = int(f_turnx * 75 + 40)
    #         servo_direction.duty(directionx)
    #
    #         # print('got position from joystick hand x,y : {} , {}'
    #         #       'got position from joystick run turn : {} \n'
    #         #       'direction , speed : {} , {}'.format('-',
    #         #                                            '-',
    #         #                                            directionx,
    #         #                                            '-',
    #         #                                            '-'))
    #
    #     if r_runy.search(request) is not None:
    #         s_runy = str(m_runy.group(0))
    #         # print('source string: {}'.format(s_runy))
    #         runy = r_number.search(s_runy)
    #         # print('  value found: {}'.format(runy.group(0)))
    #         f_runy = float(runy.group(0))
    #
    #         if f_runy < 0.5:
    #             m_duty = -1
    #         else:
    #             m_duty = 1
    #
    #         p_duty = int(abs(f_runy * 3000) - 1500)
    #
    #         # print('got position from joystick hand x,y : {} , {}'
    #         #       'got position from joystick run turn : {} \n'
    #         #       'direction , speed : {} , {}'.format('-',
    #         #                                            '-',
    #         #                                            '-',
    #         #                                            m_duty,
    #         #                                            p_duty))
    #         motor_a_p.duty(p_duty)
    #         motor_a_m.duty(m_duty)
    #         # networkpin.off()
    #
    #     if r_catch.search(request) is not None:  # just catch is boolean "catch-release"
    #         # print('DBG servo_catch.duty() : {}'.format(
    #         #     servo_catch.duty()))
    #
    #         if servo_catch.duty() < 75:
    #             servo_catch.duty(110)
    #         else:
    #             servo_catch.duty(40)
    #         # time.sleep(0.05)
    # except:
    #     print('ERR processing request for servo_head_x')
    # end (v01)

    # (v01.9) add Hall sensor
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
                    f_turnx = 1 - float(turnx.group(0))   # inverse Y axis
                    directionx = int(f_turnx * 75 + 40)
                    servo_direction.duty(directionx)

                # if r_runy.search(request) is not None:
                #     s_runy = str(m_runy.group(0))
                #     runy = r_number.search(s_runy)
                #     f_runy = float(runy.group(0))
                #
                #     if f_runy < 0.5:
                #         m_duty = -1
                #     else:
                #         m_duty = 1
                #
                #     p_duty = int(abs(f_runy * 3000) - 1500)
                #
                #     # print('got position from joystick hand x,y : {} , {}'
                #     #       'got position from joystick run turn : {} \n'
                #     #       'direction , speed : {} , {}'.format('-',
                #     #                                            '-',
                #     #                                            '-',
                #     #                                            m_duty,
                #     #                                            p_duty))
                #     motor_a_p.duty(p_duty)
                #     motor_a_m.duty(m_duty)

                # for firmware dated after 2018-04-xx

                if r_runy.search(request) is not None:
                    s_runy = str(m_runy.group(0))
                    runy = r_number.search(s_runy)
                    f_runy = float(runy.group(0))

                    if f_runy < 0.5:
                        # m_duty = -1
                        m_duty = -300
                        p_duty = int(1000 - 2000 * f_runy)

                    elif f_runy == 0.5:
                        m_duty = 0
                        p_duty = 0
                    else:
                        m_duty = int(f_runy * 1000)
                        p_duty = int(f_runy * 1000)

                    # print('DBG f_runy {}, m_duty {}, p_duty {}'.format(f_runy, m_duty, p_duty))

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


def give_up():
    servo_head_x.duty(75)
    servo_hand_y.duty(40)
    networkpin.on()
    motor_a_p.duty(0)
    # print('DBG: # give_up')


def driverobot(request):
    try:
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.bind(('', 80))
        # s.listen(5)
        # print('DBG: opened connection to port 80')
        while True:
            try:
                # # networkpin.on()
                # conn, addr = s.accept()
                # # print("Got a connection from %s" % str(addr))
                # request = conn.recv(1024)
                # # print("Content = %s" % str(request))  # print full request
                request = str(request)

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

                # response = html
                # conn.send(response)
                # conn.close()
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
                # sys.exit()
                pass
    finally:
        pass

if __name__ == '__main__':
    run()