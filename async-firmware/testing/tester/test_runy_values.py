# http://192.168.4.1/?&run={"turnx": 77, "runy": 50}

import time
import socket
import random

robot_host = '192.168.4.1'
robot_port = 80


def send_commands_runy(commands):
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


def send_commands_headx(commands):
    #  self.current_command['headx'] = self.recalculate_servo_position(x)
    str_commands = 'http://192.168.4.1/?&run={"headx":"' + str(commands) + '"}\&'
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


step = 5
timeout = 0.5
cycles = 10

# # send_commands_runy
# for i in range(0, 100, 5):
#     send_commands_runy(str(i))
#     listen = input('Send next?')

for i in range(40, 116, step):
    send_commands_headx(str(i))
    listen = input('Send next?')
    # time.sleep(timeout)


# auto send_commands_headx

# for t in range(100, 0, -1):
#     timeout = t / 1000
#     time.sleep(random.randint(1, 5))
#     print('DBG current timeout: {}'.format(timeout))
#     for i in range(40, 116, step):
#         send_commands_headx(str(i))
#         # listen = input('Send next?')
#         time.sleep(timeout)
