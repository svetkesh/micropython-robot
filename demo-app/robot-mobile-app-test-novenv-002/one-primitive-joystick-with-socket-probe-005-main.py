from kivy.app import App
from kivy.garden.joystick import Joystick
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import time
# import requests

import socket

# sock = socket.socket()
# sock.connect(('localhost', 9090))
# sock.send('hello, world!')
#
# data = sock.recv(1024)
# sock.close()

# print data

# robot address
# robot_host = '192.168.101.101'
# robot_host = '192.168.88.186'  # hardcodedrobot ip t4m net
robot_host = '192.168.4.1'  # hardcodedrobot ip t4m net

class DemoApp(App):
    def build(self):
        self.root = BoxLayout()
        self.root.padding = 50
        joystick = Joystick()
        joystick.bind(pad=self.update_coordinates)
        self.root.add_widget(joystick)
        self.label = Label()
        self.root.add_widget(self.label)
    def update_coordinates(self, joystick, pad):
        send_status = 'try...'
        x = str(pad[0])[0:5]
        y = str(pad[1])[0:5]
        radians = str(joystick.radians)[0:5]
        magnitude = str(joystick.magnitude)[0:5]
        angle = str(joystick.angle)[0:5]
        # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # self.label.text = text.format(x, y, radians, magnitude, angle, send_status)

        time.sleep(0.4)

        posx = (float(x)+1)/2
        print('posx: {}'.format(posx))
        #
        # http://192.168.88.186/?headx=0.37
        # http://192.168.4.1/?headx=0.37
        #
        # url = 'http://192.168.88.186/'
        # payload = {'headx',posx}
        # r = requests.post(url, data=payload)
        # print(r.text)

        # socket implementation in this def
        try:

            sock = socket.socket()
            send_status = 'sock-OK '
            sock.connect((robot_host, 80))
            send_status = 'connect-OK '
            soc_string = 'http://192.168.4.1/?headx=' + str(posx)
            send_status = 'string-OK '
            sock.send(soc_string)
            send_status = 'send-OK '
            sock.close()
            send_status = 'close-OK '
            send_status = 'sent ok'
        except:
            send_status += 'error'

        # display info
        text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        self.label.text = text.format(x, y, radians, magnitude, angle, send_status)



DemoApp().run()