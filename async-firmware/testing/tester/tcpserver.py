# #asyncio_echo_server_coroutine.py
# # https://pymotw.com/3/asyncio/io_coroutine.html#echo-server
#
# import uasyncio
# # import logging
# import sys
#
# # SERVER_ADDRESS = ('localhost', 10000)
# SERVER_ADDRESS = ('192.168.4.1', 8080)
# # logging.basicConfig(
# #     level=logging.DEBUG,
# #     format='%(name)s: %(message)s',
# #     stream=sys.stderr,
# # )
# # # log = logging.getLogger('main')
#
# event_loop = uasyncio.get_event_loop()
#
# async def echo(reader, writer):
#     address = writer.get_extra_info('peername')
#     # log = logging.getLogger('echo_{}_{}'.format(*address))
#     print(('echo_{}_{}'.format(*address)))
#     # log.debug('connection accepted')
#     print('connection accepted')
#
#     while True:
#         data = await reader.read(128)
#
#         if data:
#             print(('received {!r}'.format(data)))
#             writer.write(data)
#             await writer.drain()
#             # log.debug('sent {!r}'.format(data))
#             print(('sent {!r}'.format(data)))
#
#         else:
#             # log.debug('closing')
#             print('closing')
#             writer.close()
#             return
#
# # Create the server and let the loop finish the coroutine before
# # starting the real event loop.
# factory = uasyncio.start_server(echo, *SERVER_ADDRESS)
# server = event_loop.run_until_complete(factory)
# # log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))
# print(('starting up on {} port {}'.format(*SERVER_ADDRESS)))
#
# try:
#     event_loop.run_forever()
# except KeyboardInterrupt:
#     pass
# finally:
#     # log.debug('closing server')
#     print('closing server')
#     server.close()
#     event_loop.run_until_complete(server.wait_closed())
#     # log.debug('closing event loop')
#     print('closing event loop')
#     event_loop.close()
#
#
# # >>>
# # >>> import main
# # echo_192.168.4.2_42564
# # connection accepted
# # received b'GET / HTTP/1.1\r\nHost: 192.168.4.1:8080\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (X11; Linu'
# # Traceback (most recent call last):
# #   File "<stdin>", line 1, in <module>
# #   File "main.py", line 45, in <module>
# #   File "uasyncio/core.py", line 180, in run_until_complete
# #   File "uasyncio/core.py", line 154, in run_forever
# #   File "uasyncio/core.py", line 109, in run_forever
# #   File "main.py", line 31, in echo
# # AttributeError: 'StreamWriter' object has no attribute 'write'


import uasyncio as asyncio

@asyncio.coroutine
def serve(reader, writer):
    print(reader, writer)
    print("================")
    # print((yield from reader.read()))  # orig
    # print((yield from reader.read()))  # mod readline
    # line = yield from reader.readline()
    line = yield from reader.read()
    print('DBG line: {}, {}'.format(type(line), str(line)))  # mod readline
    yield from writer.awrite("HTTP/1.0 200 OK\r\n\r\nHello.\r\n")
    print("After response write")
    yield from writer.aclose()
    print("Finished processing request")


# import logging
#logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
loop = asyncio.get_event_loop()
# loop.call_soon(asyncio.start_server(serve, "127.0.0.1", 8081))
loop.call_soon(asyncio.start_server(serve, "192.168.4.1", 80))
loop.run_forever()
loop.close()

