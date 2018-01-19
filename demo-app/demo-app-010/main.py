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


ver 0.7.9.2 - accepting separate commands
0.7.9.2 - version for SuperBuggy 0.7.9.2
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

#HTML to send to browsers
html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<!-- 
<form class="" action="http://192.168.4.1/" method="get">
-->
<form class="" action="http://192.168.4.1/" method="get">
    <input type="text" name="headx" id="headx" value="" placeholder="0.00">
    <input type="text" name="handy" id="handy" value="" placeholder="0.00">
    <input type="submit" value="submit position">
</form>
</body>
<!--http://192.168.101.102/?headx=0.5&handy=0.5&turnx=0.5&runy=0.5-->
</html>

"""

#Setup drives
# LE0 = machine.Pin(0, machine.Pin.OUT)
# LED2 = machine.Pin(2, machine.Pin.OUT)
motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
serv_direction = machine.PWM(machine.Pin(12), freq=50)
# sevr_head_x = machine.PWM(machine.Pin(14), freq=50)
# sevr_hand_y = machine.PWM(machine.Pin(13), freq=50)

#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
print('DBG: opened connection to port 80')
while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    # print("Content = %s" % str(request))  # print full request
    request = str(request)

    # compile re number
    r_number = re.compile("0\.(\d+)")

    # # get head position
    # r_headx = re.compile("headx=0\.(\d+)")
    # m_headx = r_headx.search(request)
    #
    # # get hand position
    # r_handy = re.compile("handy=0\.(\d+)")  #
    # m_handy = r_handy.search(request)

    # get body direction turnx
    r_turnx = re.compile("turnx=0\.(\d+)")  #
    m_turnx = r_turnx.search(request)

    # get body speed runy
    r_runy = re.compile("runy=0\.(\d+)")  #
    m_runy = r_runy.search(request)

    # try:
    #     print('string: {}\n found x,y: {} , {}'.format(
    #         request, m_headx.group(0), m_handy.group(0)))
    # except:
    #     print('string: {}\n found: {}'.format(
    #         request, "Position not found"))

    # print('\n---- looking for exact headx/handy value'
    #       '\n---- and direction and speed       ---- :')

    try:
        # default values for positions and speed and direction
        # f_headx = 0.5
        # f_handy = 0.5
        f_turnx = 0.5
        f_runy = 0.5

        # selecting only actual commands without defaults values
        # >>> print('not') if None != re_compiled.search(search_string) else print('yes')
        # not

        # if r_headx.search(request) != None:
        #
        #     s_headx = str(m_headx.group(0))
        #     print('source string: {}'.format(s_headx))
        #     headx = r_number.search(s_headx)
        #     print('  value found: {}'.format(headx.group(0)))
        #     f_headx = float(headx.group(0))
        #     # print('  float value: {} , value+2 = {} '.format(f_headx, f_headx + 2))  # testing float conversion
        #     posx = int(f_headx * 75 + 40)
        #     sevr_head_x.duty(posx)
        #
        #     print('got position from joystick hand x,y : {} , {}\n'
        #           'got position from joystick run turn : {} \n'
        #           'direction , speed : {} , {}'.format(posx,
        #                                                '-',
        #                                                '-',
        #                                                '-',
        #                                                '-'))
        #
        # if r_handy.search(request) != None:
        #     s_handy = str(m_handy.group(0))
        #     print('source string: {}'.format(s_handy))
        #     handy = r_number.search(s_handy)
        #     print('  value found: {}'.format(handy.group(0)))
        #     f_handy = float(handy.group(0))
        #     posy = int(f_handy * 75 + 40)
        #     sevr_hand_y.duty(posy)
        #
        #     print('got position from joystick hand x,y : {} , {}'
        #           'got position from joystick run turn : {} \n'
        #           'direction , speed : {} , {}'.format('-',
        #                                                posy,
        #                                                '-',
        #                                                '-',
        #                                                '-'))

        if r_turnx.search(request) != None:
            # &turnx=0.5
            s_turnx = str(m_turnx.group(0))
            print('source string: {}'.format(s_turnx))
            turnx = r_number.search(s_turnx)
            print('  value found: {}'.format(turnx.group(0)))
            f_turnx = float(turnx.group(0))
            directionx = int(f_turnx * 75 + 40)
            serv_direction.duty(directionx)

            print('got position from joystick hand x,y : {} , {}'
                  'got position from joystick run turn : {} \n'
                  'direction , speed : {} , {}'.format('-',
                                                       '-',
                                                       directionx,
                                                       '-',
                                                       '-'))

        if r_runy.search(request) != None:
            # &runy=0.5
            s_runy = str(m_runy.group(0))
            print('source string: {}'.format(s_runy))
            runy = r_number.search(s_runy)
            print('  value found: {}'.format(runy.group(0)))
            f_runy = float(runy.group(0))

            if f_runy < 0.5:
                m_duty = -1
            else:
                m_duty = 1

            p_duty = int(abs(f_runy * 3000) - 1500)

            print('got position from joystick hand x,y : {} , {}'
                  'got position from joystick run turn : {} \n'
                  'direction , speed : {} , {}'.format('-',
                                                       '-',
                                                       '-',
                                                       m_duty,
                                                       p_duty))
            motor_a_p.duty(p_duty)
            motor_a_m.duty(m_duty)



    except:
        print('Error searching exact values')

    # posx = int(f_headx * 75 + 40)
    # posy = int(f_handy * 75 + 40)
    # directionx = int(f_turnx * 75 + 40)
    # speedy = int(f_runy * 75 + 40)

    # calculate direction and speed "speedy"
    # motor_a_p.duty( -1000 .. 2000) # need to recalculate
    # motor_a_m.duty(-1 .. 1)
    #
    # if f_runy < 0.5:
    #     m_duty = -1
    # else:
    #     m_duty = 1
    #
    # p_duty = int(abs(f_runy * 3000) - 1500)

    # print('got position from joystick hand x,y : {} , {}\n'
    #       'got position from joystick run turn : {} \n'
    #       'direction , speed : {} , {}'.format(posx,
    #                                            posy,
    #                                            directionx,
    #                                            m_duty,
    #                                            p_duty))

    # sevr_head_x.duty(posx)
    # sevr_hand_y.duty(posy)

    # serv_direction.duty(directionx)
    # place here speed
    # motor_a_p.duty(p_duty)
    # motor_a_m.duty(m_duty)

    response = html
    conn.send(response)
    conn.close()
