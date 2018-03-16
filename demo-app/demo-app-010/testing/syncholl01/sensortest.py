import machine
import utime as time

hall_sensor_a = machine.ADC(0)  #ADC connector
hall_sensor_d = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

networkpin = machine.Pin(2, machine.Pin.OUT)
networkpin.off()

while True:
    print('DBG: sensor D(): {}, '
          'sensor A(): {} '
          'at: {}'.format(hall_sensor_d.value(),
                          hall_sensor_a.read(),
                          time.time()))
    networkpin.off()
    time.sleep(0.1)
    if ((hall_sensor_d.value() == 0)or(hall_sensor_a.read() < 1024)):
        networkpin.on()

