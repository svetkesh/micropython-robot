"""
0.8.1 -using uasyncio
      suits firmware versions 2018 04 +
      this uses custom firmware with added uasyncio


0.8.3.0.15 - added setting reader and writer
             accept JSON

http://192.168.4.1/?&settings={%22runy%22:%2277%22,%22handy%22:%2240%22}&
http://192.168.4.1/?&settings={%22debug%22:%22True%22,%22ssid%22:%22Some%20SSID%22}&
http://192.168.4.1/?&run={%22debug%22:%22True%22,%22ssid%22:%22Some%20SSID%22}&

"""

import uasyncio as asyncio

try:
    import machine
    print('DBG: import "machine" library - done')
except ImportError:
    print('ERR: Could not import "machine" library')

try:
    import ure as re
    print('DBG: import microRE "ure" library successful')
except ImportError:
    try:
        import re
        print('DBG: import standard library RE "re" successful')
    except ImportError:
        print('ERR: import could not be done neither re neither micro "ure"')
        raise SystemExit

try:
    import ujson as json
    print('DBG: import "ujson" library successful')
except ImportError:
    try:
        import json
        print('DBG: import standard library "JSON" successful')
    except ImportError:
        print('ERR: import could not be done neither ujson neither JSON')
        raise SystemExit

# from settingsreader import SettingsReader
# from settingswriter import SettingsWriter

# import utime as time
# import sys

import network

LONG_SLEEP = 3
SHORT_SLEEP = 1
BLINK_SLEEP = 0.3

robot_ip = '192.168.4.1'

sta_if = network.WLAN(network.STA_IF)

# if sta_if.active():
#     print('sta_if: {}, {}, {}'.format(sta_if.active(), type(sta_if.ifconfig()), sta_if.ifconfig()))
#     robot_ip = sta_if.ifconfig()[0]
#     print('robot_ip: {}'. format(robot_ip))

print('Robot IP robot_ip: {}'. format(robot_ip))

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
# start_timer = 0.0  # del
# mean_times = {}                      # store mean time of runnings
# last_commands_servos = {}
# last_commands_dcdrive = {}

# count_robot_listener = 0
# count_handler = 0
# workers = 0

robot_settings = {}
robot_settings_file = 'settings.txt'


def give_up():
    servo_head_x.duty(75)
    servo_hand_y.duty(40)
    networkpin.on()
    motor_a_p.duty(0)
    # print('DBG: # give_up')

# # compile regex
try:
    # # compile re number
    # float_number = re.compile("0\.(\d+)")
    r_number = re.compile("(\d+)")

    # commands
    # r_update_settings = re.compile("settings=(\s+)")
    r_settings = re.compile("settings=({.*})")
    r_run = re.compile("run=({.*})")


except:
    print('ERR: error compiling regex')
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


def robotworkers():
    """test to ensure command passes to robot driver"""
    global workers

    workers += 1
    print('DBG: workers count: {}'.format(workers))
    workers -= 1


def give_up():
    servo_head_x.duty(75)
    servo_hand_y.duty(40)
    networkpin.on()
    motor_a_p.duty(0)
    # print('DBG: # give_up')


def update_settings(settings_to_update=None, file=robot_settings_file):
    # robot_settings = {}
    # robot_settings_file = 'settings.txt'

    global robot_settings

    print('DBG update_settings settings_to_update: {}, {}'.format(type(settings_to_update), settings_to_update))
    print('DBG update_settings robot_settings: {}, {}'.format(type(robot_settings), robot_settings))
    print('DBG update_settings file: {}'.format(file))
    print('DBG update_settings (if settings_to_update): ...')
    print('DBG update_settings (if settings_to_update): {}'.format(True if settings_to_update else False))

    if settings_to_update:
        try:
            write_settings(settings_to_update, file)
            robot_settings = read_settings(file)

            print('DBG robot_settings after upd: {}, {}'.format(type(robot_settings), robot_settings))
        except Exception as e:
            print('Error while updating settings {}, {}'.format(type(e), e))
    else:
        try:
            robot_settings = read_settings(file)
            print('DBG robot_settings read: {}, {}'.format(type(robot_settings), robot_settings))

        except Exception as e:
            print('Error while reading settings {}, {}'.format(type(e), e))


def read_settings(file):
    try:
        print('DBG: read_settings from file:{}'.format(file))
        with open(file, 'r') as f:
            print('DBG file content: {}'.format(f.read()))
            try:
                j = json.load(f)
                print('DBG: j = json.load(f): {}, {}'.format(type(j), str(j)))
                for key in j:
                    print('DBG: key:value of j: {}:{}'.format(key, j[key]))
                return j
            except Exception as e:
                print('ERR loading settings from file: {}, '
                      'json.load(f) {}, {}'.format(file, type(e), e))
                return False
    except Exception as e:
        print('ERR reading file {}, {}'.format(type(e), e))
        return False


