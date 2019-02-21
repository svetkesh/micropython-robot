# http://192.168.4.1/?&run={"turnx": 77, "runy": 50}

import time
import socket
import random

robots = {
    'protected_robot_host': '192.168.4.1',
    'unprotected_robot_host': '192.168.4.1',
}
# robot_host = '192.168.4.1'
# robot_port = 80

command_heads = [
    'http://192.168.4.1/?&run={"turnx":"',
    'http://192.168.4.1/?&run={"runy":"',
]
# command_tail = '"}\&'


gear_head = 'http://192.168.4.1/?&run={"gear":"'


def generare_command_value(center=50, offset=49):
    if (center - offset) < 1 or (center + offset) > 99:
        return random.randint(1, 99)
    else:
        return random.randint(center - offset, center + offset)


def send_command(command_head,
                 command,
                 timeout_responce = 1,
                 robot_host='192.168.4.1',
                 robot_port=80,
                 # command_tail='"}\&',
                 command_tail='"}',
                 center=50,
                 offset=49,
                 recovery_timeout=12,
                 debug_msg=False
                 ):
    # str_commands = command_head + str(generare_command_value(center, offset)) + command_tail
    str_commands = command_head + str(command) + command_tail
    try:
        # print('DBG start sending command send_command_data_with_saved_params: {}'.format(str_commands))
        client_socket = socket.socket()  # instantiate
        client_socket.settimeout(timeout_responce)
        client_socket.connect((robot_host, robot_port))  # connect to the server
        client_socket.send(str_commands.encode())  # encode than send message
        #
        if debug_msg:
            print(str_commands.encode())  # command like :
        client_socket.close()  # close the connection
        # print('DBG command sent send_command_data_with_saved_params: {}'.format(str_commands))
        return True
    except socket.timeout as e:
        if debug_msg:
            print('ERR: connection lost after {}s, {} {}'.format(timeout_responce, type(e), e))
        time.sleep(recovery_timeout)
        return False
    except Exception as e:
        if debug_msg:
            print('ERR: command not sent {} {}'.format(type(e), e))
        return True


def send_commands_runy(commands):
    str_commands = 'http://192.168.4.1/?&run={"turnx":"' + str(commands) + '"}\&'
    try:
        print('DBG start sending command send_command_data_with_saved_params: {}'.format(str_commands))
        client_socket = socket.socket()  # instantiate
        client_socket.connect((robot_host, robot_port))  # connect to the server
        client_socket.send(str_commands.encode())  # encode than send message
        #
        print(str_commands.encode())  # command like :
        client_socket.close()  # close the connection
        print('DBG command sent send_command_data_with_saved_params: {}'.format(str_commands))
    except Exception as e:
        print('ERR: command not sent {} {}'.format(type(e), e))


def send_commands_headx(commands):
    #  self.current_command['headx'] = self.recalculate_servo_position(x)
    str_commands = 'http://192.168.4.1/?&run={"runy":"' + str(commands) + '"}\&'
    try:
        print('DBG start sending command send_command_data_with_saved_params: {}'.format(str_commands))
        client_socket = socket.socket()  # instantiate
        client_socket.connect((robot_host, robot_port))  # connect to the server
        client_socket.send(str_commands.encode())  # encode than send message
        #
        print(str_commands.encode())  # command like :
        client_socket.close()  # close the connection
        print('DBG command sent send_command_data_with_saved_params: {}'.format(str_commands))
    except Exception as e:
        print('ERR: command not sent {} {}'.format(type(e), e))


# step = 5
# timeout = 0.5
# cycles = 10

# # send_commands_runy
# for i in range(0, 100, 5):
#     send_commands_runy(str(i))
#     listen = input('Send next?')

# for i in range(40, 116, step):
#     # send_commands_headx(str(i))
#     print(generare_command_value(90, 5))
#     listen = input('Send next?')
#     # time.sleep(timeout)


# auto send_commands_headx

# for t in range(100, 0, -1):
#     timeout = t / 1000
#     time.sleep(random.randint(1, 5))
#     print('DBG current timeout: {}'.format(timeout))
#     for i in range(40, 116, step):
#         send_commands_headx(str(i))
#         # listen = input('Send next?')
#         time.sleep(timeout)


# fault_counter = 0
# total_counter = 0
# sleep = 0.2

# stats = {}
# sleeps = [0.99, 0.50, 0.30, 0.20, 0.15, 0.10, 0.05]
# test_quantity = 10


def test_run(test_quantity=10,
             sleeps=[0.99, 0.50, 0.30, 0.20, 0.15, 0.10, 0.05],
             commands_hardness=2,  # qty of same commands to be sent as ESP try to soften and can ignore/half the value
             debug_msg=False
             ):
    stats = {}

    for sleep in sleeps:
        fault_counter = 0
        total_counter = 0
        # sleep = s / 100
        # sleep = 0.05

        for i in range(test_quantity):
            try:
                for header in command_heads:
                    total_counter += 1

                    c = generare_command_value(50, 49)
                    if debug_msg:
                        print('Command {}: {}'.format(total_counter, c))

                    for hard in range(commands_hardness):
                        sended = send_command(header, c, timeout_responce=1)
                        #  repeat commands to override chips lazy command fulfilment

                    # print(sended)
                    if not sended:
                        fault_counter += 1
                        if debug_msg:
                            print('Faulted {}: {} {}'.format(total_counter, sended, fault_counter))

                    time.sleep(sleep)
                    stats[sleep] = fault_counter / total_counter

            except Exception as e:
                if debug_msg:
                    print('ERR: command not sent {} {}'.format(type(e), e))

            finally:
                if debug_msg:
                    print('Commands sent {} errors {} . Timeout {}'.format(total_counter, fault_counter, sleep))
    print(stats)

    for k in stats:
        print(k, '\t', stats[k])


def main():
    test_started = time.time()
    print("Test started at {}".format(time.asctime()))

    hardness = [1, 2, 3]  # repeat same command to override lazy esp
    gears = [2, 3, 4, 5]  # gear used for motor speed
    sleep_timeouts = [0.99, 0.50, 0.30, 0.20, 0.15, 0.10, 0.05, 0.01]
    butch_quantity = 2  # qty of tests in single butch, repeat for same settings

    for hard in hardness:
        print("Set hardness = {}".format(hard))
        for gear in gears:
            send_command(command_head=gear_head, command=gear)
            print("... hardness = {}, Set gear = {}".format(hard, gear))
            test_run(test_quantity=butch_quantity,
                     sleeps=sleep_timeouts,
                     commands_hardness=hard)

    print("Tests total:{}, elapsed: {}".format(len(hardness) * len(gears) * len(sleep_timeouts) * butch_quantity,
                                               time.time() - test_started))


if __name__ == "__main__":
    main()
