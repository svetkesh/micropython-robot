from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.lang import Builder

Builder.load_string('''
<JoystickPad>:
    id: pad
    canvas:

        ###  Background  ###
        Color:
            rgba: self._background_color
        Ellipse:
            pos: (self.center_x - self._radius), (self.center_y - self._radius)
            size: (self._diameter, self._diameter)

        ###  Border  ###
        Color:
            rgba: self._line_color
        Line:
            circle: (self.center_x, self.center_y, (self._diameter - (self._line_width * 2)) / 2)
            width: self._line_width
''')


class JoystickPad(Widget):
    _diameter = NumericProperty(1)
    _radius = NumericProperty(1)
    _background_color = ListProperty([0, 0, 0, 1])
    _line_color = ListProperty([1, 1, 1, 1])
    _line_width = NumericProperty(1)
