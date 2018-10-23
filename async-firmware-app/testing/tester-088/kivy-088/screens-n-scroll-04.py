from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen  # , FadeTransition

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
        spacing: 10
        padding: 10
        Button:
            halign: 'center'
            id: welcome_settings
            size_hint: 1,.2
            text: 'Settings'
            font_size: 30
            on_release: app.root.current = 'settings_screen'
        Button:
            id: welcome_play
            size_hint: 1,.6
            text: 'Play'
            font_size: 30
            on_release: app.root.current = 'play_screen'
        Button:
            id: welcome_exit
            size_hint: 1,.2
            text: 'Exit'
            font_size: 30
            on_release: app.stop()

<SettingsScreen>:
    name: 'settings_screen'        
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10
        Button:
            size_hint: 1,.2
            text: 'Home'
            font_size: 30
            on_release: app.root.current = 'welcome_screen'
        ScrollView:
            size_hint: 1,.8
            spacing: 10
            padding: 10
            GridLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 60
                cols:1
                BoxLayout:                
                    Switch:
                        id: allow_overdrive
                        size_hint: .3,1
                        text: 'allow_overdrive'
                    Label:
                        text: 'allow_overdrive'
                BoxLayout:                
                    Label:
                        text: 'set_gear'
                BoxLayout:                
                    Slider:
                        id: set_gear
                        size_hint: .8, .8
                        min: 1
                        max: 4
                        value: 2
                        step: 1
                BoxLayout:                
                    Button:
                        size_hint: .3,1
                        text: 'button54'
                    Label:
                        text: 'label56'
                BoxLayout:                
                    Button:
                        size_hint: .3,1
                        text: 'button'
                    Label:
                        text: 'label'
                BoxLayout:                
                    Button:
                        size_hint: .3,1
                        text: 'button'
                    Label:
                        text: 'label'
                BoxLayout:                
                    Button:
                        size_hint: .3,1
                        text: 'button'
                    Label:
                        text: 'label'
                BoxLayout:                
                    Button:
                        size_hint: .4,1
                        text: 'button78'
                    Label:
                        text: 'label80'
                Button:
                    text: 'button82'
                Label:
                    text: 'label84'
                Button:
                    text: 'button86'
                Label:
                    text: 'label88'

<PlayScreen>:
    name: 'play_screen'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Play!'
            font_size: 30
        Image:
            source: 'colours2.png'
            allow_stretch: True
            keep_ratio: False
        BoxLayout:
            size_hint: 1,.1
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

    def sys_exit(self):
        App.get_running_app().stop()


if __name__ == "__main__":
    MicrorobotScreen().run()