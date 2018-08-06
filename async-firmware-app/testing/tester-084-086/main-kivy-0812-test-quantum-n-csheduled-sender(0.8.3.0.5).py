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

ver 0.8.2 test version with smooth joystik run
          uses drop commands if "last command seems to be long"
          how long is calculated in def accept_command()

          re-calculates joystik coordinates in def squaredround()

          add Timer

0.8.3.01 - added sliders for accept_command_timeout and velocity_factor adjust
0.8.3.02 - added sliders for timeout_timer_start adjust
0.8.3.02 - allow / disallow coomand by comparing with time latest coomand sent 
'''

from kivy.app import App

from kivy.uix.widget import Widget
from kivy.garden.joystick import Joystick

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider

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
        self.joystickhand = Joystick(size_hint=(.45, .45),
                                     pos_hint={'x': 0.0, 'y': .2},
                                     sticky=True)
        self.add_widget(self.joystickhand)
        self.joystickrun = Joystick(size_hint=(.45, .45),
                                    pos_hint={'x': 0.6, 'y': .2})
        self.joystickhand.bind(pad=self.update_coordinates_hand)

        self.add_widget(self.joystickrun)
        self.joystickrun.bind(pad=self.update_coordinates_run)

        # add some buttons
        self.catchbutton = Button(size_hint=(.15, .15),
                                  pos_hint={'x': .8, 'y': .65},
                                  text='Catch me!')
        self.add_widget(self.catchbutton)
        self.catchbutton.bind(on_press=self.update_catch_release)

        # self.reset_stat_button = Button(size_hint=(.05, .05),
        #                                 pos_hint={'x': .6, 'y': .65},
        #                                 text='reset stat')
        # self.add_widget(self.reset_stat_button)
        # self.reset_stat_button.bind(on_press=self.reset_stat_button)

        # add debug Labels
        self.debug_label = Label(size_hint=(.4, .0),
                                     pos_hint={'x': .2, 'y': .2},
                                     text='message ... ...',)  # multiline=True,)
        self.add_widget(self.debug_label)
        # self.debug_label_hand = Label(size_hint=(.2, .2),
        #                               pos_hint={'x': .1, 'y': .8},
        #                               text='message ... ...',)
        # self.add_widget(self.debug_label_hand)
        # self.debug_label_run = Label(size_hint=(.2, .2),
        #                              pos_hint={'x': .5, 'y': .8},
        #                              text='message ... ...',)  # multiline=True,)
        # self.add_widget(self.debug_label_run)

        # bind joystick



        # bind button


        self.slider_accept_command_timeout = Slider(size_hint=(.4, .03),
                                                    pos_hint={'x': .1,
                                                              'y': .9},
                                                    min=0.02,
                                                    max=0.2,
                                                    value=0.05)
        self.add_widget(self.slider_accept_command_timeout)
        self.slider_accept_command_timeout.bind(value=self.OnSliderAcccepptCommandTiteoutValueChange)

        self.slider_velocity_factor = Slider(size_hint=(.4, .03),
                                                    pos_hint={'x': .1,
                                                              'y': .85},
                                                    min=0.01,
                                                    max=10.0,
                                                    value=0.3)
        self.add_widget(self.slider_velocity_factor)
        self.slider_velocity_factor.bind(value=self.OnSliderVelocityFactorValueChange)

        #  not used , just place holder
        self.slider_timeout_timer_start = Slider(size_hint=(.4, .03),
                                                    pos_hint={'x': .1,
                                                              'y': .8},
                                                    min=0.02,
                                                    max=0.2,
                                                    value=0.11)
        self.add_widget(self.slider_timeout_timer_start)
        self.slider_timeout_timer_start.bind(value=self.OnSliderTimeoutTimerStartValueChange)

        self.accept_command_timeout = 0.05  # 0.6 is too short, broke app!
                            #
                            # for slow motion 0.1 ok ok
                            # for fast motiion 0.0.25 is not enough

        # self.timeout_slow = 0.14
        self.timeout_timer_start = 0.14
        self.velocity_factor = 0.3


        self.old_headx = 0.0
        self.old_handy = 0.0
        self.old_turnx = 0.0
        self.old_runy = 0.0
        self.last_command_compiled_before_send = time.time()
        self.last_command_sent_at = time.time()

        # self.current_hand_pos = {'headx': 0.0, 'handy': 0.0}
        # self.saved_hand_pos = {}
        # self.last_hand_move = {}
        # self.current_run_pos = {'turnx': 0.0, 'runy': 0.0}
        # self.saved_run_pos = {'turnx': 0.0, 'runy': 0.0}
        # self.last_run_move = {}

        self.current_pos = {'headx': 0.0, 'handy': 0.0, 'turnx': 0.0, 'runy': 0.0}
        self.saved_pos = {'headx': 0.0, 'handy': 0.0, 'turnx': 0.0, 'runy': 0.0}

        self.last_move = {'headx': 0.0, 'handy': 0.0, 'turnx': 0.0, 'runy': 0.0}



        self.mean_time_send_command_data = 0.05
        self.counter_send_command_data = 1
        self.counter_commands = 1




        Clock.schedule_interval(self.timer, self.timeout_timer_start)

    def OnSliderAcccepptCommandTiteoutValueChange(self, instance, value):
        print(type(value), value, self.accept_command_timeout)
        self.accept_command_timeout = value

    def OnSliderVelocityFactorValueChange(self, instance, value):
        print(type(value), value, self.velocity_factor)
        self.velocity_factor = value

    def OnSliderTimeoutTimerStartValueChange(self, instance, value):
        print(type(value), value, self.timeout_timer_start)
        self.timeout_timer_start = value

    def update_coordinates_run(self, joystick, pad):

        RUN_Y_STEP = 2  # steps to final acceleration
        RUN_Y_SLEEP = 0.04  # steps to final acceleration


        x = self.squaredround(pad[0])
        y = self.squaredround(pad[1])

        self.current_pos['turnx'] = x
        self.current_pos['runy'] = y

        # self.current_run_pos = {'turnx': x, 'runy': y}  # not working good in mix servo and DC drive
        # self.current_run_pos = {'turnx': x, 'runy': y}  # not working good in mix servo and DC drive
        # self.current_run_pos = {'turnx': x}  # not working good in mix servo and DC drive

        # self.current_run_pos = {'turnx': x, 'runy': y}  # not working good in mix servo and DC drive

        # if self.accept_command(pos=self.current_run_pos):

        if self.accept_command(pos=self.current_pos):
            self.send_command_data(turnx=x, runy=y)

        else:
            pass

    def update_coordinates_hand(self, joystick, pad):

        x = self.squaredround(pad[0])
        y = self.squaredround(pad[1])

        # self.current_hand_pos = {'headx': x, 'handy': y}
        self.current_pos['headx'] = x
        self.current_pos['handy'] = y

        # if self.accept_command(pos=self.current_hand_pos):
        if self.accept_command(pos=self.current_pos):
            self.send_command_data(headx=x, handy=y)
        else:
            pass

    def update_catch_release(self, instance):
        # # print('DBG: button pressed!')
        # catch = catch
        self.send_command_data(catch='catch')

    # def reset_stat_button(self, instance):
    #     # self.mean_time_send_command_data = 0.05
    #     # self.counter_send_command_data = 1
    #     # self.counter_commands = 1
    #     print('reset stat')



    def send_command_data(self, headx='z', handy='z', turnx='z', runy='z', catch='z'):

        before_send_command_data = time.time()

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
        print(dict_commands)

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

                    # remember last command
                    try:
                        # print('DBG remember last command {} {} {}'.format(self.saved_pos[item],
                        #                                                   dict_commands[item],
                        #                                                   self.last_move[item]))
                        self.last_move[item] = abs(self.saved_pos[item] - dict_commands[item])   #
                    except Exception as e:
                        print('ERR saving self.last_move[item] {} {}'.format(type(e), e))

                        pass
                else:
                    str_commands += item + \
                                    '=' + \
                                    'catch' + \
                                    '&'
        # # print('str_commands: {}'.format(str_commands))

        try:
            self.last_command_compiled_before_send = time.time()

            client_socket = socket.socket()  # instantiate
            client_socket.connect((robot_host, robot_port))  # connect to the server
            #     message = 'http://192.168.4.1/?turnx=' + str(turnx)  # take input
            client_socket.send(str_commands.encode())  # encode than send message
            #
            print(str_commands.encode())  # command like :
            # b'http://192.168.4.1/?headx=0.50&runy=0.50&turnx=0.50&handy=0.50&'
            client_socket.close()  # close the connection
            #     # sleep(3)
            #     # time.sleep(0.02)
            #     #
            # time.sleep(0.2)
            # print('sent OK {} sent'.format(str_commands))
            # send_status = 'sent ok' + str(turnx)

            # update send command as saved position

            # self.last_command_compiled_before_send = time.time()

            for item in dict_commands:

                # if dict_commands[item] != 'z' or dict_commands[item] != 'catch':  # gives type error:
                #                               # DBG send_command_data after socket.close 0.0 to <class 'str'> z

                if dict_commands[item] != 'z' and dict_commands[item] != 'catch':  # gives type error:

                    # print('DBG send_command_data after socket.close {} to {} {}'.format(self.saved_pos[item],
                    #                                                                     type(dict_commands[item]),
                    #                                                                     dict_commands[item]))

                    self.saved_pos[item] = dict_commands[item]

            self.mean_time_send_command_data = (self.counter_send_command_data * self.mean_time_send_command_data +
                                                time.time() - before_send_command_data) / \
                                               (self.counter_send_command_data + 1)

            self.counter_send_command_data += 1
            self.last_command_sent_at = time.time()

        except:
            print('ERR: command not sent {}'.format(turnx))
        #     send_status += 'error sending turnx' + str(turnx)


    def timer(self, dt):

        debug_text = "commands counter: {} sent: {}\n" \
                     "mean timeout sending commands: {}\n" \
                     "self.slider_accept_command_timeout: {}\n" \
                     "self.slider_velocity_factor: {}\n" \
                     "self.slider_timeout_timer_start: {}\n" \

        self.debug_label.text = debug_text.format(self.counter_commands,
                                                  str((self.counter_send_command_data / self.counter_commands))[0:5],
                                                  str(self.mean_time_send_command_data)[0:5],
                                                  str(self.accept_command_timeout)[0:5],
                                                  str(self.velocity_factor)[0:5],
                                                  str(self.timeout_timer_start)[0:5])

        # print('timer running \n{}\n{}\n{}'.format(time.time() - self.last_command_compiled_before_send,
        #                                           self.current_hand_pos,
        #                                           self.saved_hand_pos))

        if (time.time() - self.last_command_compiled_before_send) > self.timeout_timer_start: #
            #     # and (self.saved_hand_pos != self.current_hand_pos):
            #
            # # print('Im timer got NEW data:{}'.format(self.current_hand_pos))
            #
            # try:
            #     self.send_command_data(headx=self.current_hand_pos['headx'], handy=self.current_hand_pos['handy'])
            #     self.last_command_compiled_before_send = time.time()
            #     # self.saved_hand_pos = self.current_hand_pos
            #     print('timer raised afterburner {} {}'. format(self.current_hand_pos['headx'],
            #                                                    self.current_hand_pos['handy']))

            if self.current_pos == self.saved_pos:
                # print('DBG timer has no jobs for {} at pos: {}'.format(time.time() - self.last_command_compiled_before_send,
                #                                                        self.saved_pos))
                pass
            else:
                print('DBG timer have job at {} to move to: {}'.format(time.time() - self.last_command_compiled_before_send,
                                                                       self.current_pos))
                try:
                    # self.send_command_data(headx=self.current_hand_pos['headx'],
                    #                        handy=self.current_hand_pos['handy'],
                    #
                    #                        turnx=self.current_run_pos['turnx'],
                    #                        runy=self.current_run_pos['runy'])



                    self.send_command_data(headx=self.current_pos['headx'],
                                           handy=self.current_pos['handy'],

                                           turnx=self.current_pos['turnx'],
                                           runy=self.current_pos['runy'])

                except Exception as e:
                    print('ERR in timer {}, {}'.format(type(e), e))
                    # pass

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

        # ACCEPT_COMMAND_TIMEOUT = 0.06  # 0.6 is too short, broke app!
        #
        #                     for slow motion 0.1 ok ok
        #                     for fast motiion 0.0.25 is not enough
        #
        # velocity = 0.3  # 0.1 too short - joystick freezes broke app!


        hand_timeout_slow = 0.25

        change_factor = 0.2

        next_hand_pos = {}
        # delta_positions = [0.0]
        delta_last_run = [0.0]

        self.counter_commands += 1

        for item in pos:
            if pos[item] != 'z' and pos[item] != 'catch':
                # pass
                # self.saved_hand_pos[item] = pos[item]
                next_hand_pos[item] = pos[item]
                try:
                    # delta_position = abs(next_hand_pos[item] - self.saved_hand_pos[item])
                    delta_last_run.append(self.last_move[item])
                    # print(next_hand_pos[item],
                    #       self.saved_hand_pos[item],
                    #       abs(next_hand_pos[item] - self.saved_hand_pos[item]))

                except Exception as e:
                    print('ERR collecting movements'.format(type(e), e))
                    # pass


        if time.time() > self.last_command_sent_at:
            return False
        else:
            return True


class RoboJoystickApp(App):
    def build(self):
        # print('BasicApp.running build()')
        self.icon = 'robot256.png'
        return RoboPad()  # goes how ?


if __name__ == '__main__':
    # print('running __main__()')
    RoboJoystickApp().run()
    # print('quiting __main__()')

