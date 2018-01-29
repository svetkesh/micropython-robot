# import kivy
# kivy.require('1.10.0') # replace with your current kivy version !

''' Testing 2 joysticks sending commands
should match main(0.7.9.4. testing).py (ESP8266 autoloaded v. 0.7.9.1)

manages via
headx, handy, turnx, runy

added delay 0.05 s after sending commands

'''

from kivy.app import App

from kivy.uix.widget import Widget
from kivy.garden.joystick import Joystick

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import socket
import time


class RoboPad(FloatLayout):
    def __init__(self, **kwargs):
        super(RoboPad, self).__init__(**kwargs)

        print('running super(Gamepad, self).__init__()')

        # joystickhand and joystickrun
        self.joystickhand = Joystick(size_hint=(.4, .4),
                                     pos_hint={'x':0.0, 'y':.2},
                                     sticky=True)
        self.add_widget(self.joystickhand)
        self.joystickrun = Joystick(size_hint=(.4, .4),
                                    pos_hint={'x':0.6, 'y':.2})
        self.add_widget(self.joystickrun)

        # add some buttons
        self.catchbutton = Button(size_hint=(.15, .15),
                                  pos_hint={'x': .8, 'y': .65},
                                  text='Catch me!')
        self.add_widget(self.catchbutton)

        # add debug Labels
        self.debug_label = Label(size_hint=(.2, .2),
                                     pos_hint={'x': .8, 'y': .8},
                                     text='message ... ...',)  # multiline=True,)
        self.add_widget(self.debug_label)
        self.debug_label_hand = Label(size_hint=(.2, .2),
                                      pos_hint={'x': .1, 'y': .8},
                                      text='message ... ...',)
        self.add_widget(self.debug_label_hand)
        self.debug_label_run = Label(size_hint=(.2, .2),
                                     pos_hint={'x': .5, 'y': .8},
                                     text='message ... ...',)  # multiline=True,)
        self.add_widget(self.debug_label_run)
        
        # bind joystick
        self.joystickrun.bind(pad=self.update_coordinates_run)
        self.joystickhand.bind(pad=self.update_coordinates_hand)
        
    # def update_coordinates(self, joystick, pad):
    def update_coordinates(self, joystick, pad):  # ok copy of original update_coordinates
        pass

        #
        # # from time import sleep
        #
        # # robot_host = '192.168.101.103'  # hardcodedrobot ip t4m net
        # robot_host = '192.168.88.186'  # hardcodedrobot ip t4m net
        # robot_port = 80
        #
        # send_status = 'try...'
        # x = str(pad[0])[0:5]
        # y = str(pad[1])[0:5]
        # radians = str(joystick.radians)[0:5]
        # magnitude = str(joystick.magnitude)[0:5]
        # angle = str(joystick.angle)[0:5]
        # # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # # self.label.text = text.format(x, y, radians, magnitude, angle, send_status)
        #
        # # time.sleep(0.4)
        #
        # posx = (float(x)+1)/2
        # print('posx: {}'.format(posx))
        # #
        # # http://192.168.88.186/?headx=0.37&hand=0.99
        # # http://192.168.4.1/?headx=0.37
        # #
        # # url = 'http://192.168.88.186/'
        # # payload = {'headx',posx}
        # # r = requests.post(url, data=payload)
        # # print(r.text)
        #
        # # socket implementation in this def
        # # try:
        # #
        # #     sock = socket.socket()
        # #     send_status = 'sock-OK '
        # #     sock.connect((robot_host, 80))
        # #     send_status = 'connect-OK '
        # #     soc_string = 'http://192.168.4.1/?headx=' + str(posx)
        # #     send_status = 'string-OK '
        # #     sock.send(soc_string)
        # #     send_status = 'send-OK '
        # #     sock.close()
        # #     send_status = 'close-OK '
        # #     send_status = 'sent ok'
        # # except:
        # #     send_status += 'error'
        #
        # try:
        #     client_socket = socket.socket()  # instantiate
        #     client_socket.connect((robot_host, robot_port))  # connect to the server
        #     message = 'http://192.168.4.1/?headx=' + str(posx)  # take input
        #     client_socket.send(message.encode())  # encode than send message
        #
        #     client_socket.close()  # close the connection
        #     # sleep(3)
        #     time.sleep(0.02)
        #     #
        #     print('posx {} sent'.format(message))
        #     send_status = 'sent ok' + str(posx)
        # except:
        #     print('posx not sent {}'.format(posx))
        #     send_status += 'error sending posx' + str(posx)
        #
        # # display info
        # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # self.label.text = text.format(x, y, radians, magnitude, angle, send_status)

        # test for joystickrun binding ok
        # print('joystickrun binded')
        # x = str(pad[0])[0:5]
        # y = str(pad[1])[0:5]
        # radians = str(joystick.radians)[0:5]
        # magnitude = str(joystick.magnitude)[0:5]
        # angle = str(joystick.angle)[0:5]
        # # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # # self.debuglabel.text = text.format(x, y, radians, magnitude, angle, send_status)
        #
        # # without send_status print just to debug label
        # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}"
        # self.debuglabel.text = text.format(x, y, radians, magnitude, angle)

    # update coordinates for joystickrun
    # for now just print coordinates to debug label

    def update_coordinates_run(self, joystick, pad):
        # test for joystickrun binding test
        # print('update_coordinates_run ...')
        print(self, joystick, pad)
        x = str(pad[0])[0:5]
        y = str(pad[1])[0:5]
        radians = str(joystick.radians)[0:5]
        magnitude = str(joystick.magnitude)[0:5]
        angle = str(joystick.angle)[0:5]
        # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # self.debug_label_run.text = text.format(x, y, radians, magnitude, angle, send_status)

        # without send_status print just to debug label
        text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}"
        self.debug_label_run.text = text.format(x, y, radians, magnitude, angle)
        # self.debug_label.text = text.format(x, y, radians, magnitude, angle)

        # for query http://192.168.101.102/?headx=0.5&handy=0.5&turnx=0.5&runy=0.5
        # robot_host = '192.168.88.186'  # hardcodedrobot ip t4m net
        # robot_port = 80
        # turnx = (float(x) + 1) / 2
        # try:
        #     client_socket = socket.socket()  # instantiate
        #     client_socket.connect((robot_host, robot_port))  # connect to the server
        #     message = 'http://192.168.4.1/?turnx=' + str(turnx)  # take input
        #     client_socket.send(message.encode())  # encode than send message
        #
        #     client_socket.close()  # close the connection
        #     # sleep(3)
        #     # time.sleep(0.02)
        #     #
        #     print('turnx {} sent'.format(message))
        #     send_status = 'sent ok' + str(turnx)
        # except:
        #     print('turnx not sent {}'.format(turnx))
        #     send_status += 'error sending turnx' + str(turnx)

        # <<<
        self.update_fake_data(turnx=x, runy=y)


    def update_coordinates_hand(self, joystick, pad):
        # test for update_coordinates_hand binding test
        # print('update_coordinates_hand running...')
        print(self, joystick, pad)
        x = str(pad[0])[0:5]
        y = str(pad[1])[0:5]
        radians = str(joystick.radians)[0:5]
        magnitude = str(joystick.magnitude)[0:5]
        angle = str(joystick.angle)[0:5]
        # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # self.debug_label_run.text = text.format(x, y, radians, magnitude, angle, send_status)

        # without send_status print just to debug label
        text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}"
        self.debug_label_hand.text = text.format(x, y, radians, magnitude, angle)
        # self.debug_label.text = text.format(x, y, radians, magnitude, angle)

        # <<<
        self.update_fake_data(headx=x, handy=y)

    # def update_fake_data(self, *args,**kwargs):
    def update_fake_data(self, headx='z', handy='z', turnx='z', runy='z'):
        # robot_host = '192.168.88.186'  # hardcodedrobot ip t4m net
        robot_host = '192.168.4.1'  # hardcodedrobot ip t4m net
        robot_port = 80
        print('update_fake_data running')
        self.debug_label.text = 'headx {}\nhandy {}\nturnx {}\nruny {}\n'.format(headx, handy, turnx, runy)

        dict_commands = {'headx':headx, 'handy':handy, 'turnx':turnx, 'runy':runy}
        print(dict_commands)

        str_commands = 'http://'+str(robot_host)+'/?'

        for item in dict_commands:
            print(item,
                  dict_commands[item],
                  type(dict_commands[item])
                  )
            # if dict_commands[item] !='z':
            #     str_commands += item +\
            #                     '=' + \
            #                     dict_commands[item] + \
            #                     '&'

            # add normalization
            if dict_commands[item] != 'z':
                str_commands += item +\
                                '=' + \
                                str('{0:.2f}'.format((float(dict_commands[item]) + 1) / 2)) +\
                                '&'
                                # str((float(dict_commands[item]) + 1) / 2) +\
        print('str_commands: {}'.format(str_commands))

        # for query http://192.168.101.102/?headx=0.5&handy=0.5&turnx=0.5&runy=0.5

        # turnx = (float(x) + 1) / 2
        try:
            client_socket = socket.socket()  # instantiate
            client_socket.connect((robot_host, robot_port))  # connect to the server
        #     message = 'http://192.168.4.1/?turnx=' + str(turnx)  # take input
            client_socket.send(str_commands.encode())  # encode than send message
        #
            client_socket.close()  # close the connection
        #     # sleep(3)
        #     # time.sleep(0.02)
        #     #
            time.sleep(0.05)
            print('sent OK {} sent'.format(str_commands))
            # send_status = 'sent ok' + str(turnx)
        except:
            print('turnx not sent {}'.format(turnx))
        #     send_status += 'error sending turnx' + str(turnx)




class RoboJoystickApp(App):
    def build(self):
        print('BasicApp.running build()')
        return RoboPad()  # goes how ?

        # more basic build
        # return Label(text='Hello')  # goes good


if __name__ == '__main__':
    print('running __main__()')
    RoboJoystickApp().run()
    print('quiting __main__()')

