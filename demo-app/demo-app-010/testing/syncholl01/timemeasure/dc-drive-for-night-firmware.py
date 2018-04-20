'''
test dc drive
for night firmwares
'''
import machine
import utime as time

measure_timeout = 2
step_drive = 250

motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
while True:
    for p_duty in range(-1200, 1200, step_drive):
        for m_duty in range(-1200, 1200, step_drive):
            motor_a_p.duty(p_duty)
            motor_a_m.duty(m_duty)
            print('p: {} ; m: {}'.format(
                p_duty,
                m_duty
            ))
            time.sleep(measure_timeout)
