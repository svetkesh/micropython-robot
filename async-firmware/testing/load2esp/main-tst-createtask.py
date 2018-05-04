# import pyb

import sys, machine, network, urandom
import utime as time
import uasyncio as asyncio

servo_direction = machine.PWM(machine.Pin(12), freq=50)
servo_head_x = machine.PWM(machine.Pin(14), freq=50)
servo_hand_y = machine.PWM(machine.Pin(13), freq=50)
servo_catch = machine.PWM(machine.Pin(15), freq=50)
networkpin = machine.Pin(2, machine.Pin.OUT)

servos=[servo_direction,
        servo_head_x,
        servo_hand_y,
        servo_catch
        ]


async def runservo(servo):
    servo.duty(urandom.getrandbits(7)+40)
    print('running runservo for {}'.format(servo))
    await asyncio.sleep_ms(urandom.getrandbits(3))
    print('exiting runservo for {}'.format(servo))


async def killer(duration):
    print('running killer')
    await asyncio.sleep(duration)
    print('exiting killer')

# async def toggle(objLED, time_ms):
#     while True:
#         await asyncio.sleep_ms(time_ms)
#         objLED.toggle()

# TEST FUNCTION

# def test(duration):
#     loop = asyncio.get_event_loop()
#     duration = int(duration)
#     if duration > 0:
#         print("Flash LED's for {:3d} seconds".format(duration))
#     leds = [pyb.LED(x) for x in range(1,5)]  # Initialise all four on board LED's
#     for x, led in enumerate(leds):           # Create a coroutine for each LED
#         t = int((0.2 + x/2) * 1000)
#         loop.create_task(toggle(leds[x], t))
#     loop.run_until_complete(killer(duration))
#     loop.close()
#
# # test(10)


def test_runservo(duration):
    print('step into test_runservo')
    loop = asyncio.get_event_loop()
    for servo in servos:
        loop.create_task(runservo(servo))
    loop.run_until_complete(killer(duration))
    loop.close()
    print('exiting test_runservo() and loop.close')


test_runservo(20)
print('end main')
