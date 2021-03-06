"""
to load settings:
        http://192.168.4.1/?load=default

0.8.6.1 - start 'objecting'...
main-tank(0.8.7.1.1) tank version

"""

try:
    import uasyncio as asyncio
    import machine
    import ure as re
    import ujson as json
    import utime as time
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
motor_b_p = machine.PWM(machine.Pin(4), freq=50)
motor_b_m = machine.PWM(machine.Pin(2), freq=50)

servo_headx = machine.PWM(machine.Pin(12), freq=50)  # Pin 6
servo_handy = machine.PWM(machine.Pin(13), freq=50)  # Pin 7
fire_led5 = machine.PWM(machine.Pin(14), freq=50)  # Pin 5
# right_led8 = machine.PWM(machine.Pin(15), freq=50)  #pin 8

robot_settings = {}
robot_settings_file = 'settings.txt'

leds_on = False
# DEBUG_ON = True


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
        j_str = json.dumps(j)
        print('DBG: JSON data loaded OK')
        with open(file, 'w') as f:
            f.write(str(j_str))
            print('DBG: data: {} written to: {}, OK'.format(file, j_str))
        return True
    except json.JSONDecodeError as e:
        print('ERR: data not valid JSON: {}, {}, {}'.format(type(e), e, str(j)))
    except Exception as e:
        print('ERR: given data could not be written {}, {}\n    {}'.format(type(e), e, str(j)))
        return False


if read_settings(robot_settings_file):
    robot_settings = read_settings(robot_settings_file)
else:
    raise SystemExit


def update_settings(settings_to_update=None, file=robot_settings_file):
    global robot_settings
    if settings_to_update:
        try:
            for item in settings_to_update:
                try:
                    print('DBG update {} -> {}'.format(
                        robot_settings[item],
                        settings_to_update[item]
                    ))
                except Exception as e:
                    print('ERR-DBG update_settings for: {}, {}, {}'.format(item, settings_to_update[item], e))

                if settings_to_update[item] in ('True', 'TRUE', 'true', 'T', 't',
                                                'Yes', 'YES', 'yes', 'Y', 'y'):
                    robot_settings[item] = True
                elif settings_to_update[item] in ('False', 'FALSE', 'false', 'F', 'F',
                                                  'No', 'NO', 'no', 'N', 'n'):
                    robot_settings[item] = False
                else:
                    try:
                        setting_i = int(settings_to_update[item])
                        robot_settings[item] = setting_i
                    except ValueError:
                        robot_settings[item] = settings_to_update[item]

            write_settings(robot_settings, file)
            return True
        except Exception as e:
            print('Error while updating settings {}, {}'.format(type(e), e))
            return False
        finally:
            print('DBG after robot_settings: {}, {}'.format(type(robot_settings), robot_settings))
    else:
        print('DBG nothing to update, '
              'current settings: {}, {}'.format(type(robot_settings),
                                                robot_settings))
        return True


# compile regex for commands
r_settings = re.compile("settings=({.*})")
r_run = re.compile("run=({.*})")
r_load_default = re.compile("load=default")
r_reset = re.compile("reset=reset")


def give_up():
    pass


def limit_min_max(x, mini, maxi):
    try:
        if x > maxi:
            return maxi
        elif x < mini:
            return mini
        else:
            return x
    except TypeError:
        return x


def move_servo(servo,
               duty=robot_settings['servo_center'],
               forward=True,
               servo_min=robot_settings['servo_min'],
               servo_max=robot_settings['servo_max'],
               servo_adj_zero=0,
               servo_multiply_power=1,
               # servo_speed=1,
               # servo_type='direct'
               ):
    # # servo_speed is placeholder for speed switching operating servo
    # # servo_type = 'direct' / additive  placeholder for type of servo command
    try:
        duty_int = int(duty)
        if duty_int in range(servo_min, servo_max):
            duty_int = limit_min_max(duty_int, servo_min, servo_max)
        if forward:
            duty_int = duty_int + servo_adj_zero
            servo.duty(duty_int * servo_multiply_power)
        else:
            duty_int = servo_min + servo_max - duty_int + servo_adj_zero
            servo.duty(duty_int * servo_multiply_power)
    except Exception as e:
        print('Error while move_servo {}, {}'.format(type(e), e))
    # finally:
    #     print('DBG move_servo {} got duty: {}, {} -> {}'
    #           ''.format(servo, type(duty), duty, duty_int))


def headx(key):
    move_servo(servo_headx, duty=key)


def handy(key):
    move_servo(servo_handy, duty=key)


