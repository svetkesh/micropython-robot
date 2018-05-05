# import uasyncio as asyncio
#
# @asyncio.coroutine
# def serve(reader, writer):
#     print(reader, writer)
#     print("================")
#     print((yield from reader.read()))
#     yield from writer.awrite("HTTP/1.0 200 OK\r\n\r\nHello.\r\n")
#     print("After response write")
#     yield from writer.aclose()
#     print("Finished processing request")
#
#
# import logging
# logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
# print('starting loop')
# loop = asyncio.get_event_loop()
# loop.call_soon(asyncio.start_server(serve, "127.0.0.1", 8081))
# loop.run_forever()
# loop.close()

#!/usr/bin/env micropython

import uasyncio as asyncio


def _handler(reader, writer):
    print('New connection')
    line = yield from reader.readline()
    print(line)
    yield from writer.awrite('Gotcha!')
    yield from writer.aclose()


# def run(host="127.0.0.1", port=8081, loop_forever=True, backlog=16): # orig
def run(host="192.168.4.1", port=8081, loop_forever=True, backlog=16):
    loop = asyncio.get_event_loop()
    print("* Starting Server at {}:{}".format(host, port))
    loop.create_task(asyncio.start_server(_handler, host, port, backlog=backlog))
    if loop_forever:
        loop.run_forever()
        loop.close()


if __name__ == '__main__':
    run()