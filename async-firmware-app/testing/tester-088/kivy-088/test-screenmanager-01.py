from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen #, FadeTransition

import time
import random


class WelcomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class PlayScreen(Screen):
    pass


class MicrorobotScreen(ScreenManager):
    pass



# class MyScreenManager(ScreenManager):
#     def new_colour_screen(self):
#         name = str(time.time())
#         s = ColourScreen(name=name,
#                          colour=[random.random() for _ in range(3)] + [1])
#         self.add_widget(s)
#         self.current = name


root_widget = Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
MicrorobotScreen:
    transition: FadeTransition()
    WelcomeScreen:
    SettingsScreen:
    PlayScreen:
<WelcomeScreen>:
    name: 'welcome_screen'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Welcome!'
            font_size: 30
        Image:
            source: 'colours.png'
            allow_stretch: True
            keep_ratio: False
        BoxLayout:
            Button:
                text: 'Play'
                font_size: 30
                on_release: app.root.current = 'play_screen'
            Button:
                text: 'Settings'
                font_size: 30
                on_release: app.root.current = 'settings_screen'

<SettingsScreen>:
    name: 'settings_screen'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Settings!'
            font_size: 30
        Image:
            source: 'colours2.png'
            allow_stretch: True
            keep_ratio: False
        BoxLayout:
            Button:
                text: 'Home'
                font_size: 30
                on_release: app.root.current = 'welcome_screen'
            Button:
                text: 'Play'
                font_size: 30
                on_release: app.root.current = 'play_screen'
                
<PlayScreen>:
    name: 'play_screen'
    BoxLayout:
        orientation: 'horizontal'
        Label:
            text: 'Play!'
            font_size: 30
        Image:
            source: 'colours2.png'
            allow_stretch: True
            keep_ratio: False
        BoxLayout:
            Button:
                text: 'Home'
                font_size: 30
                on_release: app.root.current = 'welcome_screen'
            Button:
                text: 'Settings'
                font_size: 30
                on_release: app.root.current = 'settings_screen'

''')




# class ScreenManagerApp(App):
#     def build(self):
#         return root_widget

# ScreenManagerApp().run()

class MicrorobotScreen(App):
    def build(self):
        return root_widget


if __name__ == "__main__":
    MicrorobotScreen().run()