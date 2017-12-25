import machine
motor_a_p = machine.PWM(machine.Pin(5), freq=50)
motor_a_m = machine.PWM(machine.Pin(0), freq=50)
serv = machine.PWM(machine.Pin(12), freq=50)

print('robot demo-app 010 running...')

directions = ['s', 'f', 'ff', 'l', 'r', 'b', 'bb', 'q']
direction = 's'                                    # default direction "stop"
command = 'run'
# default "stop"


def run(direction):
    try:
        if direction == 's':
            motor_a_p.duty(0)
            motor_a_m.duty(1)
            serv.duty(60)
            print('Go "STOP"')

        elif direction == 'f':
            motor_a_p.duty(1000)
            motor_a_m.duty(1)
            print('Go "Forward"')

        elif direction == 'ff':
            motor_a_p.duty(2000)
            motor_a_m.duty(1)
            print('Go "Fast Forward"')

        elif direction == 'l':
            serv.duty(10)
            print('Go "Left"')

        elif direction == 'r':
            serv.duty(110)
            print('Go "Right"')

        elif direction == 'b':
            motor_a_p.duty(1000)
            motor_a_m.duty(-1)
            serv.duty(60)
            print('Go "Backward"')

        elif direction == 'bb':
            motor_a_p.duty(2000)
            motor_a_m.duty(-1)
            print('Go "Fast Backward"')

        else:
            print('Unknown direction')
    except:
        print('direction is {}'.format(direction))

while True:
    command = input("Plese set direction f,ff,l,r,b,bb; s to stop, q to quit ")
    if command == 'q':
        print('Thanks, quiting now')
        break
    else:
        run(command)
