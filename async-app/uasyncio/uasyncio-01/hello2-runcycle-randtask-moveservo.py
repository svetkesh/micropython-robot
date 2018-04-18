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

import asyncio
import time
import random

class FakeRobo:
    def __init__(self):
        self.led = True
        self.servo = 70
        self.timer = time.time()
        self.pending_task = False
        self.pending_duty = 70

        # this runs only run()
        # loop = asyncio.get_event_loop()
        # loop.create_task(self.run())
        # loop.run_forever()

        loop = asyncio.get_event_loop()
        asyncio.gather(self.run(),
                       self.rand_duty(),
                       self.move_servo())
        loop.run_forever()

    async def run(self):
        print('run?')
        run_counter = 0
        while True:
            run_counter += 1
            await asyncio.sleep(0.5)
            print('run_counter: {}; timer: {}; led: {}; servo: {}'.format(
                run_counter,
                round(time.time() - self.timer, 3),
                self.led,
                self.servo))

    # # sync variant
    # def move_servo(self, new_duty):
    #     print('move_servo with {}'.format(new_duty))
    #     time.sleep(random.randint(1, 2))
    #     self.servo = new_duty

    # async var
    async def move_servo(self):
        while True:
            if self.pending_task:
                print('got task to move_servo with {}'.format(self.pending_duty))
                await asyncio.sleep(random.randint(1, 3))
                self.servo = self.pending_duty
                self.pending_task = False
                print('task done at {}'.format(round(time.time() - self.timer, 3)))
            await asyncio.sleep(random.randint(2, 4))

    async def rand_duty(self):
        while True:
            self.pending_duty = random.randint(40, 110)
            self.pending_task = True
            print('new task')
            # print('put task at {} for duty {}'.format(
            #     round(time.time() - self.timer, 3)),
            #     self.pending_duty)
            await asyncio.sleep(random.randint(1, 5))


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


## some tasks were ignored
## got task to move_servo with 73 < --

# mark 0
# new task
# got task to move_servo with 106
# run?
# run_counter: 1; timer: 0.501; led: True; servo: 70
# task done at 1.002
# run_counter: 2; timer: 1.002; led: True; servo: 106
# run_counter: 3; timer: 1.503; led: True; servo: 106
# run_counter: 4; timer: 2.004; led: True; servo: 106
# run_counter: 5; timer: 2.505; led: True; servo: 106
# run_counter: 6; timer: 3.006; led: True; servo: 106
# run_counter: 7; timer: 3.507; led: True; servo: 106
# run_counter: 8; timer: 4.008; led: True; servo: 106
# run_counter: 9; timer: 4.509; led: True; servo: 106
# new task
# got task to move_servo with 108
# run_counter: 10; timer: 5.01; led: True; servo: 106
# run_counter: 11; timer: 5.511; led: True; servo: 106
# run_counter: 12; timer: 6.012; led: True; servo: 106
# run_counter: 13; timer: 6.513; led: True; servo: 106
# run_counter: 14; timer: 7.014; led: True; servo: 106
# run_counter: 15; timer: 7.515; led: True; servo: 106
# task done at 8.003
# run_counter: 16; timer: 8.016; led: True; servo: 108
# run_counter: 17; timer: 8.517; led: True; servo: 108
# run_counter: 18; timer: 9.018; led: True; servo: 108
# run_counter: 19; timer: 9.519; led: True; servo: 108
# new task
# run_counter: 20; timer: 10.02; led: True; servo: 108
# run_counter: 21; timer: 10.521; led: True; servo: 108
# got task to move_servo with 50
# run_counter: 22; timer: 11.022; led: True; servo: 108
# run_counter: 23; timer: 11.523; led: True; servo: 108
# task done at 12.007
# run_counter: 24; timer: 12.023; led: True; servo: 50
# run_counter: 25; timer: 12.524; led: True; servo: 50
# run_counter: 26; timer: 13.025; led: True; servo: 50
# run_counter: 27; timer: 13.526; led: True; servo: 50
# run_counter: 28; timer: 14.027; led: True; servo: 50
# run_counter: 29; timer: 14.528; led: True; servo: 50
# new task
# got task to move_servo with 79
# run_counter: 30; timer: 15.03; led: True; servo: 50
# run_counter: 31; timer: 15.531; led: True; servo: 50
# task done at 16.011
# run_counter: 32; timer: 16.031; led: True; servo: 79
# run_counter: 33; timer: 16.532; led: True; servo: 79
# run_counter: 34; timer: 17.033; led: True; servo: 79
# run_counter: 35; timer: 17.534; led: True; servo: 79
# new task
# run_counter: 36; timer: 18.036; led: True; servo: 79
# run_counter: 37; timer: 18.537; led: True; servo: 79
# got task to move_servo with 73
# run_counter: 38; timer: 19.038; led: True; servo: 79
# run_counter: 39; timer: 19.539; led: True; servo: 79
# run_counter: 40; timer: 20.04; led: True; servo: 79
# run_counter: 41; timer: 20.541; led: True; servo: 79
# run_counter: 42; timer: 21.042; led: True; servo: 79
# run_counter: 43; timer: 21.544; led: True; servo: 79
# new task
# task done at 22.015
# run_counter: 44; timer: 22.044; led: True; servo: 100
# run_counter: 45; timer: 22.545; led: True; servo: 100
# run_counter: 46; timer: 23.046; led: True; servo: 100
# run_counter: 47; timer: 23.548; led: True; servo: 100
# run_counter: 48; timer: 24.048; led: True; servo: 100
# run_counter: 49; timer: 24.549; led: True; servo: 100
# run_counter: 50; timer: 25.05; led: True; servo: 100
# run_counter: 51; timer: 25.551; led: True; servo: 100
# run_counter: 52; timer: 26.052; led: True; servo: 100
# run_counter: 53; timer: 26.554; led: True; servo: 100
# new task
# run_counter: 54; timer: 27.055; led: True; servo: 100
# run_counter: 55; timer: 27.556; led: True; servo: 100
# got task to move_servo with 88
# run_counter: 56; timer: 28.056; led: True; servo: 100
# run_counter: 57; timer: 28.557; led: True; servo: 100
# run_counter: 58; timer: 29.058; led: True; servo: 100
# run_counter: 59; timer: 29.559; led: True; servo: 100
# run_counter: 60; timer: 30.06; led: True; servo: 100
# run_counter: 61; timer: 30.561; led: True; servo: 100
# new task
# task done at 31.019
#
