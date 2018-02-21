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

    # some inline tests
    def brrr(self):
        return 'motorbrrrrr'

    def brv(self, val):
        return 'motorbrrrrr' + str(val)

    def echo(self, *args):
        return 'motorbrrrrr' + str(args)

    def duty(self, *args):
        return 'motor reporting duty' + str(args)
