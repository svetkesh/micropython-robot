'''
This is main.py for running on ESP8266 MicroPython

Handles request of type:

http://192.168.101.102/?headx=0.5&handy=0.5&turnx=0.5&runy=0.5

Not requires all
 headx, handy, turnx, runy

>>> import ure
>>> rh = re.compile("headx=0\.(\d+)")

# >>> print('not') if None != rh.search(s) else print('yes')
# not
>>> print('not') if None != rh.search(not_s) else print('yes')
yes


ver 0.7.9.1 - accepting separate commands
0.7.9.1 - version for RoboHand 0.7.9.1

ver 0.7.9.1 + minor fix for y axis for hand - joystick

ver 0.7.9.3 reply html with current IP
ver 0.7.9.4 add catch (now testing ...)

add set wifi ...

'''

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
import ujson as json


LONG_SLEEP = 10
SHORT_SLEEP = 1
BLINK_SLEEP = 0.3

robot_ip = '192.168.4.1'

sta_if = network.WLAN(network.STA_IF)

if sta_if.active():
    print('sta_if: {}, {}, {}'.format(sta_if.active(), type(sta_if.ifconfig()), sta_if.ifconfig()))
    if sta_if.ifconfig()[0] != '0.0.0.0':
        pass
        # robot_ip = sta_if.ifconfig()[0]  # do not overwrite default ip 192.168.4.1
    print('robot_ip : {}'. format(robot_ip))


#HTML to send to browsers



html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<!-- 
<form class="" action="http://""" + robot_ip + """/" method="get">
-->
<form class="" action="http://""" + robot_ip + """/" method="get">
    <input type="text" name="headx" id="headx" value="" placeholder="0.0 hand x">
    <input type="text" name="handy" id="handy" value="" placeholder="0.0 hand y">
    <br>
    <input type="text" name="turnx" id="turnx" value="" placeholder="0.0 turn">
    <input type="text" name="runy" id="runy" value="" placeholder="0.0 speed">
    <br>
    <input type="checkbox" name="catch" value="catch">catch-release
    <br>
    <input type="submit" value="submit position">
</form>>
</body>
<!--http://192.168.101.102/?headx=0.5&handy=0.5&turnx=0.5&runy=0.5&catch=catch -->
<!-- hold-on -->
</html>

"""

html_settings = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form class="" action="http://""" + robot_ip + """/" method="get">
    <input type="text" name="nextssid" id="nextssid" value="" placeholder="WIFI network SSID">
    <br>
    <input type="text" name="nextwifipassword" id="nextwifipassword" value="" placeholder="WIFI password">
    <p>
    Mode
    <input type="text" name="nextrunmode" id="nextrunmode" value="" placeholder="demo|run|stage">
    </p>
    <br>
    <input type="submit" value="submit">
</form>>
</body>
</html>

"""

#Setup drives
# LE0 = machine.Pin(0, machine.Pin.OUT)
# LED2 = machine.Pin(2, machine.Pin.OUT)
motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
serv_direction = machine.PWM(machine.Pin(12), freq=50)
sevr_head_x = machine.PWM(machine.Pin(14), freq=50)
sevr_hand_y = machine.PWM(machine.Pin(13), freq=50)
sevr_catch = machine.PWM(machine.Pin(15), freq=50)

networkpin = machine.Pin(2, machine.Pin.OUT)
# networkpin.on()

# def blink_report(n_blinks):
#     networkpin.off()
#     time.sleep(SHORT_SLEEP*2)
#     for blinks in range (n_blinks):
#         networkpin.on()
#         time.sleep(BLINK_SLEEP)
#         networkpin.off()

def blink_report(n_blinks):
    # networkpin.off()
    print('booooom')
    time.sleep(SHORT_SLEEP*2)
    for blinks in range (n_blinks):
        # networkpin.on()
        time.sleep(BLINK_SLEEP)
        # networkpin.off()
        print('blinks {}'.format(blinks))


def blink_twice(n_blinks, repeat_reports = 2):
    def blink_report(n_blinks):
        # networkpin.off()
        print('booooom')
        time.sleep(SHORT_SLEEP * 2)
        for blinks in range(n_blinks):
            # networkpin.on()
            time.sleep(BLINK_SLEEP)
            # networkpin.off()
            print('blinks {}'.format(blinks))
    for repeat in range(repeat_reports):
        blink_report(n_blinks)

