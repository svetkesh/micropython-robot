# import curses
#
# def main(stdscr):
#     # do not wait for input when calling getch
#     stdscr.nodelay(1)
#     while True:
#         # get keyboard input, returns -1 if none available
#         c = stdscr.getch()
#         if c != -1:
#             # print numeric value
#             stdscr.addstr(str(c) + ' ')
#             stdscr.refresh()
#             # return curser to start position
#             stdscr.move(0, 0)
#
# if __name__ == '__main__':
#     curses.wrapper(main)

# #!/usr/bin/env python
#
# import curses
# import curses.textpad
# import time
#
# stdscr = curses.initscr()
#
# #curses.noecho()
# #curses.echo()
#
#
# begin_x = 20
# begin_y = 7
# height = 5
# width = 40
# win = curses.newwin(height, width, begin_y, begin_x)
# tb = curses.textpad.Textbox(win)
# text = tb.edit()
# curses.addstr(4,1,text.encode('utf_8'))
#
# #hw = "Hello world!"
# #while 1:
# #    c = stdscr.getch()
# #    if c == ord('p'):
# #    elif c == ord('q'): break # Exit the while()
# #    elif c == curses.KEY_HOME: x = y = 0
#
# curses.endwin()

# import pygame, time
# from pygame.locals import *
#
# pygame.init()
# screen = pygame.display.set_mode((640, 480))
# pygame.display.set_caption('Pygame Keyboard Test')
# pygame.mouse.set_visible(0)
#
#
# while True:
#
#     print( "doing a function")
#
#     for event in pygame.event.get():
#       if (event.type == KEYUP) or (event.type == KEYDOWN):
#          print( "key pressed")
#          time.sleep(0.1)


# controller
# from pynput.keyboard import Key, Controller
#
# keyboard = Controller()
#
# # Press and release space
# keyboard.press(Key.space)
# keyboard.release(Key.space)
#
# # Type a lower case A; this will work even if no key on the
# # physical keyboard is labelled 'A'
# keyboard.press('a')
# keyboard.release('a')
#
# # Type two upper case As
# keyboard.press('A')
# keyboard.release('A')
# with keyboard.pressed(Key.shift):
#     keyboard.press('a')
#     keyboard.release('a')
#
# # Type 'Hello World' using the shortcut type method
# keyboard.type('Hello World')

# monitoring
from pynput import keyboard

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()