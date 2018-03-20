import asyncio
import time
import sys, signal
import sys, termios, tty, os
import pynput

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


