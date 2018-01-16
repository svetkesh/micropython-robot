'''
testing raw socket connection
compiled android app no gui - OK).py
'''

import socket
from time import sleep

robot_host = '192.168.101.104'  # hardcodedrobot ip t4m net
robot_port = 80


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number



    posx = 0.1

    while posx < 0.99:
        try:
            client_socket = socket.socket()  # instantiate
            client_socket.connect((robot_host, robot_port))  # connect to the server
            message = 'http://192.168.4.1/?headx=' + str(posx)  # take input
            client_socket.send(message.encode())  # send message

            client_socket.close()  # close the connection
            sleep(3)
            #
            print('posx {} sent'.format(message))
        except:
            print('posx not sent {}'.format(posx))

        posx += 0.1



if __name__ == '__main__':
    client_program()
