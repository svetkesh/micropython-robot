import asyncio
import time
import sys, signal
import sys, termios, tty, os

VELOCITY = 1 # move from position 0  to 1 in 1 second


async def side_move(side):
    return await side


async def up_move(up):
    return await up


# async def read_input():
#     while True:
#         if keyboard.is_pressed('q'):
#             print('QUIT')
#         else:
#             print('something pressed')


def getch():
    fd = sys.stdin.fileno()
    # old_settings = termios.tcgetattr(fd)
    old_settings = termios.t
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


button_delay = 0.2


def sync_read_input():
    while True:
        char = getch()

        if char == "a":
            print("Left pressed")
            time.sleep(button_delay)

        elif char == "d":
            print("Right pressed")
            time.sleep(button_delay)

        elif char == "w":
            print("Up pressed")
            time.sleep(button_delay)

        elif char == "s":
            print("Down pressed")
            time.sleep(button_delay)

        elif char == "p":
            print("Stop!")
            exit(0)


# async def hand_up(hand):
#     print('rising hand '+hand)
#     return 'rise hand '+hand
#
#
# async def exercise():
#     return await hand_up('left')
#
#
# async def speak_async():
#     # time.sleep(1)
#     await asyncio.sleep(1)
#     print('hello asynk')


# def signal_handler(signal, frame):
#     loop.stop()
#     # client.close()
#     sys.exit(0)


# signal.signal(signal.SIGINT, signal_handler)
#
# loop = asyncio.get_event_loop()
# # loop.run_until_complete(speak_async())
# # loop.run_until_complete(exercise())
#
# asyncio.ensure_future(speak_async())
# asyncio.ensure_future(exercise())
# loop.run_forever()

sync_read_input()
