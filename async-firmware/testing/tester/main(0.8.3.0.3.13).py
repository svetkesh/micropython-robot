"""
0.8.1 -using uasyncio
      suits firmware versions 2018 04 +
      this uses custom firmware with added uasyncio

0.8.3.0.8 operates integers only
0.8.3.0.3.9 - added listener for gear lever


re notes:
----------------------------------------------------------------
r_number = re.compile("(\d+)")
r_headx = re.compile("headx=(\d+)")

request='http://192.168.4.1/?turnx=77&headx=71&runy=72&handy=73&'
print(request)

m_headx = r_headx.search(request)
print(m_headx)

s_headx = str(m_headx.group(0))
print(s_headx)

headx = r_number.search(s_headx)
print(headx)

f_headx = int(headx.group(0))
print(f_headx)

>>> r_number = re.compile("(\d+)")
>>> r_headx = re.compile("headx=(\d+)")
>>>
>>> request='http://192.168.4.1/?turnx=77&headx=71&runy=72&handy=73&'
>>> print(request)
http://192.168.4.1/?turnx=77&headx=71&runy=72&handy=73&
>>>
>>> m_headx = r_headx.search(request)
>>> print(m_headx)
<match num=2>
>>>
>>> s_headx = str(m_headx.group(0))
>>> print(s_headx)
headx=71
>>>
>>> headx = r_number.search(s_headx)
>>> print(headx)
<match num=2>
>>>
>>> f_headx = int(headx.group(0))
>>> print(f_headx)
71

----------------------------------------------------------------

0.8.3.0.11 - added gears forward and backward
0.8.3.0.3.13 debug version of 0.8.3.0.3.11
             eliminating delays
"""

import uasyncio as asyncio


def _handler(reader, writer):
    print('New connection')
    line = yield from reader.readline()
    # print(line)
    # driverobot(line)

    if workers < 4:
        robotlistener(line)
        # robotworkers()
    else:
        print('DBG: workers count: {}'.format(workers))
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

mean_time_robotlistener = 0.0
count_robotlistener = 1

# set game timers
HOLD_LOOSE_TIMEOUT = 5
# time_loose = 0

gear_factor = 3


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

# some debug and stats
start_timer = 0.0
command_counter = 0
# mean_times = {}
last_commands_servos = {}
# last_commands_dcdrive = {}

workers = 0


def give_up():
    servo_head_x.duty(75)
    servo_hand_y.duty(40)
    networkpin.on()
    motor_a_p.duty(0)
    # print('DBG: # give_up')

try:
    # compile regex
    # compile re number
    float_number = re.compile("0\.(\d+)")
    r_number = re.compile("(\d+)")

    # # get head position
    r_headx = re.compile("headx=(\d+)")
    # # get hand position
    r_handy = re.compile("handy=(\d+)")  #
    # get body direction turnx
    r_turnx = re.compile("turnx=(\d+)")  #
    # get body speed runy
    r_runy = re.compile("runy=(\d+)")  #
    #  get catch-relase trigger
    r_catch = re.compile("catch=catch")  #
    #  get gear factor
    r_gear = re.compile("gear=(\d+)")  #
except:
    print('DBG: error compiling regex')
    # blink_report(4)
    # blink_report(4)

def means(m, x=0.0, t=1):
    # previous mean time for x values
    # given x
    # given count

    # print(m, x, t)
    try:
        if t == 0:
            # print('return first value, avoid zero division')
            return x
        elif t < 2:
            # print('return first value')
            return x
        else:
            # print('calculating...')
            return (m * (t-1) + x) / t
    except Exception as e:
        # print('return first value, supress arithmetic errors')
        print('ERR while calculating meaning values {}, {}'.format(type(e), e))
        return x


def robotworkers():  # test to ensure command passes to robot driver
    global workers

    workers += 1
    print('DBG: workers count: {}'.format(workers))
    workers -= 1


