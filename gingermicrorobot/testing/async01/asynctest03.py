from pynput import keyboard
import asyncio
import time
import sys, signal


def signal_handler(signal, frame):
    loop.stop()
    # client.close()
    sys.exit(0)


def on_press(key):
    print('Key {} pressed.'.format(key))
    return False


def on_release(key):
    print('Key {} released.'.format(key))
    if str(key) == 'Key.esc':
        print('Exiting...')
        # return False


# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()


async def kb():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        await listener.join()


signal.signal(signal.SIGINT, signal_handler)

loop = asyncio.get_event_loop()

# asyncio.ensure_future(speak_async())
asyncio.ensure_future(kb())
loop.run_forever()
