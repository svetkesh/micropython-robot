'''
http://192.168.101.102/?headx=0.3

?headx=0.3
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
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form class="" action="http://192.168.101.102/" method="get">
<input type="text" name="headx" id="headx" value="" placeholder="0.00">
<input type="submit" value="head x">
</form>
</body>
<!--http://192.168.101.102/?headx=0.37-->
</html>

"""

#Setup drives
# LE0 = machine.Pin(0, machine.Pin.OUT)
# LED2 = machine.Pin(2, machine.Pin.OUT)
# motor_a_p = machine.PWM(machine.Pin(5), freq=50)
# motor_a_m = machine.PWM(machine.Pin(0), freq=50)
# serv = machine.PWM(machine.Pin(12), freq=50)
sevr_head_x = machine.PWM(machine.Pin(14), freq=50)

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
    # # LEDON0 = request.find('/?LED=ON0')
    # # LEDOFF0 = request.find('/?LED=OFF0')
    # # LEDON2 = request.find('/?LED=ON2')
    # # LEDOFF2 = request.find('/?LED=OFF2')
    #
    #
    # #print("Data: " + str(LEDON0))
    # #print("Data2: " + str(LEDOFF0))
    #
    # LEDON0 = request.find('/?LED=ON0')
    #
    #
    # if LEDON0 == 6:
    #     print('TURN LED0 ON')
    #     LED0.low()
    # if LEDOFF0 == 6:
    #     print('TURN LED0 OFF')
    #     LED0.high()
    # if LEDON2 == 6:
    #     print('TURN LED2 ON')
    #     LED2.low()
    # if LEDOFF2 == 6:
    #     print('TURN LED2 OFF')
    #     LED2.high()

    # try head x pos
    # re.search(r'=0.(\d+)', s).groups(0)
    # int(re.findall(r'(\d+)', s)[-1])

    # reqx = re.findall(r'(\d+)', request)[-1]  # re.findall is not available for micropython

    # reqx

    r_number = re.compile("0\.(\d+)")
    r_headx = re.compile("headx=0\.(\d+)")
    m_headx = r_headx.search(request)

    try:
        print('string: {}\n    re: {}\n found: {}'.format(
            request, str(r_headx), m_headx.group(0)))
    except:
        print('string: {}\n    re: {}\n found: {}'.format(
            request, str(r_headx), "None found"))

    print('\n---- looking for exact headx/handy value:')

    try:
        s_headx = str(m_headx.group(0))
        print('source string: {}'.format(s_headx))
        headx = r_number.search(s_headx)
        print('  value found: {}'.format(headx.group(0)))
        f_headx = float(headx.group(0))
        print('  float value: {} , value+2 = {} '.format(f_headx, f_headx + 2))

    except:
        print('source string: {}'.format('None found'))
        print('  value found: {}'.format('None found'))
        print('Error searching value for headx')
        f_headx = 0.01

    # posx = int(((f_headx + 1)/2) * 110 + 30)
    posx = int(f_headx  * 75 + 40)

    print('position x : {}'.format(posx))

    sevr_head_x.duty(posx)

    response = html
    conn.send(response)
    conn.close()
