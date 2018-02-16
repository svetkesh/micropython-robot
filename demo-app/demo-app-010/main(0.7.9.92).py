"""
This is main.py for running on ESP8266 MicroPython

Handles request of type:

http://192.168.101.102/?headx=0.5&handy=0.5&turnx=0.5&runy=0.5

Not requires all
 headx, handy, turnx, runy

# >>> import ure
# >>> rh = re.compile("headx=0\.(\d+)")

# >>> print('not') if None != rh.search(s) else print('yes')
# not
# >>> print('not') if None != rh.search(not_s) else print('yes')
yes


ver 0.7.9.1 - accepting separate commands
0.7.9.1 - version for RoboHand 0.7.9.1

ver 0.7.9.1 + minor fix for y axis for hand - joystick

ver 0.7.9.3 reply html with current IP
ver 0.7.9.4 add catch (working)
ver 0.7.9.9 based on 0.7.9.4 rewritten as modules and objects
            uses ('...some kind of dot notation -
            - instance.attributes') for storing components

            variant 1 (update(args)):
                def __init__(self, **args):
                    self.__dict__.update(args)
                    self.__dict__.update(locals())
                    del self.self

            variant 2 (setattr):
                def __init__(self, **kwargs):
                    for key, value in kwargs.items():
                    setattr(self, key, value)
"""


# # ok ...
# # introducing classes inside class Robot
# class RobotPWM:
#     """
#     Power Width Modulation drive.
#
#     This class defines PWM for motor-shield for ESP12E with
#     ESP8266 module.
#     Should easy define logical structure,
#     and electrical parameters,
#     and easy tie to motor-shield pin numeration,
#     and easy working frequency setting.
#
#     Example:
#         pwm_turn = RobotPWM(
#             'pwm 12',
#             12
#         )
#         print(pwm_turn)
#
#         # gives:
#
#         INFO: RobotPWM initialized
#         INFO: RobotMotor initialized
#         INFO: object: {'pin': 12, 'name': 'pwm 12'}
#                class: RobotPWM
#                 name: pwm 12
#                  pin: 12
#     Attributes:
#         name: readable name for PWM drive such as 'left_leg_up', 'catch_hand'
#         pin: pin to connect to Dx at DEVKIT notation. Please refer Motorshield to ESP12E pinout here:
#             http://csharpcorner.mindcrackerinc.netdna-cdn.com/article/
#                 blinking-led-by-esp-12e-nodemcu-v3-module-using-arduinoide/
#                     Images/NodeMCU_Pinout.png
#         (@ http://www.c-sharpcorner.com/article/blinking-led-by-esp-12e-nodemcu-v3-module-using-arduinoide/)
#
#     Todo:
#         * Rewrite class to accept motorshield pinout notation.
#     """
#     print('INFO: class {} running'.format(
#         'RobotPWM')
#     )
#
#     def __init__(self, name, pin):
#         self.name = name
#         self.pin = pin
#         print('INFO: {} initialized'.format(
#             self.__class__.__name__)
#         )
#
#     def __str__(self):
#         return 'INFO: object: {}\n'\
#                '       class: {}\n'\
#                '        name: {}\n'\
#                '         pin: {}'\
#             .format(self.__dict__,
#                     self.__class__.__name__,
#                     self.name,
#                     str(self.pin))
#
#
# class RobotMotor:
#     print('INFO: class {} running'.format(
#         'RobotMotor')
#     )
#
#     def __init__(self, name, letter):
#         self.name = name
#         self.letter = letter
#         print('INFO: {} initialized'.format(
#             self.__class__.__name__)
#         )
#
#     def __str__(self):
#         return 'INFO: object: {}\n'\
#                '       class: {}\n'\
#                '        name: {}\n'\
#                '      letter: {}'\
#             .format(self.__dict__,
#                     self.__class__.__name__,
#                     self.name,
#                     self.letter)


