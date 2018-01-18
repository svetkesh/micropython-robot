'''basic kivy layout examples -01

'''

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        print('running super(LoginScreen, self).__init__()')
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 3
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        # one way to add widget to root
        self.add_widget(Label(text='one way to add widget / unnamed or indexed'))

        # second way to add named widget
        self.namedwidget6 = Label(text='I\'m namedwidget6')
        self.add_widget(self.namedwidget6)

        self.textinput7 = TextInput(multiline=True)
        self.add_widget(self.textinput7)

        self.button8 = Button(text='button8')
        self.add_widget(self.button8)


class BasicApp(App):
    def build(self):
        print('BasicApp.running build()')
        return LoginScreen()  # goes good

        # more basic build
        # return Label(text='Hello')  # goes good


if __name__ == '__main__':
    print('running __main__()')
    BasicApp().run()
    print('quiting __main__()')