def robotlistener(request):  # test to ensure command passes to robot driver

    global motor_a_p
    global motor_a_m
    global servo_direction
    global servo_head_x
    global servo_hand_y
    global servo_catch
    global networkpin

    global html

    global HOLD_LOOSE_TIMEOUT

    global mean_time_robotlistener
    start_robotlistener = time.ticks_ms()
    start_timer = time.ticks_ms()
    global command_counter
    command_counter += 1
    global count_robotlistener

    global gear_factor

    global workers

    workers += 1

    current_commands_servos = {}
    # current_commands_servos_max = 0
    # current_commands_dcdrive = {}
    global last_commands_servos
    # global last_commands_dcdrive

    global mean_times





    time_loose = 0.0  # initial time out since last game loose - hall sensor trigger



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

    # get gear factor gear_factor
    m_gear = r_gear.search(request)


    try:
        if hall_sensor.value() == 1:  # just caught !
            time_loose = time.ticks_ms()
            give_up()
            # print('DBG: # just caught !')
        else:
            if (time.ticks_ms() - time_loose) < HOLD_LOOSE_TIMEOUT:
                pass
                # still give_up
                # print('DBG: # still give_up')
            else:
                # print('DBG: # robot in action!')
                networkpin.off()
                # robot in action!

                try:
                    m_headx = r_headx.search(request)
                    m_handy = r_handy.search(request)
                    m_turnx = r_turnx.search(request)
                    m_runy = r_runy.search(request)
                    m_catch = r_catch.search(request)
                    m_gear = r_gear.search(request)

                except Exception as e:
                    print('Error while regex m_ {}, {}'.format(type(e), e))

                try:

                    if r_gear.search(request) is not None:
                        s_gear = str(m_gear.group(0))
                        gear = r_number.search(s_gear)
                        gear_factor = int(gear.group(0))
                        print('DBG: updated gear_factor: {}'.format(gear_factor))

                    # if r_headx.search(request) is not None:
                    #     s_headx = str(m_headx.group(0))
                    #     headx = r_number.search(s_headx)
                    #     f_headx = float(headx.group(0))
                    #     posx = int(f_headx * 75 + 40)
                    #     servo_head_x.duty(posx)

                    # new in 0.3.0.3.8 with integers only
                    if r_headx.search(request) is not None:
                        s_headx = str(m_headx.group(0))
                        headx = r_number.search(s_headx)
                        posx = int(headx.group(0))
                        servo_head_x.duty(posx)
                        current_commands_servos['posx'] = posx

                    # if r_handy.search(request) is not None:
                    #     s_handy = str(m_handy.group(0))
                    #     handy = r_number.search(s_handy)
                    #     f_handy = 1 - float(handy.group(0))  # inverse Y axis
                    #     posy = int(f_handy * 75 + 40)
                    #     servo_hand_y.duty(posy)

                    # new in 0.3.0.3.8 with integers only
                    if r_handy.search(request) is not None:
                        s_handy = str(m_handy.group(0))
                        handy = r_number.search(s_handy)
                        # f_handy = 1 - float(handy.group(0))  # inverse Y axis
                        posy = 155 - int(handy.group(0))       # inverse Y axis
                        servo_hand_y.duty(posy)
                        current_commands_servos['posy'] = posy

                    # if r_turnx.search(request) is not None:
                    #     s_turnx = str(m_turnx.group(0))
                    #     turnx = r_number.search(s_turnx)
                    #     f_turnx = 1 - float(turnx.group(0))   # inverse Y axis
                    #     directionx = int(f_turnx * 75 + 40)
                    #     servo_direction.duty(directionx)

                        # new in 0.3.0.3.8 with integers only
                    if r_turnx.search(request) is not None:
                        s_turnx = str(m_turnx.group(0))
                        turnx = r_number.search(s_turnx)
                        # f_turnx = 1 - float(turnx.group(0))   # inverse Y axis
                        directionx = 155 - int(turnx.group(0))  # inverse Y axis
                        servo_direction.duty(directionx)
                        current_commands_servos['directionx'] = directionx

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
                        # f_runy = float(runy.group(0))
                        i_runy = int(runy.group(0))
                        # current_commands_dcdrive['i_runy'] = i_runy

                        # pre - 0.8.0.3.8

                        # if f_runy < 0.5:
                        #     # m_duty = -1
                        #     m_duty = -300
                        #     p_duty = int(1000 - 2000 * f_runy)
                        #
                        # elif f_runy == 0.5:
                        #     m_duty = 0
                        #     p_duty = 0
                        # else:
                        #     m_duty = int(f_runy * 1000)
                        #     p_duty = int(f_runy * 1000)

                        # new in 0.3.0.3.8 with integers only
                        if i_runy < 77:
                            # m_duty = -1
                            m_duty = -200
                            m_duty = -70 * gear_factor
                            p_duty = int((924 - 12 * i_runy))

                        elif i_runy == 77:
                            m_duty = 0
                            p_duty = 0
                        else:
                            m_duty = int((i_runy-70) * 5 * gear_factor)
                            p_duty = int((i_runy-70) * 5 * gear_factor)

                        # print('DBG f_runy {}, m_duty {}, p_duty {}'.format(f_runy, m_duty, p_duty))
                        # print('DBG i_runy {}, m_duty {}, p_duty {}'.format(i_runy, m_duty, p_duty))

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
                    print('Error while processing servo and dcdrive commands  {}, {}'.format(type(e), e))


        # html = """<!DOCTYPE html>
        # <html lang="en">
        # mean_time_robotlistener = """ + str(mean_time_robotlistener) + """</html>
        #
        # """

        # for command in current_commands_servos:
        #     current_commands_servos_max = (current_commands_servos_max,
        #                                    last_commands_servos[command] - current_commands_servos[command])

            # last_commands_servos[command] = current_commands_servos[command]

        try:

            robotlistener_time = time.ticks_ms() - start_timer
            # mean_times['robotlistener_time'] = means(mean_times['robotlistener_time'], robotlistener_time, command_counter)
            # mean_times['robotlistener_time'] = means(mean_times['robotlistener_time'], robotlistener_time, command_counter)

            # print('DBG meaning times: {}, speed:{}'.format(mean_times,))
            # print('DBG meaning times: {}, speed:{}'.format(mean_times, # current_commands_servos_max / robotlistener_time))

            print('DBG ms:{}, count_robotlistener: {} , {}'.format(
                  robotlistener_time,
                count_robotlistener,
                current_commands_servos))
        except Exception as e:
            print('Error while processing stats {}, {}'.format(type(e), e))

        count_robotlistener += 1

        workers -= 1

    except Exception as e:
        print('Error while processing command {}, {}'.format(type(e), e))
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


if __name__ == '__main__':
    run()