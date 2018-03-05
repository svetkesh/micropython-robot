class Led:
    """
    LED
     attached to GPIO (digital, D3 default),
     with wrap for desktop testing.

     :return LED value 1 - lighting
                       0 - LED is dark

    Usage:

    """
    def __init__(self, light=1, pin=4):
        self.light = light
        self.pin = pin

    @property
    def light(self):
        return self.__light

    @light.setter
    def light(self, light):
        try:
            from machine import Pin
            pin_light = machine.Pin(self.pin, machine.Pin.OUT)
            if self.light == 0:
                pin_light.off()
            else:
                pin_light.on()
            self.__light = self.light

        except ImportError:
            self.__light = self.light

l=Led(light=0, pin=2)

