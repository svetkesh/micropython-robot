#!/usr/bin/env python3

"""
ver 0.7.9.95 robot modelled in objects. Introducing him here.
"""

import logging

from gingermicrorobot import GingerMicroRobot as Ginger
from dcdrive import DCDrive as DCDrive
from servomotor import ServoMotor as Servo


def main():
    # Ginger robot pin out
    # servo_direction = machine.PWM(machine.Pin(12), freq=50)
    # servo_head_x = machine.PWM(machine.Pin(14), freq=50)
    # servo_hand_y = machine.PWM(machine.Pin(13), freq=50)
    # servo_catch = machine.PWM(machine.Pin(15), freq=50)

    ginger=Ginger(
        motor=DCDrive(
            name='motor',
            letter='A'
        ),
        servo_direction=Servo(
            name='servo_dir',
            pin=12
        ),
        servo_head_x=Servo(
            name='servo_head_x',
            pin=14
        ),
        servo_hand_y=Servo(
            name='servo_hand_y',
            pin=13
        ),
        servo_catch=Servo(
            name='servo_catch',
            pin=15
        ),
    )

    print(ginger)
    print(dir(ginger.motor))
    print(ginger.motor.echo())
    print(ginger.motor.echo(71))
    print(ginger.motor.duty(71))
    print(ginger.motor.echo('string71'))

    print(ginger.servo_catch.echo())
    print(ginger.servo_catch.echo(72))
    print(ginger.servo_catch.duty(72))
    print(ginger.servo_catch.echo('string 72'))


if __name__ == "__main__":
    print(
        'Here I am'
    )

    main()
