class Led:
    """
    LED
     attached to GPIO (digital, D3 default),
     with wrap for desktop testing.

     :return LED value 1 - lighting
                       0 - LED is dark

    Usage:
        #
        l = Led(light=0, pin=2)
        print(l, l.light)

        l.light = 1
        print(l, l.light)
        >>
        LED at pin: 2, light: 0 0
        LED at pin: 2, light: 1 1

    """
    def __init__(self, light=0, pin=4):
        self._light = light
        self.pin = pin

    def __repr__(self):
        return 'LED at pin: {}, light: {}'.format(
            self.pin,
            self.light,
        )

    @property
    def light(self):
        return self._light

    @light.setter
    def light(self, value):
        try:
            from machine import Pin
            pin_light = machine.Pin(self.pin, machine.Pin.OUT)
            if self.light == 0:
                pin_light.off()
            else:
                pin_light.on()
            self._light = value

        except ImportError:
            self._light = value




