''' This test for Joystick.
This test for Joystick layout.


'''

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import time


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 3
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.add_widget(Label(text='test3'))
        self.text4 = Label(text='text4')
        self.add_widget(self.text4)

        # test out of bond widget
        self.add_widget(Label(text='tex5'))
        self.text6 = Label(text='text6')
        self.add_widget(self.text6)
        print('running LoginScreen.__init__()')


class BasicApp(App):
    '''
    BasicApp class definition.
    '''
    print('BasicApp body running')

    def build(self):
        '''
        implements its build() method so it
        :return: Widget instance (the root of your widget tree)
        '''
        print('def build running')
        # return Label(text='Hello')
        return LoginScreen()


if __name__ == '__main__':
    BasicApp().run()
    print('I\'ve done )')
