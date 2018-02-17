class Pin:
    """
    Place holder for uPython machine.Pin
    """

    # " ...Available pins are: 0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16,
    # which correspond to the actual GPIO pin numbers of ESP8266 chip
    # ..."
    # https://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html#pins-and-gpio

    ESP8266AvailablePins = (0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16)

    def __init__(self, pin):
        nonlocal ESP8266AvailablePins
        if pin in ESP8266AvailablePins:
            self.pin = pin
        else:
            print('ERR: cannon initialize Pin : {}'.format(pin))

    def __repr__(self):
        return 'Pin connected : {}'.format(
            self.pin
        )


class PWM:
    """
    Place holder for uPython machine.PWM class

    sevr_catch = machine.PWM(machine.Pin(15), freq=50)
    serv_direction.duty(directionx)
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
        print('DBG: MachineDesktopSubsitutor recieved command duty :{}'.format(
            str(value)
        ))
        return value


def main():
    sevr_catch = PWM(Pin(15), freq=50)
    print(sevr_catch)
    direction = 70
    sevr_catch.duty(direction)


if __name__ == '__main__':
    main()