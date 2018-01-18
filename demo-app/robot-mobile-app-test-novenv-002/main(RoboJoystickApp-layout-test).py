# import kivy
# kivy.require('1.10.0') # replace with your current kivy version !

'''basic kivy layout examples -03

'''

from kivy.app import App

from kivy.uix.widget import Widget
from kivy.garden.joystick import Joystick

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class RoboPad(FloatLayout):
    def __init__(self, **kwargs):
        super(RoboPad, self).__init__(**kwargs)

        print('running super(Gamepad, self).__init__()')

        # joystickhand and joystickhead
        self.joystickhand = Joystick(size_hint=(.4, .4),
                                     pos_hint={'x':0.0, 'y':.2})
        self.add_widget(self.joystickhand)
        self.joystickhead = Joystick(size_hint=(.4, .4),
                                     pos_hint={'x':0.6, 'y':.2})
        self.add_widget(self.joystickhead)

        # add some buttons
        self.catchbutton = Button(size_hint=(.15, .15),
                                  pos_hint={'x': .8, 'y': .65},
                                  text='Catch me!')
        self.add_widget(self.catchbutton)


class RoboJoystickApp(App):
    def build(self):
        print('BasicApp.running build()')
        return RoboPad()  # goes how ?

        # more basic build
        # return Label(text='Hello')  # goes good


if __name__ == '__main__':
    print('running __main__()')
    RoboJoystickApp().run()
    print('quiting __main__()')

