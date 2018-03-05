#!/usr/bin/env python3

from dcdrive import DCDrive as dcdrive
from servomotor import ServoMotor as servo

class GingerMicroRobot:
    print('INFO: class {} running'.format(
        'GingerMicroRobot')
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

    def __str__(self):
        for item in self.__dict__:
            print(item,
                  self.__dict__[item],
                  type(self.__dict__[item]),
                  self.__dict__[item].__class__.__name__
                  )
        return 'this, of course ))'

def main():
    print('yessssss main!')
    # dc_a = dcdrive('FFRR', 'A')
    # servo_catch = servo('Catch', 12)

    ginger = GingerMicroRobot(
        dc_a = dcdrive('FFRR', 'A'),
        servo_catch = servo('catch', 12),
        servo_hand_turn = servo('hand_turn', 13),
    )
    print(ginger)
    print('----')
    print('using dot notation with Robot instance')
    print(ginger.dc_a.brrr())
    print(ginger.servo_catch.brrr())
    print(ginger.dc_a.brv('motorrrr'))
    print(ginger.servo_catch.brv(13))
    print(ginger.servo_hand_turn.brv(33))

    # TODO separate gingermicrorobot from its instance and make gingermicrorobot pure class
    #   ... delete import dcdrive and servodrive from this file
    #   ... play with 3 (as far) imports elsewhere


if __name__ == '__main__':
    print('DBG: __main__ running')
    main()
    print('DBG: __main__ quit')
