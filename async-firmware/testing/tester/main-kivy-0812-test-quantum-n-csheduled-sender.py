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

from kivy.clock import Clock

# old_headx = 0.01
# old_handy = 0.01
# old_turnx = 0.01
# old_runy = 0.01

class RoboPad(FloatLayout):
    def __init__(self, **kwargs):
        super(RoboPad, self).__init__(**kwargs)

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

        self.old_headx = 0.0
        self.old_handy = 0.0
        self.old_turnx = 0.0
        self.old_runy = 0.0
        self.last_command_sent_at = 0.0

        self.current_hand_pos = {}
        self.saved_hand_pos = {}
        self.current_run_pos = {}
        self.saved_run_pos = {}

        self.timeout_slow = 1.1

        Clock.schedule_interval(self.timer, self.timeout_slow)

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

        start_ucr = time.time()

        # test for update_coordinates_hand binding test
        # # print('update_coordinates_hand running...')
        # # print(self, joystick, pad)
        # x = str(pad[0])[0:5]
        # y = str(pad[1])[0:5]
        # radians = str(joystick.radians)[0:5]
        # magnitude = str(joystick.magnitude)[0:5]
        # angle = str(joystick.angle)[0:5]
        # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # self.debug_label_run.text = text.format(x, y, radians, magnitude, angle, send_status)

        # without send_status # print just to debug label
        text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}"
        # self.debug_label_hand.text = text.format(x, y, radians, magnitude, angle)
        # self.debug_label.text = text.format(x, y, radians, magnitude, angle)

        # <<<
        # self.send_command_data(headx=x, handy=y)  # original in 0.8.1


        # self.compare_n_send_command_data(headx=x, handy=y)

        # raw_headx = pad[0]
        # aligned_x = raw_headx * 1.4
        # if aligned_x > 0.99 :
        #     x = str(0.99)
        # else:
        #     x = str(aligned_x)[0:4]
        # print(x, raw_headx)
        #

        x = self.squaredround(pad[0])
        y = self.squaredround(pad[1])

        self.current_hand_pos = {'headx': str(x), 'handy': str(y)}

        if self.accept_command(pos=self.current_hand_pos):
            self.send_command_data(headx=x, handy=y)
        else:
            pass

        # if abs(float_headx - self.old_headx) or abs(float_handy - self.old_handy) > change_factor:
        #     print('DBG: above change_factor {} x:{}, y:{}'.format(change_factor,
        #                                                           abs(float_headx - self.old_headx),
        #                                                           abs(float_handy - self.old_handy)
        #                                                           ))
        # for head_x

        # if abs(float_headx - self.old_headx) > change_factor:  # not running good on fast moves

        # if (abs(float_headx - self.old_headx) > change_factor
        #     and (time.time() - self.last_command_sent_at) > hand_timeout) \
        #         or (time.time() - self.last_command_sent_at) > hand_timeout_slow:  #

        # if (abs(float_headx - self.old_headx) > change_factor
        #     and (time.time() - self.last_command_sent_at) > hand_timeout) \
        #         or (time.time() - self.last_command_sent_at) > hand_timeout_slow:  #

        #  add more time for drive move:
        #  hand_timeout + abs(float_headx - self.old_headx)/12.0
        #
        # if (abs(float_headx - self.old_headx) > change_factor
        #     and (time.time() - self.last_command_sent_at) > (hand_timeout + abs(float_headx - self.old_headx)/12.0)) \
        #         or (time.time() - self.last_command_sent_at) > hand_timeout_slow:  #

            # print('DBG: above change_factor headx')

            # print('DBG: above change_factor:{} '
            #       'x:{} '
            #       'delta:{} '
            #       'current TOUT: {}'.format(change_factor,
            #                                 x,
            #                                 # float_headx,
            #                                 abs(float_headx - self.old_headx),
            #                                 hand_timeout + abs(float_headx - self.old_headx) / 8.0
            #                                 ))
            # self.saved_hand_pos = {'headx': x, 'handy': y}
            # self.current_hand_pos = {'headx': x}
            # self.old_headx = str(x)
            # self.last_command_sent_at = time.time()
            # self.send_command_data(headx=str(x))

            # print('last_command_sent_at: {} {}'.format(time.time(), time.clock()))
        # else:
        #     x = 'zz'



        # for hand_y
        # if abs(float_handy - self.old_handy) > change_factor:
        #     print('DBG: above change_factor handy')
        #     self.old_handy = float_handy
        #     print('DBG: above change_factor {} y:{}, delta:{}'.format(change_factor,
        #                                                               y,
        #                                                               # float_handy,
        #                                                               abs(float_handy - self.old_handy)
        #                                                               ))
        #     self.send_command_data(handy=y)
        # # else:
        # #     y = 'zz'

        # if self.accept_command(pos={'headx': x, 'handy': y}):
        #     self.send_command_data(handy=y)

        # print('command x{}, y{}'.format(x, y))

        # self.send_command_data(headx=x, handy=y)

        # self.current_hand_pos = {'headx': str(float_headx), 'handy': y}  # need to add for scheduled

        print(time.time() - start_ucr)

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

        # tuple_commands = (headx, handy, turnx, runy, catch)
        # print(tuple_commands)

        dict_commands = {'headx': headx, 'handy': handy, 'turnx': turnx, 'runy': runy, 'catch': catch}
        # print(dict_commands)

        # for item in dict_commands:
        #     print(item, dict_commands[item])
        #
        # if any(i != 'z' for i in tuple_commands):
        #     print('meaning value  found')

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
                                    str('{0:.2f}'.format((dict_commands[item] + 1) / 2)) + \
                                    '&'
                else:
                    str_commands += item + \
                                    '=' + \
                                    'catch' + \
                                    '&'
        # # print('str_commands: {}'.format(str_commands))

        try:
            self.last_command_sent_at = time.time()

            client_socket = socket.socket()  # instantiate
            client_socket.connect((robot_host, robot_port))  # connect to the server
            #     message = 'http://192.168.4.1/?turnx=' + str(turnx)  # take input
            client_socket.send(str_commands.encode())  # encode than send message
            #
            client_socket.close()  # close the connection
            #     # sleep(3)
            #     # time.sleep(0.02)
            #     #
            # time.sleep(0.2)
            # print('sent OK {} sent'.format(str_commands))
            # send_status = 'sent ok' + str(turnx)

            # update send command as saved position

            # self.last_command_sent_at = time.time()

            for item in dict_commands:
                if dict_commands[item] != 'z' or dict_commands[item] != 'catch':
                    self.saved_hand_pos[item] = dict_commands[item]

        except:
            print('ERR: command not sent {}'.format(turnx))
        #     send_status += 'error sending turnx' + str(turnx)

    # def compare_n_send_command_data(self, headx='z', handy='z', turnx='z', runy='z', catch='z'):
    #
    #     # define some globals
    #
    #     global old_headx
    #     global old_handy
    #     global old_turnx
    #     global old_runy
    #
    #     change_factor = 0.05
    #
    #     print('DBG: headx:{} {} {} {} ()'.format(headx, type(headx), float(headx), float(headx)+1.1, type(float(headx))))
    #     print('DBG: old_headx:{} {} {} {}'.format(old_headx, type(old_headx), float(old_headx), type(float(old_headx))))
    #     print('DBG: abs(float(old_headx)-float(headx) > change_factor: {}, {}').format(float(headx)+1.1, type(float(old_headx)-float(headx)))
    #
    #     # # if abs(float(old_headx)-float(headx)) > change_factor or abs(old_handy-float(handy))>change_factor:  # of course not True alws
    #     # if abs(float(old_headx)-float(headx) > change_factor) > change_factor:  # of course not True alws
    #                                                                                           # //head just
    #     if True:
    #
    #         try:
    #         # if True:
    #         #     print('DBG: headx:{} {} , handy:{} {}'.format(headx, type(headx), handy, type(handy)))
    #
    #             # update saved old_* joystick values
    #
    #             old_headx = headx
    #             old_handy = handy
    #             old_turnx = turnx
    #             old_runy = runy
    #
    #             print('DBG: joystick values re-saved')
    #
    #
    #             robot_host = '192.168.4.1'  # hardcoded robot ip t4m net
    #             robot_port = 80
    #             # # print('send_command_data running')
    #             # self.debug_label.text = 'headx {}\nhandy {}\nturnx {}\nruny {}\ncatch {}'.format(headx,
    #             #                                                                                  handy,
    #             #                                                                                  turnx,
    #             #                                                                                  runy,
    #             #                                                                                  catch)
    #
    #             dict_commands = {'headx': headx, 'handy': handy, 'turnx': turnx, 'runy': runy, 'catch': catch}
    #             # # print(dict_commands)
    #
    #             str_commands = 'http://' + str(robot_host) + '/?'
    #
    #             for item in dict_commands:
    #                 # # print(item,
    #                 #       dict_commands[item],
    #                 #       type(dict_commands[item])
    #                 #       )
    #                 # if dict_commands[item] !='z':
    #                 #     str_commands += item +\
    #                 #                     '=' + \
    #                 #                     dict_commands[item] + \
    #                 #                     '&'
    #
    #                 # add normalization
    #                 if dict_commands[item] != 'z':
    #                     if dict_commands[item] != 'catch':
    #                         str_commands += item + \
    #                                         '=' + \
    #                                         str('{0:.2f}'.format((float(dict_commands[item]) + 1) / 2)) + \
    #                                         '&'
    #                     else:
    #                         str_commands += item + \
    #                                         '=' + \
    #                                         'catch' + \
    #                                         '&'
    #             # # print('str_commands: {}'.format(str_commands))
    #
    #             try:
    #                 client_socket = socket.socket()  # instantiate
    #                 client_socket.connect((robot_host, robot_port))  # connect to the server
    #                 #     message = 'http://192.168.4.1/?turnx=' + str(turnx)  # take input
    #                 client_socket.send(str_commands.encode())  # encode than send message
    #                 #
    #                 client_socket.close()  # close the connection
    #                 #     # sleep(3)
    #                 #     # time.sleep(0.02)
    #                 #     #
    #                 time.sleep(0.2)
    #                 print('sent OK {} sent'.format(str_commands))
    #                 # send_status = 'sent ok' + str(turnx)
    #             except:
    #                 print('ERR: command not sent {}'.format(turnx))
    #             #     send_status += 'error sending turnx' + str(turnx)
    #         except:
    #             pass
    #     else:
    #         print('DBG: joystick changes ignored')

    def timer(self, dt):
        # print('timer running \n{}\n{}\n{}'.format(time.time() - self.last_command_sent_at,
        #                                           self.current_hand_pos,
        #                                           self.saved_hand_pos))

        if (time.time() - self.last_command_sent_at) > self.timeout_slow*2 : #
                # and (self.saved_hand_pos != self.current_hand_pos):

            # print('Im timer got NEW data:{}'.format(self.current_hand_pos))

            try:
                self.send_command_data(headx=self.current_hand_pos['headx'], handy=self.current_hand_pos['handy'])
                self.last_command_sent_at = time.time()
                # self.saved_hand_pos = self.current_hand_pos
                print('timer raised afterburner {} {}'. format(self.current_hand_pos['headx'],
                                                               self.current_hand_pos['handy']))
            except Exception as e:
                # print('ERR in timer {}, {}'.format(type(e), e))
                pass

    def squaredround(self, x):
        import math

        max_x = 0.99
        multiply_factor = 1.4

        sign = lambda y: math.copysign(1, y)
        aligned_x = x * multiply_factor

        if abs(aligned_x) < 0.05:
            return 0.0
        if abs(aligned_x) > 0.99:
            return max_x * sign(aligned_x)
        else:
            return float(str(aligned_x)[0:4])

    def accept_command(self, pos):

        hand_timeout = 0.12  # 0.18 ok  0.17 is too short
                            #
                            # for slow motion 0.1 ok ok
                            # for fast motiion 0.0.25 is not enough

        hand_timeout_slow = 0.25

        change_factor = 0.2

        # <<<
        # self.send_command_data(headx=x, handy=y)  # original in 0.8.1


        # self.compare_n_send_command_data(headx=x, handy=y)

        # raw_headx = pad[0]
        # aligned_x = raw_headx * 1.4
        # if aligned_x > 0.99 :
        #     x = str(0.99)
        # else:
        #     x = str(aligned_x)[0:4]
        # print(x, raw_headx)
        #


        # if abs(float_headx - self.old_headx) or abs(float_handy - self.old_handy) > change_factor:
        #     print('DBG: above change_factor {} x:{}, y:{}'.format(change_factor,
        #                                                           abs(float_headx - self.old_headx),
        #                                                           abs(float_handy - self.old_handy)
        #                                                           ))
        # for head_x

        # if abs(float_headx - self.old_headx) > change_factor:  # not running good on fast moves

        # if (abs(float_headx - self.old_headx) > change_factor
        #     and (time.time() - self.last_command_sent_at) > hand_timeout) \
        #         or (time.time() - self.last_command_sent_at) > hand_timeout_slow:  #

        # if (abs(float_headx - self.old_headx) > change_factor
        #     and (time.time() - self.last_command_sent_at) > hand_timeout) \
        #         or (time.time() - self.last_command_sent_at) > hand_timeout_slow:  #

        #  add more time for drive move:
        #  hand_timeout + abs(float_headx - self.old_headx)/12.0
        #
        # if (abs(float_headx - self.old_headx) > change_factor
        #     and (time.time() - self.last_command_sent_at) > (hand_timeout + abs(float_headx - self.old_headx)/12.0)) \
        #         or (time.time() - self.last_command_sent_at) > hand_timeout_slow:  #

        # check against given params
        print(pos)

        if time.time() - self.last_command_sent_at > hand_timeout:
            return True
        else:
            return False


class RoboJoystickApp(App):
    def build(self):
        # print('BasicApp.running build()')
        self.icon = 'robot256.png'
        return RoboPad()  # goes how ?


if __name__ == '__main__':
    # print('running __main__()')
    RoboJoystickApp().run()
    # print('quiting __main__()')

