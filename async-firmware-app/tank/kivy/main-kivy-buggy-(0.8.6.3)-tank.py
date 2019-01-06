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


0.8.3.0.15 - added setting reader and writer
             (for accept JSON)

0.8.4.1(084.1)  - send JSON -formatted command
0.8.4.5(084.1)  - run command sends value integer 0..99, changed runy math, gear limited 1..5
0.8.4.7(084.7) - re-entered "AFTERBURNER", clock scheduled to issue "delayed commands"
.1 for trike/quadro
0.8.4.7-5 (.5) - both joysticks are non-stick
                 fixed run now values from 1 to 98
                 turn uses square x**2 function
0.8.4.7-5 (.5) - speed factor initiated with 4
                initiated self.timeout_timer_start = 0.16
for tank FW 0.8.7.1.1 and 0.8.7.1.2
0.8.6.1 - add "overdrive" button
0.8.6.2 - add enginireing controls for tank
0.8.6.3 - bugs fixed

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
from kivy.uix.switch import Switch

import socket
import time

from kivy.clock import Clock
import json

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
                                     pos_hint={'x': .0, 'y': .0},  #)  #,
                                     sticky=True)
        self.add_widget(self.joystickhand)
        self.joystickrun = Joystick(size_hint=(.5, .5),
                                    pos_hint={'x': .5, 'y': .0})  #,
                                    # sticky=True)
        self.joystickhand.bind(pad=self.update_coordinates_hand)

        self.add_widget(self.joystickrun)
        self.joystickrun.bind(pad=self.update_coordinates_run)

        # add some buttons
        self.firebutton = Button(size_hint=(.3, .2),
                                  pos_hint={'x': .6, 'y': .7},
                                  text='Fire!')
        self.add_widget(self.firebutton)
        self.firebutton.bind(on_press=self.update_fire_release)

        # self.dance_button = Button(size_hint=(.2, .1),
        #                           pos_hint={'x': .4, 'y': .9},
        #                           text='Dance!')
        # # self.add_widget(self.dance_button)
        # self.dance_button.bind(on_press=self.update_dance)

        # self.hiphop_dance = Button(size_hint=(.2, .1),
        #                           pos_hint={'x': .1, 'y': .9},
        #                           text='hip-hop!')
        # # self.add_widget(self.hiphop_dance)
        # self.hiphop_dance.bind(on_press=self.update_hiphop)

        # self.reset_stat_button = Button(size_hint=(.05, .05),
        #                                 pos_hint={'x': .6, 'y': .65},
        #                                 text='reset stat')
        # self.add_widget(self.reset_stat_button)
        # self.reset_stat_button.bind(on_press=self.reset_stat_button)

        # add debug Labels
        # self.debug_label = Label(size_hint=(.4, .0),
        #                              pos_hint={'x': .2, 'y': .2},
        #                              text='message ... ...',)  # multiline=True,)
        # # self.add_widget(self.debug_label)

        # self.debug_label_hand = Label(size_hint=(.2, .2),
        #                               pos_hint={'x': .1, 'y': .8},
        #                               text='message ... ...',)
        # self.add_widget(self.debug_label_hand)
        # self.debug_label_run = Label(size_hint=(.2, .2),
        #                              pos_hint={'x': .5, 'y': .8},
        #                              text='message ... ...',)  # multiline=True,)
        # self.add_widget(self.debug_label_run)

        # self.slider_accept_command_timeout = Slider(size_hint=(.4, .03),
        #                                             pos_hint={'x': .1,
        #                                                       'y': .9},
        #                                             min=0.02,
        #                                             max=0.2,
        #                                             value=0.05)
        # # self.add_widget(self.slider_accept_command_timeout)
        #
        # self.slider_accept_command_timeout.bind(value=self.OnSliderAcccepptCommandTiteoutValueChange)

        # self.slider_velocity_factor = Slider(size_hint=(.4, .03),
        #                                             pos_hint={'x': .1,
        #                                                       'y': .85},
        #                                             min=0.01,
        #                                             max=10.0,
        #                                             value=0.3)
        # # self.add_widget(self.slider_velocity_factor)
        #
        # self.slider_velocity_factor.bind(value=self.OnSliderVelocityFactorValueChange)

        #  not used , just place holder
        # self.slider_timeout_timer_start = Slider(size_hint=(.4, .03),
        #                                             pos_hint={'x': .1,
        #                                                       'y': .8},
        #                                             min=0.02,
        #                                             max=0.2,
        #                                             value=0.16)
        # # self.add_widget(self.slider_timeout_timer_start)
        #
        # self.slider_timeout_timer_start.bind(value=self.OnSliderTimeoutTimerStartValueChange)

        self.slider_gear_factor = Slider(size_hint=(.4, .03),
                                                    pos_hint={'x': .1,
                                                              'y': .8},
                                                    min=2,
                                                    max=5,
                                                    value=3)
        self.add_widget(self.slider_gear_factor)

        self.slider_gear_factor.bind(value=self.OnSliderGearFactorValueChange)

        # Switches for Tank
        self.switch_invert_runa = Switch(size_hint=(.1, .1),
                                         pos_hint={'x': .6, 'y': .9},)
        self.add_widget(self.switch_invert_runa)
        self.switch_invert_runa.bind(active=self.OnActiveInvertRuna)

        self.switch_invert_runb = Switch(size_hint=(.1, .1),
                                         pos_hint={'x': .8, 'y': .9},)
        self.add_widget(self.switch_invert_runb)
        self.switch_invert_runb.bind(active=self.OnActiveInvertRunb)

        self.switch_invert_headx = Switch(size_hint=(.1, .1),
                                         pos_hint={'x': .1, 'y': .9},)
        self.add_widget(self.switch_invert_headx)
        self.switch_invert_headx.bind(active=self.OnActiveInvertHeadx)

        self.switch_invert_handy = Switch(size_hint=(.1, .1),
                                         pos_hint={'x': .3, 'y': .9},)
        self.add_widget(self.switch_invert_handy)
        self.switch_invert_handy.bind(active=self.OnActiveInvertHandy)


        # # OverDrive
        # self.overdrive_button = Button(size_hint=(.2, .1),
        #                           pos_hint={'x': .4, 'y': .9},
        #                           text='OverDrive!')
        # self.add_widget(self.overdrive_button)
        # self.overdrive_button.bind(on_press=self.switch_overdrive)

        # # StatusBar
        # self.statusbar_label = Label(size_hint=(.4, .0),
        #                              pos_hint={'x': .2, 'y': .2},
        #                              text='main-kivy-buggy-(0.8.6.1) ...',)  # multiline=True,)
        # self.add_widget(self.statusbar_label)

        # Settings
        self.accept_command_timeout = 0.05  # timeout after last_command_sent_at before accepting next command

        # self.timeout_slow = 0.14
        self.timeout_timer_start = 0.16
        self.velocity_factor = 0.3

        self.old_headx = 0.0
        self.old_handy = 0.0
        self.old_runa = 0.0
        self.old_runb = 0.0
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

        # Template
        # self.invert_runy = False
        # self.invert_turnx = False

        # Controls for Tank
        self.invert_headx = False
        self.invert_handy = False
        self.invert_runa = False
        self.invert_runb = False

        self.gear = 3
        self.overdrive_switched_at = time.time()
        self.overdrive_timeout = 5.0

        self.robot_host = '192.168.4.1'  # hardcoded robot ip t4m net
        self.robot_port = 80

        self.current_pos = {'headx': 0.0, 'handy': 0.0, 'runa': 0.0, 'runb': 0.0, 'gear': self.gear}
        self.saved_pos = {'headx': 0.0, 'handy': 0.0, 'runa': 0.0, 'runb': 0.0, 'gear': self.gear}

        self.last_move = {'headx': 0.0, 'handy': 0.0, 'runa': 0.0, 'runb': 0.0, 'gear': self.gear}

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

        # self.send_command_data(gear=self.gear)
        # self.saved_command['gear'] = self.gear

        # self.current_command = {}

        self.gear = round(value)

        self.current_command['gear'] = self.gear

        # print('DBG start OnSliderGearFactorValueChange self.current_command: {}'.format(self.current_command))

        self.accept_command_with_saved_params(self.current_command)
        # print('DBG end OnSliderGearFactorValueChange self.current_command: {}'.format(self.current_command))

    # def switch_overdrive(self, instance):
    #     # self.gear = 3
    #     # self.overdrive_switched_at = time.time()
    #     # self.overdrive_timeout = 5.0
    #
    #     if time.time() > (self.overdrive_switched_at + self.overdrive_timeout):
    #         # do
    #         self.gear = 5
    #         self.current_command['gear'] = self.gear
    #         print('DBG start switch_overdrive self.current_command: {}'.format(self.current_command))
    #
    #         self.accept_command_with_saved_params(self.current_command)
    #         print('DBG end switch_overdrive self.current_command: {}'.format(self.current_command))
    #         self.overdrive_switched_at = time.time()
    #     else:
    #         print('DBG switch_overdrive timeout: {}'.format(
    #             round(time.time() - (self.overdrive_switched_at + self.overdrive_timeout))
    #         ))
    #
    # def OnSliderTimeoutTimerStartValueChange(self, instance, value):
    #     # self.command_sent = False
    #     # print(type(value), value, self.timeout_timer_start)
    #     self.timeout_timer_start = value


    # Temmplates for Switches-invertors

    # def OnActiveInvertRuny(self, instance, value):
    #     self.invert_runy = not self.invert_runy

    # def OnActiveInvertTurnx(self, instance, value):
    #     self.invert_turnx = not self.invert_turnx

    # Controls for Tank
    def OnActiveInvertRuna(self, instance, value):
        self.invert_runa = not self.invert_runa
        # print("Set self.invert_runa: {} {} {} {}".format(self.invert_runa, self, instance, value))

    def OnActiveInvertRunb(self, instance, value):
        self.invert_runb = not self.invert_runb
        # print("Set self.invert_runb: {}".format(self.invert_runb))

    def OnActiveInvertHeadx(self, instance, value):
        self.invert_headx = not self.invert_headx
        # print("Set self.invert_headx: {} {} {} {}".format(self.invert_headx, self, instance, value))

    def OnActiveInvertHandy(self, instance, value):
        self.invert_handy = not self.invert_handy
        # print("Set self.invert_handy: {} {} {} {}".format(self.invert_handy, self, instance, value))

    def update_coordinates_run(self, joystick, pad):
        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands

        x = self.squaredround(pad[0], self.invert_runa)
        y = self.squaredround(pad[1], self.invert_runb)

        self.current_command['runa'] = self.recalculate_dc_position(x, self.invert_runa)
        self.current_command['runb'] = self.recalculate_dc_position(y, self.invert_runb)

        # print('DBG start update_coordinates_run self.current_command: {}'.format(self.current_command))
        self.accept_command_with_saved_params(self.current_command)
        # print('DBG end update_coordinates_run self.current_command: {}'.format(self.current_command))

    def update_coordinates_hand(self, joystick, pad):
        # self.command_sent = False
        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands
        # self.current_command = {}

        x = self.squaredround(pad[0], self.invert_headx)
        y = self.squaredround(pad[1], self.invert_handy)

        # self.current_command['headx'] = self.recalculate_servo_position(x)  # orig 2-axes
        # self.current_command['handy'] = self.recalculate_servo_position(y)

        self.current_command['headx'] = self.recalculate_servo_position(x)
        self.current_command['handy'] = self.recalculate_servo_position(y)
        self.accept_command_with_saved_params(self.current_command)

    def update_fire_release(self, instance):
        # self.command_sent = False
        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands

        # # print('DBG: button pressed!')
        # catch = catch

        # self.current_command = {}

        # print('DBG start update_fire_release self.current_command: {}'.format(self.current_command))
        self.current_command['fire'] = 'fire'
        self.accept_command_with_saved_params(self.current_command)
        # print('DBG end update_fire_release self.current_command: {}'.format(self.current_command))

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
                self.saved_command['runa']=random.choice(['z', random.random()])
                self.saved_command['runb']=random.choice(['z', random.random()])
                self.saved_command['fire']=random.choice(['z', 'fire'])
                
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

    def timer_with_saved_params(self, dt):

        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands

        # debug_text = "commands counter: {} sent: {}\n" \
        #              "mean timeout sending commands: {}\n" \
        #              "self.slider_accept_command_timeout: {}\n" \
        #              "self.slider_velocity_factor: {}\n" \
        #              "self.slider_timeout_timer_start: {}\n" \
        #              "self.gear: {}\n" \

        # self.debug_label.text = debug_text.format(self.counter_commands,
        #                                           str((self.counter_send_command_data / self.counter_commands))[0:5],
        #                                           str(self.mean_time_send_command_data)[0:5],
        #                                           str(self.accept_command_timeout)[0:5],
        #                                           str(self.velocity_factor)[0:5],
        #                                           str(self.timeout_timer_start)[0:5],
        #                                           str(self.gear))

        # AFTERBURNER

        self.accept_command_with_saved_params(self.delayed_command)

        # # set gear = 3 after timeout and reset gear timer
        # if time.time() > (self.overdrive_switched_at + self.overdrive_timeout):
        #     # do
        #     if self.gear != 3:
        #         self.gear = 3
        #         self.current_command['gear'] = self.gear
        #         # print('DBG start switch_overdrive self.current_command: {}'.format(self.current_command))
        #
        #         self.accept_command_with_saved_params(self.current_command)
        #         # print('DBG end switch_overdrive self.current_command: {}'.format(self.current_command))
        #         self.overdrive_switched_at = time.time()

    def squaredround(self, x, inverter):
        import math

        # print('DBG squaredround x: {}'.format(x))
        max_x = 0.99
        # multiply_factor = 1.3
        multiply_factor = 0.99

        sign = lambda y: math.copysign(1, y)
        aligned_x = x * multiply_factor if inverter else x * multiply_factor * (-1)

        if abs(aligned_x) < 0.05:
            squaredround_x = 0.0
            # return 0.0

        if abs(aligned_x) > 0.99:
            # return max_x * sign(aligned_x)
            squaredround_x = max_x * sign(aligned_x)
        else:
            # return float(str(aligned_x)[0:4])
            # squaredround_x = float(str(aligned_x)[0:4])
            squaredround_x = float(str(aligned_x)[0:6])

        # print('DBG squaredround x: {} -> {}, of: {} '.format(x, squaredround_x, str(aligned_x)[0:6]))
        return squaredround_x

    def recalculate_servo_position(self, x):
        import math

        # self.SERVO_MIN = 40
        # self.SERVO_MAX = 115
        # self.servo_center = 75
        # self.SERVO_NEAR_ZERO = 0.03
        # self.SERVO_FACTOR = 1.3

        max_x = 0.99
        multiply_factor = 1.01

        sign = lambda y: math.copysign(1, y)
        aligned_x = x * multiply_factor
        # aligned_x = x * multiply_factor if inverter else x * multiply_factor * (-1)  # inverted in squaredround

        if abs(aligned_x) < self.SERVO_NEAR_ZERO:
            return self.servo_center
        elif abs(aligned_x) > 0.99:
            normalized_x = max_x * sign(aligned_x)
        else:
            # linear function
            # normalized_x = float(str(aligned_x)[0:6])
        # return int((normalized_x + 1) / 2 * self.servo_center + self.SERVO_MIN)

            # square function

            normalized_x = aligned_x ** 2 * sign(aligned_x)

        return int((normalized_x + 1) / 2 * self.servo_center + self.SERVO_MIN)

    def recalculate_dc_position(self, x, inverter):
        # inverter is self.invert_runy or (self.invert_runy is valid for trike and buggy)
        #             self.invert_runa , or
        #             self.invert_runb
        import math

        dc_min = 1  # dc accepts integer values 1..99
        dc_max = 99
        dc_center = 50  # pre-set center value

        min_x = -0.99
        max_x = 0.99
        near_zero = 0.02  # 4% of joystick run near center count as center

        multiply_factor = 1.0  # stretch joystick

        sign = lambda y: math.copysign(1, y)
        # print('DBG recalculate_dc_position sign: {}, {}'.format(type(sign(x)), sign(x)))

        # invert forward and backward according to invert_runy self.invert_runy
        # aligned_x = x * multiply_factor if inverter else x * multiply_factor * (-1)  # inverted in squaredround
        aligned_x = x * multiply_factor
        # print("recalculate_dc_position value:{}, invertor:{}, get {}".format(x, inverter, aligned_x))

        if abs(aligned_x) < near_zero:
            # normalized_x = 0.0
            recalculated_x = dc_center

        elif abs(aligned_x) > 0.99:
            normalized_x = max_x * sign(aligned_x)
            recalculated_x = int(normalized_x * dc_max)

        else:
            # normalized_x = float(str(aligned_x)[0:4])
            normalized_x = aligned_x ** 2 * sign(aligned_x)
            # print('DBG recalculate_dc_position x- > x: {}>> {}'.format(aligned_x, normalized_x))
            # print('DBG recalculate_dc_position value: {}'.format(
            #     int(round(((normalized_x - min_x) / (max_x - min_x)) * dc_max))))
            recalculated_x = int(round(((normalized_x - min_x) / (max_x - min_x)) * dc_max))
        # print('DBG recalculate_dc_position x: {},\n'
        #       '                    aligned_x: {},\n'
        #       '                 normalized_x: {},\n'
        #       '               recalculated_x: {} \
        #         '.format(x,
        #                  aligned_x,
        #                  aligned_x ** 2 * sign(aligned_x),  # normalized_x if normalized_x else '',
        #                  recalculated_x))
        return recalculated_x

        ## recalculate_dc_position from ginger
        # print('DBG recalculate_dc_position x: {}, {}'.format(type(x), x))
        #
        # dc_min = 1  # dc accepts integer values 1..99
        # dc_max = 99
        # dc_center = 50  # pre-set center value
        #
        # min_x = -0.99
        # max_x = 0.99
        # near_zero = 0.03  # 3 % of joystick run near center count as center
        #
        # multiply_factor = 1.0  # stretch joystick
        #
        # sign = lambda y: math.copysign(1, y)
        # print('DBG recalculate_dc_position sign: {}, {}'.format(type(sign(x)), sign(x)))
        # aligned_x = x * multiply_factor
        #
        # if abs(aligned_x) < near_zero:
        #     # normalized_x = 0.0
        #     return dc_center
        # elif abs(aligned_x) > 0.99:
        #     normalized_x = max_x * sign(aligned_x)
        #     return int(normalized_x * dc_max)
        # else:
        #     # normalized_x = float(str(aligned_x)[0:4])
        #     normalized_x = aligned_x ** 2 * sign(aligned_x)
        #     print('DBG recalculate_dc_position x- > x: {}>> {}'.format(aligned_x, normalized_x))
        #     print('DBG recalculate_dc_position value: {}'.format(
        #         int(round(((normalized_x - min_x) / (max_x - min_x)) * dc_max))))
        #     return int(round(((normalized_x - min_x) / (max_x - min_x)) * dc_max))

    def accept_command_with_saved_params(self, current_command):
        # # self.stored_command = {}   # updated storage for commands
        # # self.delayed_command = {}  # updated storage for commands
        #
        self.counter_commands += 1

        # stored_commands = self.stored_command

        # print('DBG start accept_command_with_saved_params: {}'.format(current_command))
        # print('DBG accept_command_with_saved_params CHECK EQUAL? current {} {}\n'
        #       '                                                    saved {} {}\n'
        #       '                                                    equal {}\n'
        #       '                                                         ------'.format(
        #        id(current_command), current_command,
        #        id(self.stored_command), self.stored_command,
        #        self.stored_command == current_command))

        try:
            if current_command != self.stored_command:
                # new command
                # print('DBG accept_command_with_saved_params NOT EQ current {}\n'
                #       '                                              saved {}\n'
                #       '                                              equal {}'. format(
                #        current_command,
                #        self.stored_command,
                #        self.stored_command == current_command))

                if time.time() > self.last_command_sent_at + self.accept_command_timeout:  # warning!!!!! DELAY!!!!
                    if self.current_command:

                        print(
                            'DBG accept_command_with_saved_params'
                            ' sender ready for new command: {}'.format(self.current_command))
                        # nothing to delay , run now new command
                        self.send_command_data_with_saved_params(self.current_command)
                        self.current_command = {}
                        self.stored_command = current_command  # save this command to ignore same future runs
                        self.delayed_command = {}
                        return True
                    else:
                        return False
                else:
                    print('DBG accept_command_with_saved_params'
                          ' sender NOT READY for new command: {}'.format(self.current_command))

                    # delay command for later run in dictionary self.delayed_command
                    self.stored_command = {}
                    for key in current_command:
                        self.delayed_command[key] = current_command[key]
                    print(
                        'DBG accept_command_with_saved_params append command to delayed: {}'.format(
                            self.delayed_command))
                    return False
            else:
                # same command
                # print('DBG accept_command_with_saved_params EQUAL current {}\n'
                #       '                                              saved {}\n'
                #       '                                              equal {}'. format(
                #        current_command,
                #        self.stored_command,
                #        self.stored_command == current_command))
                #
                # print(
                #     'DBG accept_command_with_saved_params same command, delayed: {}'.format(self.delayed_command))
                return False

        except Exception as e:
            print('ERR accept_command_with_saved_params {} {}'.format(type(e), e))

        # finally:
        #     print('DBG end accept_command_with_saved_params self.stored_command: {}'.format(self.stored_command))

    def send_command_data_with_saved_params(self, commands):
        # self.command_sent = False
        # self.stored_command = {}   # updated storage for commands
        # self.delayed_command = {}  # updated storage for commands

        # check if commands not empty
        # pass ... some check

        # print('DBG start send_command_data_with_saved_params: {}'.format(commands))

        try:

            before_send_command_data = time.time()

            # dict_commands =
            # {'headx': headx, 'handy': handy, 'turnx': turnx, 'runy': runy, 'catch': catch, 'gear': gear}

            str_commands = 'http://' + str(self.robot_host) + '/?&run=' + json.dumps(commands) + '\&'

            # for item in commands:
            #     print('DBG send_command_data_with_saved_params got command: {}={}'.format(item, commands[item]))
            #
            #     # str_commands += item + '=' + str(commands[item]) + '&'
            #     str_commands += item + '=' + str('{}'.format(commands[item])) + '&'

            # print('DBG str_commands compiled send_command_data_with_saved_params: {}'.format(str_commands))

            # self.stored_command = commands
            # print('DBG send_command_data_ store command : {} {}'.format(id(self.stored_command), self.stored_command))

            # send command
            try:
                self.last_command_compiled_before_send = time.time()

                # print('DBG start sending command send_command_data_with_saved_params: {}'.format(str_commands))

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

