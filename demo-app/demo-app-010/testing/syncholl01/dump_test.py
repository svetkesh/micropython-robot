import socket
import time


robot_host = '192.168.4.1'  # hardcoded robot ip t4m net
robot_port = 80

for cycle in range(0, 1000, 1):
    for inner_counter in range(0, 100, 1):



        # dict_commands = {'headx': headx, 'handy': handy, 'turnx': turnx, 'runy': runy, 'catch': catch}

        # # D5
        # headx = inner_counter / 100
        # dict_commands = {'headx': headx}

        # # D7
        # handy = inner_counter / 100
        # dict_commands = {'handy': handy}

        # # D6
        # turnx = inner_counter / 100
        # dict_commands = {'turnx': turnx}
        #
        # # motor line A
        runy = inner_counter / 100
        dict_commands = {'runy': runy}

        # # D8 not such way...
        # catch = inner_counter / 100
        # dict_commands = {'catch': catch}
        # print(dict_commands)

        str_commands = 'http://' + str(robot_host) + '/?'

        for item in dict_commands:
            # print(item,
            #       dict_commands[item],
            #       type(dict_commands[item])
            #       )
            # if dict_commands[item] !='z':
            #     str_commands += item +\
            #                     '=' + \
            #                     dict_commands[item] + \
            #                     '&'

            # add normalization
            if dict_commands[item] != 'z':
                if dict_commands[item] != 'catch':
                    str_commands += item + \
                                    '=' + \
                                    str('{0:.2f}'.format(float(dict_commands[item]))) + \
                                    '&'

                    #               str('{0:.2f}'.format((float(dict_commands[item]) + 1) / 2)) + \

                else:
                    str_commands += item + \
                                    '=' + \
                                    'catch' + \
                                    '&'
        print('str_commands: {}'.format(str_commands))

        try:
            client_socket = socket.socket()  # instantiate
            client_socket.connect((robot_host, robot_port))  # connect to the server
            #     message = 'http://192.168.4.1/?turnx=' + str(turnx)  # take input
            client_socket.send(str_commands.encode())  # encode than send message
            #
            client_socket.close()  # close the connection
            #     # sleep(3)
            #     # time.sleep(0.02)
            #     #
            time.sleep(0.2)
            # print('headx {} '.format(turnx))
            print('sent OK {} sent'.format(str_commands))
            # send_status = 'sent ok' + str(turnx)
        except:
            print('ERR: command not sent {}'.format(str_commands))
        #     send_status += 'error sending turnx' + str(turnx)
            time.sleep(600)
