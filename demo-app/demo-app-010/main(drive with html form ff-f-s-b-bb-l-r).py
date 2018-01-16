import socket
import machine

#HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head> <title>DRIVE-PAD</title> </head>
<body>
<form>
<table align=center>
  <tr>
    <td>00
    </td>
    <td>01<button name="ff" value="ff" type="submit">ff</button>
    </td>
    <td>02
    </td>
    <td>03
    </td>
    <td>04
    </td>
    <td>05
    </td>
  </tr>
  <tr>
    <td>10
    </td>
    <td>11<button name="f" value="f" type="submit">f</button>
    </td>
    <td>12
    </td>
    <td>13
    </td>
    <td>14
    </td>
    <td>15
    </td>
  </tr>
  <tr>
    <td>20<button name="l" value="l" type="submit">l</button>
    </td>
    <td>21<button name="s" value="s" type="submit">s</button>
    </td>
    <td>22<button name="r" value="r" type="submit">r</button>
    </td>
    <td>23
    </td>
    <td>24
    </td>
    <td>25
    </td>
  </tr>
  <tr>
    <td>30
    </td>
    <td>31<button name="b" value="b" type="submit">b</button>
    </td>
    <td>32
    </td>
    <td>33
    </td>
    <td>34
    </td>
    <td>35
    </td>
  </tr>
  <tr>
    <td>40
    </td>
    <td>41<button name="bb" value="bb" type="submit">bb</button>
    </td>
    <td>42
    </td>
    <td>43
    </td>
    <td>44
    </td>
    <td>45
    </td>
  </tr>
</table>
</form>
</body>
</html>

"""

#Setup drives
# LE0 = machine.Pin(0, machine.Pin.OUT)
# LED2 = machine.Pin(2, machine.Pin.OUT)
motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
serv = machine.PWM(machine.Pin(12), freq=50)

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
    # LEDON0 = request.find('/?LED=ON0')
    # LEDOFF0 = request.find('/?LED=OFF0')
    # LEDON2 = request.find('/?LED=ON2')
    # LEDOFF2 = request.find('/?LED=OFF2')


    #print("Data: " + str(LEDON0))
    #print("Data2: " + str(LEDOFF0))

    LEDON0 = request.find('/?LED=ON0')


    if LEDON0 == 6:
        print('TURN LED0 ON')
        LED0.low()
    if LEDOFF0 == 6:
        print('TURN LED0 OFF')
        LED0.high()
    if LEDON2 == 6:
        print('TURN LED2 ON')
        LED2.low()
    if LEDOFF2 == 6:
        print('TURN LED2 OFF')
        LED2.high()
    response = html
    conn.send(response)
    conn.close()
