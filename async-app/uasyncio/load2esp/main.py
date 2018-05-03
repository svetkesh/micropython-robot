# import asyncio
#
# async def say(what, when):
#     await asyncio.sleep(when)
#     print(what)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(say('hello world', 1))
# loop.close()


# import asyncio
#
# async def say(what, when):
#     await asyncio.sleep(when)
#     print(what)
#
#
# loop = asyncio.get_event_loop()
#
# loop.create_task(say('first hello', 2))
# loop.create_task(say('second hello', 1))
#
# loop.run_forever()
# loop.close()




# import asyncio
#
# async def say(what, when):
#     await asyncio.sleep(when)
#     print(what)
#
# async def stop_after(loop, when):
#     await asyncio.sleep(when)
#     loop.stop()
#
# print('00')
# loop = asyncio.get_event_loop()
#
# print('a')
# loop.create_task(say('first hello', 3))
# print('b')
# loop.create_task(say('second hello', 1))
# print('c')
# loop.create_task(say('third hello', 5))
# print('d')
# loop.create_task(stop_after(loop, 2))
# print('e')
# loop.run_forever()
# print('f')
# loop.close()
# print('g')

# import asyncio
# import time
# import random

import uasyncio as asyncio
import utime as time
import urandom as random


class FakeRobo:
    def __init__(self):
        self.led = True
        self.servo = 70
        self.timer = time.time()

        # this runs only run()
        # loop = asyncio.get_event_loop()
        # loop.create_task(self.run())
        # loop.run_forever()

        loop = asyncio.get_event_loop()
        asyncio.gather(self.run(),                # <-------------------------------
                       self.rand_duty())
        loop.run_forever()

    async def run(self):
        print('run?')
        while True:
            await asyncio.sleep(0.5)
            print('timer: {}; led: {}; servo: {}'.format(round(time.time() - self.timer, 3),
                                                         self.led,
                                                         self.servo))

    # # sync variant
    # def move_servo(self, new_duty):
    #     print('move_servo with {}'.format(new_duty))
    #     time.sleep(random.randint(1, 4))
    #     self.servo = new_duty

    # async var
    async def move_servo(self, new_duty):
        print('move_servo with {}'.format(new_duty))
        self.servo = new_duty
        await asyncio.sleep(random.randint(1, 4))

    async def rand_duty(self):
        while True:
            self.move_servo(random.randint(40, 110))
            await asyncio.sleep(random.randint(1, 4))


print('mark 0')
fr = FakeRobo()

# loop = asyncio.get_event_loop()
# # loop.create_task(self.run())
# loop.run_forever()
#
# print('mark 00')
# time.sleep(2)
# print('mark 02')
# fr.move_servo(40)
# print('mark 02.0')
# time.sleep(2)
# print('mark 04')
# time.sleep(2)
# print('mark 040')
# fr.move_servo(110)
# print('mark 0400')
# time.sleep(2)
print('mark 06')



