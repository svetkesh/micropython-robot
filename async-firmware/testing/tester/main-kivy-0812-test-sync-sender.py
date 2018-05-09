# import kivy
# kivy.require('1.10.0') # replace with your current kivy version !

''' Testing 2 joysticks sending commands
should match main.py (ESP8266 autoloaded v. 0.7.9.1)

manages via
headx, handy, turnx, runy

added delay 0.05 s after sending commands

0.7.9.1

ver 0.7.9.4 add catch (catch-release is working)

ver 0.7.9.7 -dev variant of (0.7.9.4) - preparation for exhibition version (0.7.9.8)
ver 0.7.9.8 - exhibition version, disabled wifi station, just access point
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

import asyncio

from kivy.clock import Clock




class RoboPad(FloatLayout):



    def __init__(self, **kwargs):

        import threading

        super(RoboPad, self).__init__(**kwargs)

        # some trash he-he

        # t = threading.Thread(target=self.some_current_data)
        # t.daemon = True
        # t.start()

        # # print('running super(Gamepad, self).__init__()')

        # joystickhand and joystickrun
        self.joystickhand = Joystick(size_hint=(.4, .4),
                                     pos_hint={'x': 0.0, 'y': .2},
                                     sticky=True)
        self.add_widget(self.joystickhand)
        self.joystickrun = Joystick(size_hint=(.4, .4),
                                    pos_hint={'x': 0.6, 'y': .2})
        self.add_widget(self.joystickrun)

        # add some buttons
        self.catchbutton = Button(size_hint=(.15, .15),
                                  pos_hint={'x': .8, 'y': .65},
                                  text='Catch me!')
        self.add_widget(self.catchbutton)

        # add debug Labels
        # self.debug_label = Label(size_hint=(.2, .2),
        #                              pos_hint={'x': .8, 'y': .8},
        #                              text='message ... ...',)  # multiline=True,)
        # self.add_widget(self.debug_label)
        # self.debug_label_hand = Label(size_hint=(.2, .2),
        #                               pos_hint={'x': .1, 'y': .8},
        #                               text='message ... ...',)
        # self.add_widget(self.debug_label_hand)
        # self.debug_label_run = Label(size_hint=(.2, .2),
        #                              pos_hint={'x': .5, 'y': .8},
        #                              text='message ... ...',)  # multiline=True,)
        # self.add_widget(self.debug_label_run)

        # bind joystick
        self.joystickrun.bind(pad=self.update_coordinates_run)
        self.joystickhand.bind(pad=self.update_coordinates_hand)

        # bind button
        self.catchbutton.bind(on_press=self.update_catch_release)

        # self.global_reader()

        self.current_hand_pos = {}
        self.saved_hand_pos = {}
        self.current_run_pos = {}
        self.saved_run_pos = {}

        Clock.schedule_interval(self.timer, 0.1)

    def update_coordinates_run(self, joystick, pad):
        # test for joystickrun binding test
        # # print('update_coordinates_run ...')
        # # print(self, joystick, pad)
        x = str(pad[0])[0:5]
        y = str(pad[1])[0:5]
        radians = str(joystick.radians)[0:5]
        magnitude = str(joystick.magnitude)[0:5]
        angle = str(joystick.angle)[0:5]
        # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # self.debug_label_run.text = text.format(x, y, radians, magnitude, angle, send_status)

        # without send_status # print just to debug label
        text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}"
        # self.debug_label_run.text = text.format(x, y, radians, magnitude, angle)
        # self.debug_label.text = text.format(x, y, radians, magnitude, angle)
        self.send_command_data(turnx=x, runy=y)

    def update_coordinates_hand(self, joystick, pad):

        global some_current_data

        # test for update_coordinates_hand binding test
        # # print('update_coordinates_hand running...')
        # # print(self, joystick, pad)
        x = str(pad[0])[0:5]
        y = str(pad[1])[0:5]
        radians = str(joystick.radians)[0:5]
        magnitude = str(joystick.magnitude)[0:5]
        angle = str(joystick.angle)[0:5]
        # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # self.debug_label_run.text = text.format(x, y, radians, magnitude, angle, send_status)

        # without send_status # print just to debug label
        text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}"
        # self.debug_label_hand.text = text.format(x, y, radians, magnitude, angle)
        # self.debug_label.text = text.format(x, y, radians, magnitude, angle)

        # <<<
        # self.send_command_data(headx=x, handy=y)  #  test not sending data but save to global some_current_data

        self.current_hand_pos = {'headx':x, 'handy':y}
        # print('DBG: some_current_data : {}'.format(self.some_current_data))

    def update_catch_release(self, instance):
        # # print('DBG: button pressed!')
        # catch = catch
        self.send_command_data(catch='catch')

    def send_command_data(self, headx='z', handy='z', turnx='z', runy='z', catch='z'):
        robot_host = '192.168.4.1'  # hardcoded robot ip t4m net
        robot_port = 80
        # # print('send_command_data running')
        # self.debug_label.text = 'headx {}\nhandy {}\nturnx {}\nruny {}\ncatch {}'.format(headx,
        #                                                                                  handy,
        #                                                                                  turnx,
        #                                                                                  runy,
        #                                                                                  catch)

        dict_commands = {'headx': headx, 'handy': handy, 'turnx': turnx, 'runy': runy, 'catch': catch}
        # # print(dict_commands)

        str_commands = 'http://' + str(robot_host) + '/?'

        for item in dict_commands:
            # # print(item,
            #       dict_commands[item],
            #       type(dict_commands[item])
            #       )
            # if dict_commands[item] !='z':
            #     str_commands += item +\
            #                     '=' + \
            #                     dict_commands[item] + \
            #                     '&'

            # add normalization
            if dict_commands[item] != 'z':
                if dict_commands[item] != 'catch':
                    str_commands += item + \
                                    '=' + \
                                    str('{0:.2f}'.format((float(dict_commands[item]) + 1) / 2)) + \
                                    '&'
                else:
                    str_commands += item + \
                                    '=' + \
                                    'catch' + \
                                    '&'
        # # print('str_commands: {}'.format(str_commands))

        try:
            client_socket = socket.socket()  # instantiate
            client_socket.connect((robot_host, robot_port))  # connect to the server
            #     message = 'http://192.168.4.1/?turnx=' + str(turnx)  # take input
            print(client_socket.gettimeout())
            client_socket.send(str_commands.encode())  # encode than send message
            #
            client_socket.close()  # close the connection
            #     # sleep(3)
            #     # time.sleep(0.02)
            #     #
            time.sleep(0.2)
            print('sent OK {} sent'.format(str_commands))
            # send_status = 'sent ok' + str(turnx)
        except:
            print('ERR: command not sent {}'.format(turnx))
        #     send_status += 'error sending turnx' + str(turnx)

    def global_reader(self, some_current_data):
        # global some_current_data
        while True:
            print('DBG: global_reader says: some_current_data is : '.format(some_current_data))
            time.sleep(0.5)

    def timer(self, dt):
        if self.saved_hand_pos == self.current_hand_pos:
            print(print('Im timer got OLD data:{}'.format(self.saved_hand_pos)))

        else:
            print(print('Im timer got NEW data:{}'.format(self.current_hand_pos)))
            self.saved_hand_pos = self.current_hand_pos
            self.send_command_data(headx=self.saved_hand_pos['headx'], handy=self.saved_hand_pos['handy'])


class RoboJoystickApp(App):
    def build(self):
        # print('BasicApp.running build()')
        self.icon = 'robot256.png'
        return RoboPad()  # goes how ?


async def global_reader(some_current_data):
    # global some_current_data
    print('DBG: global_reader started')
    # while True:
    print('DBG: global_reader says: some_current_data is : '.format(some_current_data))
    # time.sleep(0.5)
    await asyncio.sleep(0.5)


if __name__ == '__main__':
    print('running __main__()')
    # global_reader()

    # loop = asyncio.get_event_loop()
    # loop.run_forever(
    #     asyncio.gather(global_reader(some_current_data),
    #                    RoboJoystickApp().run())
    # )
    # loop.close()

    RoboJoystickApp().run()

    # global_reader()
    print('quiting __main__()')