def run(duty):
    print('Enter run({}, {})'.format(type(duty), duty))
    try:
        i_run = int(duty)
        if abs(i_run - 50) < 2:
            m_duty = 0
            p_duty = 0
        else:
            if i_run < 50:
                p_duty = int(robot_settings['gear_factor'] * (50 - i_run) * 4)
                m_duty = 0
            elif i_run > 50:
                p_duty = int(robot_settings['gear_factor'] * (i_run-50) * 4)
                m_duty = int(robot_settings['gear_factor'] * (i_run-50) * 4)
            else:
                m_duty = 0
                p_duty = 0

        print('DBG i_runy {} G: {}, K: {}->{}, P: {} , M: {}'.format(time.ticks_ms(), robot_settings['gear_factor'],
                                                                     duty, i_run, p_duty, m_duty))
    except Exception as e:
        print('Error while processing run: {}, {}'.format(type(e), e))
    finally:
        return p_duty, m_duty


def runa(key):
    print('Enter runa with arg: {}, {}'.format(type(key), key))
    try:
        # p, m = run(key)
        run(key)
        # print("run(key) {} ()".format(p, m))
        # motor_a_p.duty(p)
        # motor_a_m.duty(m)
    except Exception as e:
        print('Error while processing runa: {}, {}'.format(type(e), e))


def runb(key):
    p, m = run(key)
    motor_b_p.duty(p)
    motor_b_m.duty(m)


def fire(key):
    fire_led5.duty(800)
    time.sleep_ms(50)
    fire_led5.duty(0)


def gear(key):
    print('DBG running: {} key: {}'.format('gear', key))
    try:
        robot_settings['gear_factor'] = int(key)
        update_settings(settings_to_update=robot_settings, file=robot_settings_file)
    except Exception as e:
        robot_settings['gear_factor'] = 4
        print('ERR: could not set gear: () use default "4". {}, {}, {}'.format(str(key), type(e), e))
    
tokens = {
    'headx': headx,
    'handy': handy,
    'runa': runa,
    'runb': runb,
    'fire': fire,
    'gear': gear,
    'read_settings': read_settings,
    'update_settings': update_settings,
    # 'give_up': give_up,
}


def robot_listener_json(mess):
    global robot_settings
    global robot_busy
    robot_busy = True
    global html
    start = time.ticks_ms()

    mess = mess.replace('%22', '\"')
    mess = mess.replace('%27', '\"')
    mess = mess.replace('%20', ' ')
    mess = mess.replace('%7B', '{')
    mess = mess.replace('%7D', '}')
    mess = mess.replace('%2C', ',')
    mess = mess.replace('%3A+', ': ')
    mess = mess.replace('%3A', ':')

    # processing json commands
    if r_run.search(mess) is not None:
        try:
            m_run = r_run.search(mess)
            s_run = m_run.group(1)
            j_run = json.loads(s_run)
            for js_run in j_run:
                try:
                    function_to_call = tokens[js_run]
                    print('Dispatching command: {} for {}'.format(function_to_call, j_run[js_run]))
                    function_to_call(j_run[js_run])

                except Exception as e:
                    print('SKIP dispatching  unknown command: {}, {}, {}'.format(js_run, j_run, type(e), e))
        except Exception as e:
            print('ERR while dispatching command: {}, {}'.format(type(e), e))
        finally:
            html = "HTTP/1.0 200 OK\r\n\r\nI Am Robot\r\n    ms: " + str(time.ticks_ms() - start) + "\r\n"
            # print('DBG robot run in: {}ms'.format(str(time.ticks_ms() - start)))
            robot_busy = False

    elif r_settings.search(mess) is not None:
        try:
            m_settings = r_settings.search(mess)
            s_settings = m_settings.group(1)
            j_settings = json.loads(s_settings)

            update_settings(settings_to_update=j_settings, file=robot_settings_file)
        except Exception as e:
            print('Error while processing settings json.loads()  {}, {}'.format(type(e), e))
        finally:
            html = "HTTP/1.0 200 OK\r\n\r\nI Am Robot\r\n    ms: " + \
                   str(time.ticks_ms() - start) + "\r\n    settings: " + \
                   str(robot_settings) + "\r\n"
            robot_busy = False

    elif r_load_default.search(mess):
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
        robot_busy = False
    else:
        html = "HTTP/1.0 200 OK\r\n\r\nI Am Robot\r\n    ms: " + \
               str(time.ticks_ms() - start) + "\r\n    settings: " + \
               str(robot_settings) + "\r\n"
        robot_busy = False  # 4 times could be overrun by try-finally


@asyncio.coroutine
def serve(reader, writer):
    global robot_busy
    try:
        line = yield from reader.read()
        mess = ''

        if robot_busy:
            pass
            # print('DBG serve robot is busy: {}'.format(robot_busy))
            # print('DBG mess: {}, {}'.format(type(mess), mess))
        else:
            # print('DBG robot busy: {} it\'s OK'.format(robot_busy))
            mess = str(line)[:min(120, len(str(line)))]
            robot_listener_json(mess)
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
    robot_busy = False
    # main loop
    run()
