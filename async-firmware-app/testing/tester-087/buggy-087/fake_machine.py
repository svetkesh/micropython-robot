"""
testing class infrastructure according to scheme 0.8.7
"""

class Pin:
    def __init__(self, pin):
        self.pin = pin

    def __repr__(self):
        return str(self.pin)


class PWM:
    # freq = 50
    def __init__(self, Pin, freq=50):
        # self.pin = pin   # seems to be OK
        self.Pin = Pin     # seems to be OK
        self.freq = freq

    def __repr__(self):
        return self.__class__.__name__ + ' ' + str(id(self)) + ' at Pin ' + str(self.Pin)

    def duty(self, duty):
        print(str(duty))
        return duty


some_pin = Pin(4)
print(some_pin)

# some_pwm = PWM(some_pin, freq=50)  # init OK
# some_pwm = PWM(some_pin)           # init OK

some_pwm = PWM(some_pin, freq=50)
print(some_pwm)
some_pwm.duty(55)
