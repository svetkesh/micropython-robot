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
0.8.3.02 - allow / disallow coomand by comparing with time latest command sent
0.8.3.0.5  changed control layout
0.8.3.0.5  add dance button

0.8.3.0.8 - operates only integers, suits 0.8.3.0.8 only
0.8.3.0.9 - added gears suits 0.8.3.0.9 only for gear adjustment
0.8.3.0.11 - changed command format and command compilation
0.8.3.0.13 - dbg ver of v.0.8.3.0.1
             changer subject of sending
             and principles of allowing command to be send
             # self.stored_command = {}   # updated storage for commands
             # self.delayed_command = {}  # updated storage for commands

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
        self.joystickhand = Joystick(size_hint=(.5, .5),
                                     pos_hint={'x': .0, 'y': .0},
                                     sticky=True)
        self.add_widget(self.joystickhand)
        self.joystickrun = Joystick(size_hint=(.5, .5),
                                    pos_hint={'x': .5, 'y': .0})
        self.joystickhand.bind(pad=self.update_coordinates_hand)

        self.add_widget(self.joystickrun)
        self.joystickrun.bind(pad=self.update_coordinates_run)

        # add some buttons
        self.catchbutton = Button(size_hint=(.3, .1),
                                  pos_hint={'x': .7, 'y': .9},
                                  text='Catch me!')
        self.add_widget(self.catchbutton)
        self.catchbutton.bind(on_press=self.update_catch_release)

        self.dance_button = Button(size_hint=(.2, .1),
                                  pos_hint={'x': .4, 'y': .9},
                                  text='Dance!')
        self.add_widget(self.dance_button)
        self.dance_button.bind(on_press=self.update_dance)

        self.hiphop_dance = Button(size_hint=(.2, .1),
                                  pos_hint={'x': .1, 'y': .9},
                                  text='hip-hop!')
        self.add_widget(self.hiphop_dance)
        self.hiphop_dance.bind(on_press=self.update_hiphop)

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
        # self.add_widget(self.slider_accept_command_timeout)

        self.slider_accept_command_timeout.bind(value=self.OnSliderAcccepptCommandTiteoutValueChange)

        self.slider_velocity_factor = Slider(size_hint=(.4, .03),
                                                    pos_hint={'x': .1,
                                                              'y': .85},
                                                    min=0.01,
                                                    max=10.0,
                                                    value=0.3)
        # self.add_widget(self.slider_velocity_factor)

        self.slider_velocity_factor.bind(value=self.OnSliderVelocityFactorValueChange)

        #  not used , just place holder
        self.slider_timeout_timer_start = Slider(size_hint=(.4, .03),
                                                    pos_hint={'x': .1,
                                                              'y': .8},
                                                    min=0.02,
                                                    max=0.2,
                                                    value=0.11)
        # self.add_widget(self.slider_timeout_timer_start)

        self.slider_timeout_timer_start.bind(value=self.OnSliderTimeoutTimerStartValueChange)


        self.slider_gear_factor = Slider(size_hint=(.4, .03),
                                                    pos_hint={'x': .1,
                                                              'y': .8},
                                                    min=1,
                                                    max=5,
                                                    value=3)
        self.add_widget(self.slider_gear_factor)

        self.slider_gear_factor.bind(value=self.OnSliderGearFactorValueChange)

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

        self.mean_time_send_command_data = 0.0
        self.counter_send_command_data = 1
        self.counter_commands = 1

        self.dance = False
        self.hiphop = 1

        self.gear = 3

        self.robot_host = '192.168.4.1'  # hardcoded robot ip t4m net
        self.robot_port = 80

        self.current_pos = {'headx': 0.0, 'handy': 0.0, 'turnx': 0.0, 'runy': 0.0, 'gear': self.gear}
        self.saved_pos = {'headx': 0.0, 'handy': 0.0, 'turnx': 0.0, 'runy': 0.0, 'gear': self.gear}

        self.last_move = {'headx': 0.0, 'handy': 0.0, 'turnx': 0.0, 'runy': 0.0, 'gear': self.gear}

        # self.saved_command = {'gear': self.gear}

        self.current_command = {}   # updated storage for commands
        self.stored_command = {}   # updated storage for commands
        self.delayed_command = {}  # updated storage for commands
        self.command_sent = True

        # self.SERVO_MIN = 35   # real servo min-max
        # self.SERVO_MAX = 125
        self.SERVO_MIN = 40     # compatible with 0.8.3.0.9
        self.SERVO_MAX = 117
        self.servo_center = self.SERVO_MAX - self.SERVO_MIN
        self.SERVO_NEAR_ZERO = 0.03
        self.SERVO_FACTOR = 1.3


        Clock.schedule_interval(self.timer_with_saved_params, self.timeout_timer_start)  # start afterburner

    def OnSliderAcccepptCommandTiteoutValueChange(self, instance, value):
        # self.command_sent = False
        # print(type(value), value, self.accept_command_timeout)
        self.accept_command_timeout = value

    def OnSliderVelocityFactorValueChange(self, instance, value):
        # self.command_sent = False
        # print(type(value), value, self.velocity_factor)
        self.velocity_factor = value

    def OnSliderGearFactorValueChange(self, instance, value):
        # self.command_sent = False
        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands
        # print(type(value), value, self.gear)
        self.gear = round(value)
        # self.send_command_data(gear=self.gear)
        self.saved_command['gear'] = self.gear

    def OnSliderTimeoutTimerStartValueChange(self, instance, value):
        # self.command_sent = False
        # print(type(value), value, self.timeout_timer_start)
        self.timeout_timer_start = value

    def update_coordinates_run(self, joystick, pad):
        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands

        print('DBG start update_coordinates_run : {}'.format('new move'))

        # self.command_sent = False
        # # test for joystickrun binding test
        # # # print('update_coordinates_run ...')
        # # # print(self, joystick, pad)
        # x = str(pad[0])[0:5]
        # y = str(pad[1])[0:5]
        # radians = str(joystick.radians)[0:5]
        # magnitude = str(joystick.magnitude)[0:5]
        # angle = str(joystick.angle)[0:5]
        # # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}\nsend data status: {}"
        # # self.debug_label_run.text = text.format(x, y, radians, magnitude, angle, send_status)
        #
        # # without send_status # print just to debug label
        # text = "x: {}\ny: {}\nradians: {}\nmagnitude: {}\nangle: {}"
        # # self.debug_label_run.text = text.format(x, y, radians, magnitude, angle)
        # # self.debug_label.text = text.format(x, y, radians, magnitude, angle)
        # self.send_command_data(turnx=x, runy=y)

        # RUN_Y_STEP = 2  # steps to final acceleration
        # RUN_Y_SLEEP = 0.04  # steps to final acceleration

        # x = self.squaredround(pad[0])
        # y = self.squaredround(pad[1])

        # self.current_pos['turnx'] = x
        # self.current_pos['runy'] = y

        # self.current_run_pos = {'turnx': x, 'runy': y}  # not working good in mix servo and DC drive
        # self.current_run_pos = {'turnx': x, 'runy': y}  # not working good in mix servo and DC drive
        # self.current_run_pos = {'turnx': x}  # not working good in mix servo and DC drive

        # self.current_run_pos = {'turnx': x, 'runy': y}  # not working good in mix servo and DC drive

        # if self.accept_command(pos=self.current_run_pos):

        # if self.accept_command(pos=self.current_pos):
        #     self.send_command_data(turnx=x, runy=y)
        #
        #
        #     # # smooth start not working well
        #     # self.send_command_data(turnx=x)
        #     #
        #     # for run_step in range(RUN_Y_STEP, 1, -1):
        #     #     try:
        #     #
        #     #         # print('DBG run_step {} {} {} {} {} {}'.format(
        #     #         #     type(self.saved_pos['runy']),
        #     #         #     self.saved_pos['runy'],
        #     #         #     type(y),
        #     #         #     y,
        #     #         #     type(self.saved_pos['runy']),
        #     #         #     self.saved_pos
        #     #         # ))
        #     #
        #     #         self.send_command_data(runy=self.saved_pos['runy'] + (y -self.saved_pos['runy']) / run_step)
        #     #
        #     #         time.sleep(RUN_Y_SLEEP)
        #     #
        #     #         print('DBG run_step {} {} {}'.format(run_step,
        #     #                                              self.saved_pos['runy'],
        #     #                                              self.saved_pos['runy'] +
        #     #                                              (self.saved_pos['runy'] - y) / run_step))   # RUN_Y_STEP
        #     #     except Exception as e:
        #     #         print('ERR run_step err: {} {}'.format(type(e), e))
        #     #     # self.send_command_data(turnx=x, runy=y)
        #     #
        #     # # self.send_command_data(turnx=x, runy=y)
        #
        # else:
        #     pass

        # recreate self.current_command
        self.current_command = {}

        x = self.squaredround(pad[0])
        y = self.squaredround(pad[1])

        self.current_command['turnx'] = self.recalculate_servo_position(x)
        self.current_command['runy'] = self.recalculate_dc_position(y)

        print('DBG start update_coordinates_run self.current_command: {}'.format(self.current_command))

        if self.accept_command_with_saved_params(self.current_command):
            # self.command_sent = False
            print('DBG update_coordinates_run calls send_command_data_({}): '.format(self.current_command))
            self.send_command_data_with_saved_params(self.current_command)
        else:
            print('DBG update_coordinates_run not allowed to call send_command: {}'.format(self.current_command))
            # pass


        # # smooth run stepper (
        #
        # for run_step in range(RUN_Y_STEP, 1, -1):
        #     try:
        #
        #         # print('DBG run_step {} {} {} {} {} {}'.format(
        #         #     type(self.saved_pos['runy']),
        #         #     self.saved_pos['runy'],
        #         #     type(y),
        #         #     y,
        #         #     type(self.saved_pos['runy']),
        #         #     self.saved_pos
        #         # ))
        #
        #         self.send_command_data(runy=self.saved_pos['runy'] + (self.saved_pos['runy'] + y) / run_step)
        #
        #         # print('DBG run_step {} {} {}'.format(run_step,
        #         #                               self.saved_pos['runy'],
        #         #                               runy=self.saved_pos['runy'] + (self.saved_pos['runy'] - y) / run_step))
        #     except Exception as e:
        #         print('run_step err: {} {}'.format(type(e), e))
        #     # self.send_command_data(turnx=x, runy=y)
        #
        #     # self.current_run_pos = {'runy': y}



        # self.current_run_pos = {'runy': y}

    def update_coordinates_hand(self, joystick, pad):
        # self.command_sent = False
        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands

        RUN_Y_STEP = 2  # steps to final acceleration
        RUN_Y_SLEEP = 0.04  # steps to final acceleration

        x = self.squaredround(pad[0])
        y = self.squaredround(pad[1])

        self.current_pos['headx'] = x
        self.current_pos['handy'] = y

        if self.command_sent:

            self.saved_command['headx'] = self.recalculate_servo_position(x)
            self.saved_command['handy'] = self.recalculate_servo_position(y)
            self.command_sent = False
            self.send_command_data_with_saved_params()
        else:
            pass

    def update_catch_release(self, instance):
        # self.command_sent = False
        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands

        # # print('DBG: button pressed!')
        # catch = catch
        if self.command_sent:

            self.saved_command['catch'] = 'catch'
            self.command_sent = False
            self.send_command_data_with_saved_params()

    def update_hiphop(self, instance):
        self.hiphop = 50

    # self.dance
    def update_dance(self, instance):
        # self.command_sent = False
        import random
        print('DBG: self.dance: {}'.format(self.dance))

        if self.dance:

            def generate_commands(timeout=0, cycle=0):
                
                self.saved_command['headx']=random.choice(['z', random.random()])
                self.saved_command['handy']=random.choice(['z', random.random()])
                self.saved_command['turnx']=random.choice(['z', random.random()])
                                  # runy=random.choice(['z', random.random()]),
                self.saved_command['runy']=random.choice(['z', 'z'])
                self.saved_command['catch']=random.choice(['z', 'catch'])
                
                self.send_command_data_with_saved_params()


            def cycle_timeouted():
                # initial timeout 0.5 s: 0.2  0.2  0.2
                #  ini_timeout = 50      20   50   100
                #  step_timeout = 100    100  250  500

                ini_timeout = 100
                step_timeout = 500

                count = 1

                for timeout in range(ini_timeout, 1, -1):
                    print('DBG: current timeout: {}, count: {}'.format(timeout / step_timeout, count))
                    for cycle in range(0, 10000):
                        # print('DBG: current timeout: {}, cycle: {}'.format(timeout / step_timeout, cycle))

                        if time.time() > self.last_command_sent_at:
                            generate_commands(timeout, cycle)

                        generate_commands(timeout, cycle)
                        time.sleep(random.randint(1, 10) / self.hiphop)
                        count += 1

            cycle_timeouted()

        self.dance = not self.dance

        # self.send_command_data(catch='catch')

    # def reset_stat_button(self, instance):
    #     # self.mean_time_send_command_data = 0.05
    #     # self.counter_send_command_data = 1
    #     # self.counter_commands = 1
    #     print('reset stat')

    # def send_command_data(self, headx='z', handy='z', turnx='z', runy='z', catch='z', gear='z'):
    #
    #     # self.stored_command = {}   # updated storage for commands
    #     # self.delayed_command = {}  # updated storage for commands
    #
    #     print('Started send_command_data')
    #
    #     before_send_command_data = time.time()
    #
    #     robot_host = '192.168.4.1'  # hardcoded robot ip t4m net
    #     robot_port = 80
    #     # # print('send_command_data running')
    #     # self.debug_label.text = 'headx {}\nhandy {}\nturnx {}\nruny {}\ncatch {}'.format(headx,
    #     #                                                                                  handy,
    #     #                                                                                  turnx,
    #     #                                                                                  runy,
    #     #                                                                                  catch)
    #
    #     # tuple_commands = (headx, handy, turnx, runy, catch)
    #     # print(tuple_commands)
    #
    #     dict_commands = {'headx': headx, 'handy': handy, 'turnx': turnx, 'runy': runy, 'catch': catch, 'gear': gear}
    #     print('DBG dict_commands: {}'.format(dict_commands))
    #
    #     # for item in dict_commands:
    #     #     print(item, dict_commands[item])
    #     #
    #     # if any(i != 'z' for i in tuple_commands):
    #     #     print('meaning value  found')
    #
    #     str_commands = 'http://' + str(robot_host) + '/?'
    #
    #     for item in dict_commands:
    #         # # print(item,
    #         #       dict_commands[item],
    #         #       type(dict_commands[item])
    #         #       )
    #         # if dict_commands[item] !='z':
    #         #     str_commands += item +\
    #         #                     '=' + \
    #         #                     dict_commands[item] + \
    #         #                     '&'
    #
    #         if dict_commands[item] != 'z':
    #
    #             if dict_commands[item] == 'catch':
    #                 str_commands += item + \
    #                                 '=' + \
    #                                 'catch' + \
    #                                 '&'
    #
    #             # if dict_commands[item] != 'catch':
    #             else:
    #
    #                 # pre- 0.8.3.3.8
    #                 # str_commands += item + \
    #                 #                 '=' + \
    #                 #                 str('{0:.2f}'.format((dict_commands[item] + 1) / 2)) + \
    #                 #                 '&'
    #
    #                 if item == 'gear': # new in 0.8.3.0.9 for gear
    #                     str_commands += item + '=' + str('{}'.format(dict_commands[item])) + '&'
    #                     # print('DBG dict_commands[item] == \'gear\' {}'.format(str_commands))
    #
    #                 else:
    #                     # new in 0.8.3.3.8 ,
    #                     # calculates integer values for ESP
    #                     str_commands += item + '=' + str('{}'.format(int((dict_commands[item]+1)/2 * 75 + 40))) + '&'
    #                     # print('DBG else -- dict_commands[item] == \'gear\' {}'.format(str_commands))
    #
    #                 # print('DBG: formatting values {} -> {}'.format(dict_commands[item], (int(dict_commands[item]*100))))
    #
    #                 # remember last command
    #             try:
    #                 # print('DBG remember last command {} {} {}'.format(self.saved_pos[item],
    #                 #                                                   dict_commands[item],
    #                 #                                                   self.last_move[item]))
    #                 self.last_move[item] = abs(self.saved_pos[item] - dict_commands[item])   #
    #             except Exception as e:
    #                 print('ERR saving self.last_move[item] {} {}'.format(type(e), e))
    #
    #                     # pass
    #
    #     # # print('str_commands: {}'.format(str_commands))
    #
    #     try:
    #         self.last_command_compiled_before_send = time.time()
    #
    #         self.command_sent = False
    #
    #         client_socket = socket.socket()  # instantiate
    #         client_socket.connect((robot_host, robot_port))  # connect to the server
    #         #     message = 'http://192.168.4.1/?turnx=' + str(turnx)  # take input
    #         client_socket.send(str_commands.encode())  # encode than send message
    #         #
    #         print(str_commands.encode())  # command like :
    #         # b'http://192.168.4.1/?headx=0.50&runy=0.50&turnx=0.50&handy=0.50&'
    #         client_socket.close()  # close the connection
    #         #     # sleep(3)
    #         #     # time.sleep(0.02)
    #         #     #
    #         # time.sleep(0.2)
    #         # print('sent OK {} sent'.format(str_commands))
    #         # send_status = 'sent ok' + str(turnx)
    #
    #         # update send command as saved position
    #
    #         # self.last_command_compiled_before_send = time.time()
    #
    #         for item in dict_commands:
    #
    #             # if dict_commands[item] != 'z' or dict_commands[item] != 'catch':  # gives type error:
    #             #                               # DBG send_command_data after socket.close 0.0 to <class 'str'> z
    #
    #             if dict_commands[item] != 'z' and dict_commands[item] != 'catch':  # gives type error:
    #
    #                 # print('DBG send_command_data after socket.close {} to {} {}'.format(self.saved_pos[item],
    #                 #                                                                     type(dict_commands[item]),
    #                 #                                                                     dict_commands[item]))
    #
    #                 self.saved_pos[item] = dict_commands[item]
    #
    #         self.mean_time_send_command_data = (self.counter_send_command_data * self.mean_time_send_command_data +
    #                                             time.time() - before_send_command_data) / \
    #                                            (self.counter_send_command_data + 1)
    #
    #         self.counter_send_command_data += 1
    #         self.last_command_sent_at = time.time()
    #
    #     except:
    #         print('ERR: command not sent {}'.format(turnx))
    #     #     send_status += 'error sending turnx' + str(turnx)

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

    # def timer(self, dt):
    #
    #     debug_text = "commands counter: {} sent: {}\n" \
    #                  "mean timeout sending commands: {}\n" \
    #                  "self.slider_accept_command_timeout: {}\n" \
    #                  "self.slider_velocity_factor: {}\n" \
    #                  "self.slider_timeout_timer_start: {}\n" \
    #                  "self.gear: {}\n" \
    #
    #     self.debug_label.text = debug_text.format(self.counter_commands,
    #                                               str((self.counter_send_command_data / self.counter_commands))[0:5],
    #                                               str(self.mean_time_send_command_data)[0:5],
    #                                               str(self.accept_command_timeout)[0:5],
    #                                               str(self.velocity_factor)[0:5],
    #                                               str(self.timeout_timer_start)[0:5],
    #                                               str(self.gear))
    #
    #     # print('timer running \n{}\n{}\n{}'.format(time.time() - self.last_command_compiled_before_send,
    #     #                                           self.current_hand_pos,
    #     #                                           self.saved_hand_pos))
    #
    #     if (time.time() - self.last_command_compiled_before_send) > self.timeout_timer_start: #
    #         #     # and (self.saved_hand_pos != self.current_hand_pos):
    #         #
    #         # # print('Im timer got NEW data:{}'.format(self.current_hand_pos))
    #         #
    #         # try:
    #         #     self.send_command_data(headx=self.current_hand_pos['headx'], handy=self.current_hand_pos['handy'])
    #         #     self.last_command_compiled_before_send = time.time()
    #         #     # self.saved_hand_pos = self.current_hand_pos
    #         #     print('timer raised afterburner {} {}'. format(self.current_hand_pos['headx'],
    #         #                                                    self.current_hand_pos['handy']))
    #
    #         if self.current_pos == self.saved_pos:
    #             # print('DBG timer has no jobs for {} at pos: {}'.format(time.time() - self.last_command_compiled_before_send,
    #             #                                                        self.saved_pos))
    #             pass
    #         else:
    #             print('DBG timer have job at {} to move to: {}'.format(time.time() - self.last_command_compiled_before_send,
    #                                                                    self.current_pos))
    #             try:
    #                 # self.send_command_data(headx=self.current_hand_pos['headx'],
    #                 #                        handy=self.current_hand_pos['handy'],
    #                 #
    #                 #                        turnx=self.current_run_pos['turnx'],
    #                 #                        runy=self.current_run_pos['runy'])
    #
    #
    #
    #                 self.send_command_data(headx=self.current_pos['headx'],
    #                                        handy=self.current_pos['handy'],
    #
    #                                        turnx=self.current_pos['turnx'],
    #                                        runy=self.current_pos['runy'])
    #
    #             except Exception as e:
    #                 print('ERR in timer {}, {}'.format(type(e), e))
    #                 # pass

    def timer_with_saved_params(self, dt):

        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands

        debug_text = "commands counter: {} sent: {}\n" \
                     "mean timeout sending commands: {}\n" \
                     "self.slider_accept_command_timeout: {}\n" \
                     "self.slider_velocity_factor: {}\n" \
                     "self.slider_timeout_timer_start: {}\n" \
                     "self.gear: {}\n" \

        self.debug_label.text = debug_text.format(self.counter_commands,
                                                  str((self.counter_send_command_data / self.counter_commands))[0:5],
                                                  str(self.mean_time_send_command_data)[0:5],
                                                  str(self.accept_command_timeout)[0:5],
                                                  str(self.velocity_factor)[0:5],
                                                  str(self.timeout_timer_start)[0:5],
                                                  str(self.gear))

        # if self.command_sent:
        #     print('DBG timer_with_saved_params saved_command "len":{},'
        #           ' "if?" {} ,'
        #           ' {}'.format(len(self.saved_command),
        #                        True if self.saved_command else False,
        #                        self.saved_command))
        #     print('DBG timer_with_saved_params have no jobs')
        #     # return False
        # else:
        #     print('DBG timer_with_saved_params saved_command "len":{},'
        #           ' "if?" {} ,'
        #           ' {}'.format(len(self.saved_command),
        #                        True if self.saved_command else False,
        #                        self.saved_command))
        #     print('DBG timer_with_saved_params have some jobs')
        #     self.send_command_data_with_saved_params()
        #     # return True
        #     #

        # if self.saved_command:
        #     print('DBG timer_with_saved_params saved_command "len":{},'
        #           ' "if?" {} ,'
        #           ' {}'.format(len(self.saved_command),
        #                        True if self.saved_command else False,
        #                        self.saved_command))
        #     print('DBG timer_with_saved_params have some jobs')
        #     # return False
        #     # self.send_command_data_with_saved_params()  # temporally  disable sending command
        #     # self.saved_command = {}
        # else:
        #     print('DBG timer_with_saved_params saved_command "len":{},'
        #           ' "if?" {} ,'
        #           ' {}'.format(len(self.saved_command),
        #                        True if self.saved_command else False,
        #                        self.saved_command))
        #     print('DBG timer_with_saved_params have no jobs')
        #
        #     # return True

    def squaredround(self, x):
        import math

        # print('DBG squaredround x: {}'.format(x))
        max_x = 0.99
        multiply_factor = 1.3

        sign = lambda y: math.copysign(1, y)
        aligned_x = x * multiply_factor

        if abs(aligned_x) < 0.05:
            return 0.0
        if abs(aligned_x) > 0.99:
            return max_x * sign(aligned_x)
        else:
            return float(str(aligned_x)[0:4])

    def recalculate_servo_position(self, x):
        import math

        # self.SERVO_MIN = 40
        # self.SERVO_MAX = 115
        # self.servo_center = 75
        # self.SERVO_NEAR_ZERO = 0.03
        # self.SERVO_FACTOR = 1.3

        max_x = 0.99
        multiply_factor = 1.4

        sign = lambda y: math.copysign(1, y)
        aligned_x = x * multiply_factor

        if abs(aligned_x) < self.SERVO_NEAR_ZERO:
            return self.servo_center
        elif abs(aligned_x) > 0.99:
            normalized_x = max_x * sign(aligned_x)
        else:
            normalized_x = float(str(aligned_x)[0:4])

        return int((normalized_x + 1) / 2 * self.servo_center + self.SERVO_MIN)

    def recalculate_dc_position(self, x):
        import math

        max_x = 0.99
        multiply_factor = 1.1
        near_zero = 0.03

        dc_min = self.SERVO_MIN
        dc_max = self.SERVO_MAX
        dc_center = self.servo_center

        sign = lambda y: math.copysign(1, y)
        aligned_x = x * multiply_factor

        if abs(aligned_x) < near_zero:
            # normalized_x = 0.0
            return dc_center
        elif abs(aligned_x) > 0.99:
            normalized_x = max_x * sign(aligned_x)
            return int((normalized_x + 1) / 2 * dc_center + dc_min)
        else:
            # normalized_x = float(str(aligned_x)[0:4])
            normalized_x = aligned_x
            return int((normalized_x + 1) / 2 * dc_center + dc_min)

    # def accept_command(self, pos):
    #
    #     # ACCEPT_COMMAND_TIMEOUT = 0.06  # 0.6 is too short, broke app!
    #     #
    #     #                     for slow motion 0.1 ok ok
    #     #                     for fast motiion 0.0.25 is not enough
    #     #
    #     # velocity = 0.3  # 0.1 too short - joystick freezes broke app!
    #
    #
    #     hand_timeout_slow = 0.25
    #
    #     change_factor = 0.2
    #
    #     next_hand_pos = {}
    #     # delta_positions = [0.0]
    #     delta_last_run = [0.0]
    #
    #     self.counter_commands += 1
    #
    #     # <<<
    #     # self.send_command_data(headx=x, handy=y)  # original in 0.8.1
    #
    #
    #     # self.compare_n_send_command_data(headx=x, handy=y)
    #
    #     # raw_headx = pad[0]
    #     # aligned_x = raw_headx * 1.4
    #     # if aligned_x > 0.99 :
    #     #     x = str(0.99)
    #     # else:
    #     #     x = str(aligned_x)[0:4]
    #     # print(x, raw_headx)
    #     #
    #
    #
    #     # if abs(float_headx - self.old_headx) or abs(float_handy - self.old_handy) > change_factor:
    #     #     print('DBG: above change_factor {} x:{}, y:{}'.format(change_factor,
    #     #                                                           abs(float_headx - self.old_headx),
    #     #                                                           abs(float_handy - self.old_handy)
    #     #                                                           ))
    #     # for head_x
    #
    #     # if abs(float_headx - self.old_headx) > change_factor:  # not running good on fast moves
    #
    #     # if (abs(float_headx - self.old_headx) > change_factor
    #     #     and (time.time() - self.last_command_compiled_before_send) > hand_timeout) \
    #     #         or (time.time() - self.last_command_compiled_before_send) > hand_timeout_slow:  #
    #
    #     # if (abs(float_headx - self.old_headx) > change_factor
    #     #     and (time.time() - self.last_command_compiled_before_send) > hand_timeout) \
    #     #         or (time.time() - self.last_command_compiled_before_send) > hand_timeout_slow:  #
    #
    #     #  add more time for drive move:
    #     #  hand_timeout + abs(float_headx - self.old_headx)/12.0
    #     #
    #     # if (abs(float_headx - self.old_headx) > change_factor
    #     #     and (time.time() - self.last_command_compiled_before_send) > (hand_timeout + abs(float_headx - self.old_headx)/12.0)) \
    #     #         or (time.time() - self.last_command_compiled_before_send) > hand_timeout_slow:  #
    #
    #     # check against given params
    #     # print(pos)
    #
    #     # check type of data
    #
    #     # for item in pos:
    #     #     print(item, type(pos[item]), pos[item])
    #
    #     # next is good ...for future movements
    #     # for item in pos:
    #     #     if pos[item] != 'z' or pos[item] != 'catch':
    #     #         pass
    #     #         # self.saved_hand_pos[item] = pos[item]
    #     #         next_hand_pos[item] = pos[item]
    #     #         try:
    #     #             # delta_position = abs(next_hand_pos[item] - self.saved_hand_pos[item])
    #     #             delta_positions.append(abs(next_hand_pos[item] - self.saved_hand_pos[item]))
    #     #             # print(next_hand_pos[item],
    #     #             #       self.saved_hand_pos[item],
    #     #             #       abs(next_hand_pos[item] - self.saved_hand_pos[item]))
    #     #
    #     #
    #     #         except Exception as e:
    #     #             print(type(e), e)
    #     #             # pass
    #
    #     # if len(delta_positions) > 0:
    #     #     print(' {}  movement'.format(max(delta_positions)))
    #     # else:
    #     #     print('not a movement')
    #
    #     # calculate last path robot runs
    #     #
    #     # I think about dependence path the servos run and the closest time the robot will be available to
    #     # accept command ...
    #     #
    #
    #     # last command stored at self.last_move{}
    #
    #     for item in pos:
    #         if pos[item] != 'z' and pos[item] != 'catch':
    #             # pass
    #             # self.saved_hand_pos[item] = pos[item]
    #             next_hand_pos[item] = pos[item]
    #             try:
    #                 # delta_position = abs(next_hand_pos[item] - self.saved_hand_pos[item])
    #                 delta_last_run.append(self.last_move[item])
    #                 # print(next_hand_pos[item],
    #                 #       self.saved_hand_pos[item],
    #                 #       abs(next_hand_pos[item] - self.saved_hand_pos[item]))
    #
    #             except Exception as e:
    #                 print('ERR collecting movements'.format(type(e), e))
    #                 # pass
    #
    #     # #  ACCEPT_COMMAND_TIMEOUT - > self.accept_command_timeout
    #     # if time.time() - self.last_command_compiled_before_send > self.accept_command_timeout + max(delta_last_run) * self.velocity_factor:
    #     #     print('allow last command max {} timeout {} since last {}'.format(
    #     #         str(max(delta_last_run))[0:5],
    #     #         str(self.accept_command_timeout + max(delta_last_run) * self.velocity_factor)[0:4],
    #     #         str(time.time() - self.last_command_compiled_before_send)[0:4])
    #     #     )
    #     #
    #     #     return True
    #     # else:
    #     #     print('deny  last command max {} timeout {} since last {}'.format(
    #     #         str(max(delta_last_run))[0:5],
    #     #         str(self.accept_command_timeout + max(delta_last_run) * self.velocity_factor)[0:4],
    #     #         str(time.time() - self.last_command_compiled_before_send)[0:4])
    #     #     )
    #     #     return False
    #
    #     # added straight comparation 0.8.0.3.3
    #
    #     if time.time() > self.last_command_sent_at:
    #         return False
    #     else:
    #         return True

    def accept_command_with_saved_params(self, current_command):
        # # self.stored_command = {}   # updated storage for commands
        # # self.delayed_command = {}  # updated storage for commands
        #
        self.counter_commands += 1

        # stored_commands = self.stored_command

        print('DBG start accept_command_with_saved_params: {}'.format(current_command))
        print('DBG accept_command_with_saved_params IS EQ? current {}\n'
              '                                              saved {}\n'
              '                                              equal {}\n'.format(
            current_command,
            self.stored_command,
            self.stored_command == current_command))

        try:
            # if self.command_sent:
            #     self.stored_command = current_command
            #     return True
            # else:
            #     if current_command == stored_commands:
            #         return False
            #     else:
            #         self.stored_command = current_command
            #         return True

            # compared against current_command and self.stored_command = current_command
            # if current_command == stored_commands:
            #     return False
            # else:
            #     if self.command_sent:
            #         # sender ready for new command
            #         self.stored_command = current_command
            #         return True
            #     else:
            #         # new command could not be sent as sender is not ready store command for future runs
            #         self.delayed_command = current_command
            #         return False
            #

            if current_command != self.stored_command:
                # new command
                print('DBG accept_command_with_saved_params NOT EQ current {} {}\n'
                      '                                              saved {} {}\n'
                      '                                             equual {}\n'. format(
                      id(current_command), current_command,
                      id(self.stored_command), self.stored_command,
                      self.stored_command == current_command))

                # save this command to ignore same future runs

                self.stored_command = current_command

                # if self.command_sent:

                #  check for possible delays

                if time.time() > self.last_command_sent_at + 0.1:    #####  warning!!!!! DELAY!!!!
                    print(
                        'DBG accept_command_with_saved_params'
                        ' sender ready for new command: {}'.format(self.current_command))
                    return True
                else:
                   print(
                        'DBG accept_command_with_saved_params'
                        ' sender NOT READY for new command: {}'.format(self.current_command))
                return False
            else:
                # same command
                print('DBG accept_command_with_saved_params EQUAL current {} {}\n'
                      '                                             saved {} {}\n'
                      '                                            equual {}\n'. format(
                      id(current_command), current_command,
                      id(self.stored_command), self.stored_command,
                      self.stored_command == current_command))

                print(
                    'DBG accept_command_with_saved_params same command, delayed: {}'.format(self.delayed_command))
                self.delayed_command = current_command
                return False

        except Exception as e:
            print('ERR accept_command_with_saved_params {} {}'.format(type(e), e))

        finally:
            print('DBG end accept_command_with_saved_params self.stored_command: {}'.format(self.stored_command))


    def send_command_data_with_saved_params(self, commands):
        # self.command_sent = False
        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands

        # check if commands not empty
        # pass ... some check

        print('DBG start send_command_data_with_saved_params: {}'.format(commands))

        try:

            before_send_command_data = time.time()

            # dict_commands =
            # {'headx': headx, 'handy': handy, 'turnx': turnx, 'runy': runy, 'catch': catch, 'gear': gear}

            str_commands = 'http://' + str(self.robot_host) + '/?'

            for item in commands:
                print('DBG send_command_data_with_saved_params got command: {}={}'.format(item, commands[item]))

                # str_commands += item + '=' + str(commands[item]) + '&'
                str_commands += item + '=' + str('{}'.format(commands[item])) + '&'

            print('DBG str_commands compiled send_command_data_with_saved_params: {}'.format(str_commands))

            # self.stored_command = commands
            # print('DBG send_command_data_ store command : {} {}'.format(id(self.stored_command), self.stored_command))

            # send command
            try:
                self.last_command_compiled_before_send = time.time()

                print('DBG start sending command send_command_data_with_saved_params: {}'.format(str_commands))

                self.command_sent = False

                client_socket = socket.socket()  # instantiate
                client_socket.connect((self.robot_host, self.robot_port))  # connect to the server
                client_socket.send(str_commands.encode())  # encode than send message
                #
                print(str_commands.encode())  # command like :
                # b'http://192.168.4.1/?headx=0.50&runy=0.50&turnx=0.50&handy=0.50&'
                client_socket.close()  # close the connection
                print('DBG command sent send_command_data_with_saved_params: {}'.format(str_commands))
                self.command_sent = True
            except Exception as e:
                print('ERR: command not sent {} {}'.format(type(e), e))

            self.mean_time_send_command_data = (self.counter_send_command_data * self.mean_time_send_command_data +
                                                time.time() - before_send_command_data) / \
                                               (self.counter_send_command_data + 1)

            self.counter_send_command_data += 1
            self.last_command_sent_at = time.time()

            # erase commands for future runs and set command sent flag  # re-write needed for async native flags
            # self.current_command = {}
            self.command_sent = True

        except Exception as e:
            self.command_sent = True
            print('ERR send_command_data_with_saved_params {} {}'.format(type(e), e))

        finally:
            print('DBG end send_command_data_with_saved_params self.command_sent: {}'.format(self.command_sent))


class RoboJoystickApp(App):
    def build(self):
        # print('BasicApp.running build()')
        self.icon = 'robot256.png'
        return RoboPad()  # goes how ?


if __name__ == '__main__':
    # print('running __main__()')
    RoboJoystickApp().run()
    # print('quiting __main__()')

