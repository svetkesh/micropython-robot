class ServoMotor:
    """
    Power Width Modulation drive.

    Definitions for PWM drive connected to
    MotorShield (with H-bridge)
    driven by ESP8266.
    """
    print('INFO: class {} running'.format(
        'servomotor.ServoMotor')
    )

    def __init__(self, name, pin, reverse=False):
        self.name = name
        self.pin = pin
        self.reverse = reverse
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

    def echo(self, *args):
        return 'pwm reply ok ' + str(args)

    # duty should be int or float
    def duty(self, *args):
        return 'pwm reporting duty' + str(args)


