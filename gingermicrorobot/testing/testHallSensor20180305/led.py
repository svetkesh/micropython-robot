class Led:
    """
    LED
     attached to GPIO (digital, D3 default),
     with wrap for desktop testing.

     :return LED value 1 - lighting
                       0 - LED is switched off

    Default used pin in 2 that is onboard blue led.

    Usage:
        #
        l = Led(light=0, pin=2)
        print('led: {}\nlight: {}'.format(l, l.light))

        l.light = 1
        print('led: {}\nlight: {}'.format(l, l.light))

        led2 = Led(name='Second LED', light=1, pin=4)
        print(led2)
        led2.light = 0
        print(led2)
        print(led2.light)

        >>
        led: INFO: object: {'_light': 0, 'pin': 2, 'name': 'led'}
               class: Led
                name: led
                 pin: 2
               light: 0
        light: 0
        led: INFO: object: {'_light': 1, 'pin': 2, 'name': 'led'}
               class: Led
                name: led
                 pin: 2
               light: 1
        light: 1
        INFO: object: {'_light': 1, 'pin': 4, 'name': 'Second LED'}
               class: Led
                name: Second LED
                 pin: 4
               light: 1
        INFO: object: {'_light': 0, 'pin': 4, 'name': 'Second LED'}
               class: Led
                name: Second LED
                 pin: 4
               light: 0
        0

    """
    def __init__(self, name='led', light=0, pin=2):
        self.name = name
        self._light = light
        self.pin = pin

    # def __repr__(self):
    #     return 'LED at pin: {}, light: {}'.format(
    #         self.pin,
    #         self.light,
    #     )

    def __str__(self):
        return 'INFO: object: {}\n' \
               '       class: {}\n' \
               '        name: {}\n' \
               '         pin: {}\n' \
               '       light: {}' \
            .format(self.__dict__,
                    self.__class__.__name__,
                    self.name,
                    self.pin,
                    self.light)

    @property
    def light(self):
        return self._light

    @light.setter
    def light(self, value):
        try:
            import machine
            pin_light = machine.Pin(self.pin, machine.Pin.OUT)
            # l2 = Pin(2, Pin.OUT)
            if self.light == 0:
                pin_light.off()
            else:
                pin_light.on()
            self._light = value

        except ImportError:
            self._light = value


# l = Led(light=0, pin=2)
# print('led: {}\nlight: {}'.format(l, l.light))
#
# l.light = 1
# print('led: {}\nlight: {}'.format(l, l.light))
#
# led2 = Led(name='Second LED', light=1, pin=4)
# print(led2)
# led2.light = 0
# print(led2)
# print(led2.light)


