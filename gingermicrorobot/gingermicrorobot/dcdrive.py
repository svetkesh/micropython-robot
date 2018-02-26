class DCDrive:
    """
    DC drive.

    Definitions for DC drive connected to
    MotorShield (with H-bridge)
    driven by ESP8266.
    """
    print('INFO: class {} running'.format(
        'dcdrive.DCDrive')
    )

    def __init__(self, name, letter, reverse=False):
        self.name = name
        self.letter = letter
        self.reverse = reverse
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

    def echo(self, *args):
        return 'motor echo ok' + str(args)

        # duty should be int or float
    def duty(self, *args):
        return 'motor reporting duty' + str(args)
