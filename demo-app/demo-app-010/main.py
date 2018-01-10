import socket
import machine
import re

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
while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
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

    reqx = re.findall(r'(\d+)', request)[-1]

    posx = ((int(reqx) +1)/200)*(110-70)

    print('position x : {}'.format(posx))

    sevr_head_x.duty(posx)

    response = html
    conn.send(response)
    conn.close()
