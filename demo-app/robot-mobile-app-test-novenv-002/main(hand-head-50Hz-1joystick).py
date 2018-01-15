'''based on one-primitive-joystick-with-socket-probe-005-main
added socket encoding from
main(testing raw socket connection compiled android app no gui - OK)

add head left-right
add hand up -down

http://192.168.101.102/?headx=0.3&handy=0.7

?headx=0.3&handy=0.7

'''

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
# robot_host = '192.168.4.1'  # hardcodedrobot ip t4m net


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

        # from time import sleep

        # robot_host = '192.168.101.103'  # hardcodedrobot ip t4m net
        robot_host = '192.168.88.186'  # hardcodedrobot ip t4m net
        robot_port = 80

        send_status = 'try...'
        x = str(pad[0])[0:5]
        y = str(pad[1])[0:5]
        radians = str(joystick.radians)[0:5]
        magnitude = str(joystick.magnitude)[0:5]
        angle = str(joystick.angle)[0:5]
        # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # self.label.text = text.format(x, y, radians, magnitude, angle, send_status)

        # time.sleep(0.4)

        posx = (float(x)+1)/2
        posy = 1 - (float(y)+1)/2
        print('posx , posy: {} , {}'.format(posx, posy))

        try:
            client_socket = socket.socket()  # instantiate
            client_socket.connect((robot_host, robot_port))  # connect to the server
            # message = 'http://192.168.4.1/?headx=' + str(posx)  # take input
            # create message to send
            message = 'http://192.168.101.102/?headx=' + str(round(posx, 3)) + '&handy=' + str(round(posy, 3))
            client_socket.send(message.encode())  # encode than send message

            client_socket.close()  # close the connection
            # sleep(3)
            time.sleep(0.02)
            #
            print('posx {} sent'.format(message))
            send_status = 'sent ok \n posx ' + str(posx) + '\n posy ' + str(posy)
        except:
            print('posx not sent {}'.format(posx))
            send_status += 'error sending posx posy'

        # display info
        text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        self.label.text = text.format(x, y, radians, magnitude, angle, send_status)


DemoApp().run()