class Robot:
    print('INFO: class {} running'.format(
        'Robot')
    )

    # def __init__(self, **args):
    #     # # counter to display
    #     # counter = 0
    #     #
    #     # for arg in args:
    #     #     print('DBG: counter:{}'.format(counter))
    #     #     print(self, self.__dir__())
    #     #     print(arg)
    #     #     self.arg = arg
    #     #     counter += 1
    #
    #     self.__dict__.update(args)
    #     self.__dict__.update(locals())
    #     del self.self

    # def setAllWithKwArgs(self, **kwargs):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    class RobotPWM:
        """
        Power Width Modulation drive.
        """
        print('INFO: class {} running'.format(
            'RobotMotor.RobotPWM')
        )

        def __init__(self, name, pin):
            self.name = name
            self.pin = pin
            print('INFO: {} initialized'.format(
                self.__class__.__name__)
            )

        def __str__(self):
            return 'INFO: object: {}\n' \
                   '       class: {}\n' \
                   '        name: {}\n' \
                   '         pin: {}' \
                .format(self.__dict__,
                        self.__class__.__name__,
                        self.name,
                        str(self.pin))

        def brrr(self):
            return 'pwmbrrrrr'

        def brv(self, val):
            return 'pwmbrrrrr' + str(val)

    class RobotMotor:
        """
        DC drive.
        """
        print('INFO: class {} running'.format(
            'RobotMotor.RobotMotor')
        )

        def __init__(self, name, letter):
            self.name = name
            self.letter = letter
            print('INFO: {} initialized'.format(
                self.__class__.__name__)
            )

        def __str__(self):
            return 'INFO: object: {}\n' \
                   '       class: {}\n' \
                   '        name: {}\n' \
                   '      letter: {}' \
                .format(self.__dict__,
                        self.__class__.__name__,
                        self.name,
                        self.letter)

        def brrr(self):
            return 'motorbrrrrr'

        def brv(self, val):
            return 'motorbrrrrr' + str(val)


def mainland():
    print('yep mainland!')
    #  commented with
    #  commenting classes RobotPWM and RobotMotor
    # pwm_turn = RobotPWM(
    #     'pwm 12',
    #     12
    # )
    # motor_a = RobotMotor(
    #     'motor',
    #     'A'
    # )
    # print(pwm_turn)
    # print(motor_a)
    # ok ... so far

    # print(RobotPWM.__doc__)
    # robot = Robot()
    # print(robot.__dict__)
    # print(Robot.__dict__)
    # # some introspection
    # for item in Robot.__dict__:
    #     print(item,
    #           Robot.__dict__[item],
    #           type(Robot.__dict__[item]),
    #           Robot.__dict__[item].__class__.__name__
    #           # isinstance(type(Robot.__dict__[item]), type)
    #           )

    # robot.add_component(Robot.RobotMotor('drive_B', 'A'))
    # robot.add_component(Robot.RobotPWM('nand_catch', 12))

    # print(robot.__dict__)
    # print(Robot.__dict__)
    # # some introspection
    # for item in Robot.__dict__:
    #     print(item,
    #           Robot.__dict__[item],
    #           type(Robot.__dict__[item]),
    #           Robot.__dict__[item].__class__.__name__
    #           # isinstance(type(Robot.__dict__[item]), type)
    #           )

    extra_drive = Robot.RobotPWM('extra', 13)
    motor_a = Robot.RobotMotor('motor_a', 'A')

    # this is for
    # def __init__(self, **args):
    #   ...

    robot = Robot(extra_drive=Robot.RobotPWM('extra', 13),
                  motor_a=Robot.RobotMotor('motor_a', 'A')
                  )

    # robot = Robot(Robot.RobotPWM('extra', 13),      # keyworded args needed
    #               Robot.RobotMotor('motor_a', 'A')  # in __init__(self, **kwargs)
    #               )
    # some introspection into robot instance
    print('INFO: some introspection into robot instance')
    print('DBG: robot:{}'.format(robot))
    print('DBG: robot.__dict__ :{}'.format(robot.__dict__))
    print('DBG: robot.__dir__():{}'.format(robot.__dir__()))

    for item in robot.__dict__:
        print(item,
              robot.__dict__[item],
              type(robot.__dict__[item]),
              robot.__dict__[item].__class__.__name__
              )

    print('----')
    print('using dot notation with Robot instance')
    print(robot.motor_a.brrr())
    print(robot.extra_drive.brrr())
    print(robot.motor_a.brv('motorrrr'))
    print(robot.extra_drive.brv(13))














def main():
    print('yessssss main!')


if __name__ == '__main__':
    print('DBG: __main__ running')
    mainland()
    main()
    print('DBG: __main__ quit')