def write_settings(j_str, file='settings.txt'):
    try:
        j_str = json.loads(j_str)
        for item in j_str:
            print('DBG: json items: {}:{}'.format(
                item,
                j_str[item]
            ))
        print('DBG: JSON data loaded OK')
    except json.JSONDecodeError as e:
        print(type(e), e)
        print('ERR: given data seems not to be valid JSON:{}'.format(j_str))

    try:
        with open(file, 'w') as f:
            f.write(str(j_str))
        return True
    except Exception as e:
        print('ERR: given data could not be written {}, {}\n    {}'.format(type(e), e, j_str))
        return False


def robot_listener_json(request):
    print('DBG robot_listener_json got: {}'.format(str(request)))
    # robot_listener_json got: b'GET /?&settings={%22debug%22:%22True%22,%22ssid%22:%22Some%20SSID%22}& HTTP/1.1\r\n'
    # from string http://192.168.4.1/?&settings={%22debug%22:%22True%22,%22ssid%22:%22Some%20SSID%22}&

    request = str(request)

    # processing json commands

    if r_run.search(request) is not None:
        try:  # gonna test - try not to search one more time
            formatted_request = request.replace('%22', '\"')
            formatted_request = formatted_request.replace('%20', ' ')
            m_run = r_run.search(formatted_request)

            print('DBG processing json commands in run, request: {}, {}'.format(
                type(request), formatted_request))
            s_run = m_run.group(1)
            print('DBG processing json commands in run, s_run: {}, {}'.format(type(s_run), s_run))

            j_run = json.loads(s_run)
            print('DBG json.loads() commands in run, j_settings: {}, {}'.format(type(j_run), j_run))

            for js_run in j_run:
                print('DBG json.loads() command in run: {}:{}'.format(js_run, j_run[js_run]))

                try:
                    function_to_call = tokens[js_run]
                    function_to_call(j_run[js_run])
                except Exception as e:
                    print('SKIP while dispatching run commands with function_to_call: {}, {}'.format(type(e), e))

        except Exception as e:
            print('Error while processing run json.loads()  {}, {}'.format(type(e), e))

    if r_settings.search(request) is not None:
        try:  # gonna test - try not to search one more time
            formatted_request = request.replace('%22', '\"')
            formatted_request = formatted_request.replace('%20', ' ')
            m_settings = r_settings.search(formatted_request)

            print('DBG processing json commands for settings, request: {}, {}'.format(
                type(request), formatted_request))
            s_settings = m_settings.group(1)
            print('DBG processing json commands, s_settings: {}, {}'.format(type(s_settings), s_settings))

            j_settings = json.loads(s_settings)
            print('DBG json.loads() commands, j_settings: {}, {}'.format(type(j_settings), j_settings))

            update_settings(settings_to_update=j_settings, file=robot_settings_file)
        except Exception as e:
            print('Error while processing settings json.loads()  {}, {}'.format(type(e), e))


def move_servo(servo, duty='77', forward=True, speed=1):

    servo_start_pos = 40
    servo_end_pos = 115
    servo_center_pos = 77

    print('DBG move_servo: {}, duty: {}, forward: {}, speed: {}'
          ''.format(str(servo), duty, forward, speed))

    try:
        duty_int = int(duty)
        if forward:
            servo.duty(duty_int)
        else:
            servo.duty(servo_start_pos + servo_end_pos - duty_int)
    except Exception as e:
        print('Error while move_servo {}, {}'.format(type(e), e))


def headx(key):
    print('DBG runing: {} key: {}'.format('headx', key))


def handy(key):
    print('DBG runing: {} key: {}'.format('handy', key))


def turnx(key):
    print('DBG runing: {} key: {}'.format('turnx', key))


def runy(key):
    print('DBG runing: {} key: {}'.format('runy', key))


def catch(key):
    print('DBG runing: {} key: {}'.format('catch', key))


def gear(key):
    print('DBG runing: {} key: {}'.format('gear', key))


def read_settings(key):
    print('DBG runing: {} key: {}'.format('read_settings', key))


# def update_settings(key):
#     print('DBG runing: {} key: {}'.format('update_settings', key))


tokens = {
    'headx': headx,
    'handy': handy,
    'turnx': turnx,
    'runy': runy,
    'catch': catch,
    'gear': gear,
    'read_settings': read_settings,
    'update_settings': update_settings,
    'give_up': give_up,
}


def _handler(reader, writer):

    # # orig _handler

    # print('DBG _handler: New connection')
    line = yield from reader.readline()
    # print(line)

    # robot_listener(line)  # line is type of bytes
    robot_listener_json(line)  # line is type of bytes
        
    yield from writer.awrite('Gotcha!')
    yield from writer.aclose()

    # # end original _handler


# def run(host="127.0.0.1", port=8081, loop_forever=True, backlog=16): # orig
def run(host="192.168.4.1", port=80, loop_forever=True, backlog=16):
    loop = asyncio.get_event_loop()
    print("* Starting Server at {}:{}".format(host, port))
    loop.create_task(asyncio.start_server(_handler, host, port, backlog=backlog))
    if loop_forever:
        loop.run_forever()
        loop.close()


if __name__ == '__main__':
    # update_settings(settings_to_update=None, file=robot_settings_file)
    run()