# Setup Socket WebServer
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    print('DBG: opened connection to port 80')
    while True:
        try:
            networkpin.on()
            conn, addr = s.accept()
            print("Got a connection from %s" % str(addr))
            request = conn.recv(1024)
            # print("Content = %s" % str(request))  # print full request
            request = str(request)

            # keep it simple ... delete after all )

            # r_nextssid = re.compile('nextssid=(\\w+)')  # compile re just alpha num chars

            r_nextssid = re.compile('nextssid=([a-zA-Z0-9_\s\@\!\#\%\*\-]+)') # wide SSID Naming Convention as :
            # https://www.cisco.com/assets/sol/sb/WAP321_Emulators/WAP321_Emulator_v1.0.0.3/help/Wireless05.html

            r_nextwifipassword = re.compile('nextwifipassword=([a-zA-Z0-9_\!\@\#\$\%\^\*\(\)\=\`\~\-]+)')

            # processing request and searching SSID
            if r_nextssid.search(request) is not None:
                try:
                    print('DBG found some SSID')  # keep it simple
                    # request = request.decode("utf-8")

                    print('DBG request: {}\n'.format(request))
                    print('DBG r_nextssid.search(request): {}\n'.format(r_nextssid.search(request)))
                    print('DBG r_nextssid.search(request) is not None: {}\n'.format(r_nextssid.search(request) is not None))

                    m_nextssid = r_nextssid.search(request)

                    # using list slicing
                    print('DBG m_nextssid: {}\n'.format(m_nextssid))
                    print('DBG m_nextssid.group(0): {}\n'.format(m_nextssid.group(0)))
                    print('DBG m_nextssid.group(0)[9:]: {}\n'.format(m_nextssid.group(0)[9:]))
                    print('DBG m_nextssid.group(1): {}\n'.format(m_nextssid.group(1)))
                    # using second group in search, group(1)
                    print('DBG r_nextssid.search(request).group(0): {}\n'.format(r_nextssid.search(request).group(0)))
                    print('DBG r_nextssid.search(request).group(1): {}\n'.format(r_nextssid.search(request).group(1)))

                    ssid = r_nextssid.search(request).group(1)

                except Exception as e:
                    print('ERR: got {} error {}'.format(type(e), e))
                    print('\n while processing request and searching SSID {}\n'.format(request))
                    blink_report(5)

            # ### nextssid -> nextwifipassword
            # processing request and searching wifipassword
            if r_nextwifipassword.search(request) is not None:
                try:
                    print('DBG found some wifipassword')  # keep it simple
                    # print(' : {}\n'.format())

                    # request = request.decode("utf-8")

                    print('DBG request: {}\n'.format(request))
                    print('DBG r_nextwifipassword.search(request): {}\n'.format(r_nextwifipassword.search(request)))
                    print('DBG r_nextwifipassword.search(request) is not None: {}\n'.format(r_nextwifipassword.search(request) is not None))

                    m_nextwifipassword = r_nextwifipassword.search(request)

                    # using list slicing
                    print('DBG m_nextwifipassword: {}\n'.format(m_nextwifipassword))
                    print('DBG m_nextwifipassword.group(0): {}\n'.format(m_nextwifipassword.group(0)))
                    print('DBG m_nextwifipassword.group(0)[17:]: {}\n'.format(m_nextwifipassword.group(0)[17:]))
                    print('DBG m_nextwifipassword.group(1): {}\n'.format(m_nextwifipassword.group(1)))
                    # using second group in search, group(1)
                    print('DBG r_nextwifipassword.search(request).group(0): {}\n'.format(r_nextwifipassword.search(request).group(0)))
                    print('DBG r_nextwifipassword.search(request).group(1): {}\n'.format(r_nextwifipassword.search(request).group(1)))

                    wifipassword = r_nextwifipassword.search(request).group(1)

                except Exception as e:
                    print('ERR: got {} error {}'.format(type(e), e))
                    print('\n while processing request and searching wifipassword {}\n'.format(request))
                    blink_report(5)

            else:
                print('DBG: r_wifipassword NOT found')
                print(request)
                print('----')

            # write date into JSON formatted text file
            try:
                with open('config.txt', 'w') as f:
                    f.write('{"ssid":"' + ssid +
                            '","wifipassword":"' + wifipassword +
                            '","trick":"demo"' +
                            '}')
            except:
                print('DBG error saving settings')

            # read JSON from file
            try:
                with open('config.txt', 'r') as f:
                    j = json.load(f)
                    # print(f.read())
                    print(j)
                    print(j['ssid'])
                    print(j['wifipassword'])
                    print(j['trick'])
            except:
                print('ERR reading file')

            networkpin.off()

            # response = html  # original html for for driving and cathing
            response = html_settings
            conn.send(response)
            conn.close()
        except Exception as e:
            print('got Exception while processing requests: {} , {}'.format(type(e), e))
            # blink_report(6)
            # blink_report(6)
            networkpin.off()
            #
            # utime.sleep(LONG_SLEEP)
            #
            time.sleep(SHORT_SLEEP)
            # # hard reset
            # machine.reset()
            # soft reset
            sys.exit()

            #
except Exception as e:
    print('got Exception with running Web server: {} , {}'.format(type(e), e))
    blink_report(7)
    blink_report(7)
    networkpin.off()

