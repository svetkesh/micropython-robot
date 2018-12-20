from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
# from kivy.garden.joystick import Joystick
from kivy.uix.popup import Popup
from kivy.uix.button import Button


from kivy.uix.screenmanager import ScreenManager, Screen  # , FadeTransition

import time
import random


class WelcomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    def out_pad(self):
        print('SettingsScreen says hello from button54')

    def use_default_wifi_settings(self):
        print("Use Default WiFi Settings pressed")

    def add_to_wifi_network(self):
        print("Add to WiFi Network pressed")
        print(self.ids["wifissid"].text , self.ids["wifipass"].text)

    def fire_popup(self):
        print("Fire PopUp from SettingsScreen")
        pops=SimplePopup()
        pops.open()

    def fire_color_popup(self):
        print("Fire Color PopUp from SettingsScreen")
        pops=ColorPopup()
        pops.open()


class SimplePopup(Popup):
    pass


class ColorPopup(Popup):
    # def color_popup(self):
    #     print(self.ids["colorpopup"].hex_color)

    def color_show(self):
        print(self.ids["colorpopup"].hex_color)


# class SimpleButton(Button):
#     text = "Fire Popup !"
#
#     def fire_popup(self):
#         pops=SimplePopup()
#         pops.open()


class AdvancedSettingsScreen(Screen):
    pass


class PlayScreen(Screen):
    def out_pad(self):
        print('PlayScreen says hello from button54')
        print(self)
        # self.parent
        self.parent.current = 'welcome_screen'

    def joy_hand(self, caller):
        # print('hello from joystick', caller)  # caller returns name of event
        print('hello from joystick', caller, self.ids["joystick_hand"].pad)

    def joy_run(self, caller):
        # print('hello from joystick', caller)  # caller returns name of event
        print('hello from joystick', caller, self.ids["joystick_run"].pad)


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
#:import Joystick kivy.garden.joystick
#:import TextInput kivy.uix.textinput
#:import ColorPicker kivy.uix.colorpicker
MicrorobotScreen:
    transition: FadeTransition()
    WelcomeScreen:
    SettingsScreen:
    AdvancedSettingsScreen:
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
                spacing: 10
                padding: 10
                BoxLayout:
                    Button:
                        font_size: 30
                        # padding: 10
                        size_hint: 1,1
                        text: 'Use Default WiFi Settings'
                        on_release: root.use_default_wifi_settings()



                Button:
                    font_size: 30
                    # padding: 10
                    size_hint: 1,1
                    text: 'Add to WiFi Network'
                    on_release: root.add_to_wifi_network()
                TextInput:
                    id: wifissid
                    multiline: False
                    
                TextInput:
                    id: wifipass
                    password: True 
                    multiline: False
                        
                        
                Button:
                    font_size: 30
                    # padding: 10
                    size_hint: 1,1
                    text: ' Test PopUp root.fire_popup()'
                    on_release: root.fire_popup()
                    #self.fire_popup()
                    
                Button:
                    font_size: 30
                    # padding: 10
                    size_hint: 1,1
                    text: 'Select Color root.fire_color_popup()'
                    on_release: root.fire_color_popup()
                    #self.fire_popup()
                
                BoxLayout:
                    Button:
                        font_size: 30
                        # padding: 10
                        size_hint: 1,1
                        text: 'Add to WiFi Network'
                        on_release: root.add_to_wifi_network()
                
                BoxLayout:
                
                BoxLayout:
                
                BoxLayout:
                
                    
                # Path to Advanced Settings
                Button:
                    size_hint: 1,.2
                    text: 'Advanced Settings'
                    font_size: 30
                    on_release: app.root.current = 'advanced_settings_screen'  
                     
<AdvancedSettingsScreen>
    name: 'advanced_settings_screen'        
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10
        Button:
            size_hint: 1,.2
            text: 'Back to Settings'
            font_size: 30
            on_release: app.root.current = 'settings_screen'
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
                    Label:
                        text: 'allow_overdrive'

                BoxLayout:                
                    Switch:
                        id: invert_turn
                        size_hint: .3,1
                    Label:
                        text: 'invert_turn'

                BoxLayout:                
                    Switch:
                        id: invert_run
                        size_hint: .3,1
                    Label:
                        text: 'invert_run'
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
                    Slider:
                        id: set_gear_2
                        size_hint: .8, .8
                        min: 1
                        max: 4
                        value: 2
                        step: 1
                    Label:
                        text: 'set_gear_2' 
                BoxLayout:                
                    Button:
                        size_hint: .3,1
                        text: 'button54'

                        on_release: root.out_pad() # here root is pointed to class SettingsScreen

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
    orientation: 'horizontal'

    FloatLayout:
        # orientation: 'vertical'
        orientation: 'horizontal'

        Button:
            size_hint: .3,1
            text: 'Play_button54'

            on_release: root.out_pad() # here root is pointed to class SettingsScreen

        Joystick:
            id: joystick_hand
            size_hint: .4, .4
            # pos_hint: {'x':.5, 'y':.5}
            pos_hint: {'center_x':.2, 'center_y':.5}
            sticky: True

            # ##
            on_touch_down: root.joy_hand("joystick_hand on_touch_down")
            on_touch_move: root.joy_hand("joystick_hand on_touch_move")
            on_touch_up: root.joy_hand("joystick_hand on_touch_up")            


        Joystick:
            id: joystick_run
            size_hint: .4, .4
            pos_hint: {'center_x':.8, 'center_y':.5}
            # sticky: True


            on_touch_down: root.joy_run("joystick_run on_touch_down")
            on_touch_move: root.joy_run("joystick_run on_touch_move")
            on_touch_up: root.joy_run("joystick_run on_touch_up")


# Popup machine customization        
<SimpleButton>:
    on_press: self.fire_popup()
<SimplePopup>:
    id:pop
    size_hint: .4, .4
    auto_dismiss: False
    title: 'Hello world!!'
    Button:
        text: 'Click here to dismiss'
        on_press: pop.dismiss()
        

# it's OK
# <ColorPopup>:
#     id:pop
#     size_hint: .4, .4
#     auto_dismiss: False
#     title: 'Hello world!!'
#     ColorPicker:
#         id: colorpopup
#         on_color: root.color_show()   # #######
#         on_touch_up: pop.dismiss()

# <ColorPopup>:
#     id:pop
#     size_hint: .4, .4
#     auto_dismiss: False
#     title: 'Select Color'
#     ColorPicker:
#         id: colorpopup
#         on_color: root.color_show()   # #######
#         on_touch_up: pop.dismiss()

    #     orientation: 'vertical'
    #     FloatLayout:
    #         Joystick:
    #             id: joystick_hand
    #             size_hint: .5, .5
    #             pos_hint: .0, .0
    #             # sticky: True
    #         Joystick:
    #             id: joystick_run
    #             size_hint: .5, .5
    #             pos_hint: .0, .0
    #             # sticky: True
    #     BoxLayout:
    #         size_hint: 1,.1
    #         Button:
    #             text: 'Home'
    #             font_size: 30
    #             on_release: app.root.current = 'welcome_screen'
    #         Button:
    #             text: 'Settings'
    #             font_size: 30
    #             on_release: app.root.current = 'settings_screen'

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