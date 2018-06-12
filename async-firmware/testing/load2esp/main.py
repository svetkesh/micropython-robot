"""
0.8.1 -using uasyncio
      suits firmware versions 2018 04 +
0.8.4.1 - uses JSON for commands and settings
0.8.4.3 - added settings listeners

"""

try:
    import uasyncio as asyncio
    import machine
    import ure as re
    import ujson as json
    import utime as time
    import sys
    import network
    print('DBG: import microlibs libraries successful')
except ImportError:
    raise SystemExit

LONG_SLEEP = 3
SHORT_SLEEP = 1
BLINK_SLEEP = 0.3

robot_ip = '192.168.4.1'

sta_if = network.WLAN(network.STA_IF)

if sta_if.active():
    print('sta_if: {}, {}, {}'.format(sta_if.active(), type(sta_if.ifconfig()), sta_if.ifconfig()))
    robot_ip = sta_if.ifconfig()[0]
    print('robot_ip: {}'. format(robot_ip))

print('Robot IP robot_ip: {}'. format(robot_ip))

# HTML to send to browsers
# hardcoded ip address html reply

html = "HTTP/1.0 200 OK\r\n\r\nI Am Robot not Groot\r\n"

# Setup drives
motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
servo_turn_x = machine.PWM(machine.Pin(12), freq=50)
servo_head_x = machine.PWM(machine.Pin(14), freq=50)
servo_hand_y = machine.PWM(machine.Pin(13), freq=50)
servo_catch = machine.PWM(machine.Pin(15), freq=50)
network_pin = machine.Pin(2, machine.Pin.OUT)
# headlight = machine.Pin(16, machine.Pin.OUT)
hall_sensor = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)


robot_settings = {}
robot_settings_file = 'settings.txt'
robot_default_settings_file = 'defsett.txt'

# robot_settings_defaults = {
#     'DEBUG_ENABLE': True,
#     'robot_ip': '192.168.4.1',
#     'servo_min': 40,
#     'servo_max': 115,
#     'servo_center': 77,
#     'gear_factor': 5,
#     'HOLD_LOOSE_TIMEOUT': 5,
# }

robot_busy = False

# # compile regex
# # compile re number
# float_number = re.compile("0\.(\d+)")
# r_number = re.compile("(\d+)")

# compile regex for commands
r_settings = re.compile("settings=({.*})")
r_run = re.compile("run=({.*})")
r_load_default = re.compile("load=default")
r_reset = re.compile("reset=reset")


def give_up():
    servo_head_x.duty(75)
    servo_hand_y.duty(40)
    network_pin.on()
    motor_a_p.duty(0)
    # print('DBG: # give_up')


def move_servo(servo, duty='77', forward=True, speed=1):
    # servo_start_pos = robot_settings['servo_min']
    # servo_end_pos = robot_settings['servo_max']
    # servo_center_pos = robot_settings['servo_center']

    servo_start_pos = robot_settings['servo_min']
    servo_end_pos = robot_settings['servo_max']
    servo_center_pos = robot_settings['servo_center']

    print('DBG move_servo: {}, duty: {}, forward: {}, speed: {}'
          ''.format(str(servo), str(duty), str(forward), str(speed)))

    try:
        duty_int = int(duty)
        if forward:
            servo.duty(duty_int)
        else:
            servo.duty(servo_start_pos + servo_end_pos - duty_int)
    except Exception as e:
        print('Error while move_servo {}, {}'.format(type(e), e))


def headx(key):  # straight
    move_servo(servo_head_x, duty=key)


def handy(key):  # inverted
    move_servo(servo_hand_y, duty=key, forward=False)


def turnx(key):  # inverted
    move_servo(servo_turn_x, duty=key, forward=False)


def runy(key):  # straight
    try:
        i_runy = int(key)

        if i_runy < 77:
            m_duty = -70 * robot_settings['gear_factor']
            p_duty = int((924 - 12 * i_runy))

        elif i_runy == 77:
            m_duty = 0
            p_duty = 0
        else:
            m_duty = int((i_runy - 70) * 5 * robot_settings['gear_factor'])
            p_duty = int((i_runy - 70) * 5 * robot_settings['gear_factor'])

        motor_a_p.duty(p_duty)
        motor_a_m.duty(m_duty)
    except Exception as e:
        print('Error while processing runy: {}, {}'.format(type(e), e))


def catch(key):
    if servo_catch.duty() < 75:
        servo_catch.duty(110)
    else:
        servo_catch.duty(40)


def gear(key):
    print('DBG runing: {} key: {}'.format('gear', key))


def read_settings(file):
    try:
        with open(file, 'r') as f:
            j = json.load(f)
            print('DBG read_settings seems to be OK')
            return j
    except Exception as e:
        print('ERR read_settings from file: {}, '
              ' {}, {}'.format(file, type(e), e))
        return False


def write_settings(j, file='settings.txt'):
    try:
        for item in j:
            print('DBG: json items: {}:{}'.format(item, j[item]))

        j_str = json.dumps(j)
        print('DBG: JSON data loaded OK')
    except json.JSONDecodeError as e:
        print(type(e), e)
        print('ERR: data not valid JSON:{}'.format(str(j)))

    try:
        with open(file, 'w') as f:
            f.write(str(j_str))
            print('DBG: data: {} written to: {}, OK'.format(file, j_str))
        return True
    except Exception as e:
        print('ERR: given data could not be written {}, {}\n    {}'.format(type(e), e, j_str))
        return False


