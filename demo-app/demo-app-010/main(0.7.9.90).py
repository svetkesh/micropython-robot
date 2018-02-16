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
            uses list for storing components
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

    #
    # print('INFO: before components assigned')
    # components = []  #
    # print('INFO: after components assigned')

    def __init__(self):
        self.components = []

    def add_component(self, component):
        """
        Add drive or sensor to robot listing

        :param component: drive or sensor
        :return: updated list components
        """
        print('INFO: Robot.add_component() running ')
        self.components.append(component)
        print(self.components, len(self.components))
        return self.components


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
    robot = Robot()
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
    robot.add_component(Robot.RobotMotor('drive_B', 'A'))
    robot.add_component(Robot.RobotPWM('nand_catch', 12))

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

    print(robot)
    for component in robot.components:
        print(component)
    print('--')

    extra_drive = Robot.RobotPWM('extra', 13)
    robot.add_component(extra_drive)
    robot.add_component(14)

    print(robot.components)
    print(robot.components[0])

    print('----')
    print(robot.components)
    print(robot.components.index(extra_drive))









def main():
    print('yessssss main!')


if __name__ == '__main__':
    print('DBG: __main__ running')
    mainland()
    main()
    print('DBG: __main__ quit')





