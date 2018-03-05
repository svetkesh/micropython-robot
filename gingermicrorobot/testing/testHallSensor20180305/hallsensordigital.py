class HallSensorDigital:
    """
    Hall Sensor
     for type A3144 or KY-003
     attached to GPIO (digital, D3 default),
     with wrap for desktop testing.

     See:
     https://tkkrlab.nl/wiki/Arduino_KY-003_Hall_magnetic_sensor_module

     :return sensor value 1 - no magnet
                          0 - feel magnet
                           (in my case about 3mm(1/10 in))

    Usage:
        hsd = HallSensorDigital()
        print(hsd.sensor)

        hsd5 = HallSensorDigital(pin=5)
        print(hsd5.sensor)
        >>
        1
        1
        ...
        outputs will be
        0 or 1
        0 or 1

    Status: still in draft, getter-setter ...

    """
    def __init__(self, sensor=1, pin=3):
        self.sensor = sensor
        self.pin = pin

    @property
    def sensor(self):

        # print('DBG: Hall sensor is probing @pr')

        try:
            import machine
            pin_sensor = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
            self.__sensor = pin_sensor.value()

        except ImportError:
            import random
            self.__sensor = random.randint(0, 1)

        return self.__sensor

    # do this really necessary?
    @sensor.setter
    def sensor(self, sensor):

        print('DBG: Hall sensor is probing')

        try:
            import machine
            pin_sensor = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
            self.__sensor = pin_sensor.value()

        except ImportError:
            import random
            self.__sensor = random.randint(0, 1)

#
# hsd5 = HallSensorDigital(pin=5)
# print(hsd5.sensor)
# print(hsd5.sensor)
# print(hsd5.sensor)
# print(hsd5.sensor)
# print(hsd5.sensor)
# print(hsd5.sensor)