def update_settings(settings_to_update=None, file=robot_settings_file):
    global robot_settings
    if settings_to_update:
        try:
            for item in settings_to_update:
                try:
                    print('DBG update_settings {} -> {}'.format(
                        robot_settings[item],
                        settings_to_update[item]
                    ))
                except Exception as e:
                    print('ERR-DBG update_settings for: "{}": "{}" '
                          ' {}, {}'.format(item, settings_to_update[item], type(e), e))

                robot_settings[item] = settings_to_update[item]

            write_settings(robot_settings, file)
            return True

            # write_settings(settings_to_update, file)
            # robot_settings = {}
            # robot_settings = read_settings(file)

            print('DBG robot_settings after upd: {}, {}'.format(type(robot_settings), robot_settings))
        except Exception as e:
            print('Error while updating settings {}, {}'.format(type(e), e)) # return  what ???
            return False
    else:
        try:
            # robot_settings = read_settings(file)
            print('DBG robot_settings nothing to update, '
                  'current settings: {}, {}'.format(type(robot_settings),
                                                    robot_settings))
            return True

        except Exception as e:
            print('Error while reading settings {}, {}'.format(type(e), e))  # return  what ???
            return False


def robot_listener_json(request):
    global robot_settings
    global robot_busy
    robot_busy = True
    global html
    start = time.ticks_ms()
    print('DBG robot_listener_json got: {}'.format(str(request)[:120]))

    request = str(request)[:128]
    formatted_request = request.replace('%22', '\"')
    formatted_request = formatted_request.replace('%27', '\"')
    formatted_request = formatted_request.replace('%20', ' ')
    formatted_request = formatted_request.replace('%7B', '{')
    formatted_request = formatted_request.replace('%7D', '}')

    # processing json commands

    if r_run.search(formatted_request) is not None:
        try:  # gonna test - try not to search one more time
            m_run = r_run.search(formatted_request)
            s_run = m_run.group(1)
            j_run = json.loads(s_run)
            for js_run in j_run:
                try:
                    function_to_call = tokens[js_run]
                    function_to_call(j_run[js_run])
                except Exception as e:
                    print('SKIP while dispatching run commands with function_to_call: {}, {}'.format(type(e), e))
        except Exception as e:
            print('Error while processing run json.loads()  {}, {}'.format(type(e), e))
        finally:
            html = "HTTP/1.0 200 OK\r\n\r\nI Am Robot not Groot\r\n    ms: " + str(time.ticks_ms() - start) + "\r\n"
            robot_busy = False

    elif r_settings.search(formatted_request) is not None:
        try:
            m_settings = r_settings.search(formatted_request)
            s_settings = m_settings.group(1)
            j_settings = json.loads(s_settings)

            # update_settings(settings_to_update=j_settings, file=robot_settings_file)
            update_settings(settings_to_update=j_settings, file=robot_settings_file)
            print('DBG r_settings.search after update: {}'.format(robot_settings))
        except Exception as e:
            print('Error while processing settings json.loads()  {}, {}'.format(type(e), e))
        finally:
            html = "HTTP/1.0 200 OK\r\n\r\nI Am Robot not Groot\r\n    ms: " + \
                   str(time.ticks_ms() - start) + "\r\n    settings: " + \
                   str(robot_settings) + "\r\n"
            robot_busy = False

    elif r_load_default.search(formatted_request):


        html = """<html>
<head>
    <title>RoboSettings</title>
</head>
<body>Curr: """ + str(robot_settings) + """<p>
<form class="" action="http://""" + robot_ip + """/" method="get">
    <input type="text" name="settings" id="settings" value="" placeholder="{'':''}">
    <input type="submit" value="submit">
</form>
</body>
</html>
"""
        # Def: """ + str(robot_settings_defaults) + """<p>
        robot_busy = False

    else:
        html = "HTTP/1.0 200 OK\r\n\r\nI Am Robot not Groot\r\n    ms: " + \
               str(time.ticks_ms() - start) + "\r\n    settings: " + \
               str(robot_settings) + "\r\n"
        robot_busy = False


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


@asyncio.coroutine
def serve(reader, writer):
    global robot_busy
    try:
        line = yield from reader.read()

        if robot_busy:
            print('DBG serve robot_busy: {}'.format(robot_busy))
            print('DBG line: {}, {}'.format(type(line), str(line)[:40]))
        else:
            print('DBG serve robot_busy: {}'.format(robot_busy))
            robot_listener_json(line)
            print('DBG line: {}, {}'.format(type(line), str(line)[:120]))  # mod readline
            yield from writer.awrite(html)
            yield from writer.aclose()

    except Exception as e:
        print('Error while serve: {}, {}'.format(type(e), e))
    finally:
        robot_busy = False


def run():
    global robot_busy
    robot_busy = False
    loop = asyncio.get_event_loop()
    loop.call_soon(asyncio.start_server(serve, "192.168.4.1", 80))
    loop.run_forever()
    loop.close()


if __name__ == '__main__':

    if read_settings(robot_settings_file):
        robot_settings = read_settings(robot_settings_file)
    else:
        robot_settings = read_settings(robot_default_settings_file)
    # main loop
    run()


