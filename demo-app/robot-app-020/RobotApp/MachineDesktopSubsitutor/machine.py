# import logging

class Pin:
    """
    Place holder for uPython machine.Pin
    """

    # " ...Available pins are: 0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16,
    # which correspond to the actual GPIO pin numbers of ESP8266 chip
    # ..."
    # https://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html#pins-and-gpio

    ESP8266AvailablePins = (0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16)

    assigned_pins = set()

    def __init__(self, pin):
        if pin in Pin.ESP8266AvailablePins:
            if pin not in Pin.assigned_pins:
                Pin.assigned_pins.add(pin)
                self.pin = pin

                # some introspection
                # print('DBG: Pin.assigned_pins : {}'.format(
                #     Pin.assigned_pins
                # ))
                # >> DBG: Pin.assigned_pins : {5, 15}
            else:
                raise ValueError('ERR: cannon initialize already assigned Pin : {}'.format(pin))

        else:
            raise ValueError('ERR: cannon initialize Pin : {}'.format(pin))

    def __repr__(self):
        return 'Pin connected : {}'.format(
            self.pin
        )


class PWM:
    """
    Place holder for uPython machine.PWM class
    """

    # import Pin

    def __init__(self, pin, freq=50):
        self.pin = pin
        self.freq = freq

    def __repr__(self):
        return 'Using Pin : {}\nFrequency : {}'.format(
            self.pin,
            self.freq
        )

    def duty(self, value):
        """
        Workaround to allow running micropython PWM module launch on desktop
        and run .duty() method
        :param value: to set angle for servodrive or current for DC motor
        :return: text analogue of fulfilling motion by servo drive or DC motor rotation.
        """
        print('DBG: MachineDesktopSubsitutor recieved command duty :{}'.format(
            str(value)
        ))
        return value


def main():
    sevr_catch = PWM(Pin(15), freq=50)
    print(sevr_catch)
    direction = 70
    sevr_catch.duty(direction)

    # test - should raise err
    try:
        # initialization goes smooth
        servo5 = PWM(Pin(5), freq=50)

        print(servo5)
        # Using Pin: Pin connected: 5
        # Frequency: 50

        servo5.duty(71)
        # DBG: MachineDesktopSubsitutor  recieved command duty: 71


        # initialization checked and raised ValueError
        # servo15 = PWM(Pin(15), freq=50)  #<class 'ValueError'> ERR: cannon initialize already assigned Pin : 15
        # servo6 = PWM(Pin(6), freq=50)  # <class 'ValueError'> ERR: cannon initialize Pin : 6
    except ValueError as valerr:
        print(type(valerr), valerr)


if __name__ == '__main__':
    main()