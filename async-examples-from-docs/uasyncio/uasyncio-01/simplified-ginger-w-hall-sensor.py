"""
Simplified Ginger microrobot
based on 0.7.9.8h01
"""


class SimplifiedGingerMicroRobot:
    try:
        import machine
        print('DBG: import "machine" library - done')
    except ImportError:
        print('DBG: Could not import "machine" library')

    # def __init__(self,
    #              motor_a_p_duty,
    #              motor_a_m_duty,
    #              servo_direction_duty,
    #              servo_head_x_duty,
    #              servo_hand_y_duty,
    #              servo_catch_duty,
    #              hall_sensor_duty,
    #              networkpin_duty):
    #     '''
    #     motor_a_p = machine.PWM(machine.Pin(5), freq=50)
    #     motor_a_m = machine.PWM(machine.Pin(0), freq=50)
    #     servo_direction = machine.PWM(machine.Pin(12), freq=50)
    #     servo_head_x = machine.PWM(machine.Pin(14), freq=50)
    #     servo_hand_y = machine.PWM(machine.Pin(13), freq=50)
    #     servo_catch = machine.PWM(machine.Pin(15), freq=50)
    #     hall_sensor = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
    #     networkpin = machine.Pin(2, machine.Pin.OUT)
    #     '''

    def __init__(self):

        #
        # self._motor_a_p_duty = None
        # self._motor_a_m_duty = None
        self._servo_direction_duty = None
        # self._servo_head_x_duty = None
        # self._servo_hand_y_duty = None
        # self._servo_catch_duty = None
        # self._hall_sensor_duty = None
        # self._networkpin_duty = None

        try:
            # servo_direction = machine.PWM(machine.Pin(12), freq=50)
            self.servo_direction = machine.PWM(machine.Pin(12), freq=50)
        except Exception as e:
            print('ERR initialising servo_direction = machine.PWM(machine.Pin(12), freq=50)')
            print(type(e), e)


    @property
    def servo_direction_duty(self):
        # self._servo_direction_duty = self.servo_direction.duty()
        # print('DBG: getter of servo_direction called, and get: {}'.format(
        #     self.servo_direction.duty()
        # ))
        # return self._servo_direction_duty

        #
        return self.servo_direction.duty()

    @servo_direction_duty.setter
    def servo_direction_duty(self, value):
        # self._servo_direction_duty = self.servo_direction.duty(value)
        # print('DBG: setter of servo_direction called for duty: {}'.format(
        #     value
        # ))

        #
        self._servo_direction_duty = value
        self.servo_direction.duty(value)


print('start testing SimplifiedGingerMicroRobot')
#
robot = SimplifiedGingerMicroRobot()
robot.servo_direction_duty(33)
print(robot.servo_direction_duty)
#
print('end testing SimplifiedGingerMicroRobot')
