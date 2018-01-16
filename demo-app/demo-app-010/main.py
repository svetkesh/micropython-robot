'''
http://192.168.101.102/?headx=0.3&handy=0.7

?headx=0.3&handy=0.7
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
<form class="" action="http://192.168.101.102/" method="get">
-->
<form class="" action="http://192.168.88.186/" method="get">
    <input type="text" name="headx" id="headx" value="" placeholder="0.00">
    <input type="text" name="handy" id="handy" value="" placeholder="0.00">
    <input type="submit" value="submit position">
</form>
</body>

<!--http://192.168.101.102/?headx=0.3&handy=0.7-->

</html>

"""

#Setup drives
# LE0 = machine.Pin(0, machine.Pin.OUT)
# LED2 = machine.Pin(2, machine.Pin.OUT)
# motor_a_p = machine.PWM(machine.Pin(5), freq=50)
# motor_a_m = machine.PWM(machine.Pin(0), freq=50)
# serv = machine.PWM(machine.Pin(12), freq=50)
sevr_head_x = machine.PWM(machine.Pin(14), freq=50)
sevr_hand_y = machine.PWM(machine.Pin(13), freq=50)

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

    # get head position
    r_headx = re.compile("headx=0\.(\d+)")
    m_headx = r_headx.search(request)

    # get hand position
    r_handy = re.compile("handy=0\.(\d+)")  #
    m_handy = r_handy.search(request)

    try:
        print('string: {}\n found x,y: {} , {}'.format(
            request, m_headx.group(0), m_handy.group(0)))
    except:
        print('string: {}\n found: {}'.format(
            request, "Position not found"))

    print('\n---- looking for exact headx/handy value:')

    try:
        s_headx = str(m_headx.group(0))
        print('source string: {}'.format(s_headx))
        headx = r_number.search(s_headx)
        print('  value found: {}'.format(headx.group(0)))
        f_headx = float(headx.group(0))
        # print('  float value: {} , value+2 = {} '.format(f_headx, f_headx + 2))  # testing float conversion

        s_handy = str(m_handy.group(0))
        print('source string: {}'.format(s_handy))
        handy = r_number.search(s_handy)
        print('  value found: {}'.format(handy.group(0)))
        f_handy = float(handy.group(0))

    except:
        print('source string: {}'.format('None found'))
        print('  value found: {}'.format('None found'))
        print('Error searching value for headx')
        f_headx = 0.5
        f_handy = 0.5

    # posx = int(((f_headx + 1)/2) * 110 + 30)
    posx = int(f_headx * 75 + 40)
    posy = int(f_handy * 75 + 40)

    print('position x,y : {} , {}'.format(posx, posy))

    sevr_head_x.duty(posx)
    sevr_hand_y.duty(posy)

    response = html
    conn.send(response)
    conn.close()
