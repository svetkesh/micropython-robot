from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from kivy.properties import StringProperty

from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# Builder.load_string('''
# <ScrollableLabel>:
#     text: 'some really really long string ' * 100
#     Label:
#         text: root.text
#         font_size: 50
#         text_size: self.width, None
#         size_hint_y: None
#         height: self.texture_size[1]
# ''')

Builder.load_string('''
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        ScrollView:
            GridLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 60
                cols:1
                BoxLayout:                
                    Button:
                        size_hint: .3,1
                        text: 'button36'
                    Label:
                        text: 'label38'
                BoxLayout:                
                    Button:
                        size_hint: .4,1
                        text: 'button'
                    Label:
                        text: 'label'
                BoxLayout:                
                    Button:
                        size_hint: .5,1
                        text: 'button'
                    Label:
                        text: 'label'
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
        BoxLayout:
            size_hint: 1,.1
            Button:
                text: 'Home'
                font_size: 30
            Button:
                text: 'Play'
                font_size: 30
        
''')


# class ScrollableLabel(ScrollView):
#     # text = StringProperty('')
#     pass

class HomeScreen(Screen):
    # text = StringProperty('')
    pass


runTouchApp(HomeScreen())
