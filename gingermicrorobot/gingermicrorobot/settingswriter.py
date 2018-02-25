# try:
#     with open('config.txt', 'w') as f:
#         f.write('{"ssid":"' + ssid +
#                 '","wifipassword":"' + wifipassword +
#                 '","trick":"demo"' +
#                 '}')
# except:
#     print('DBG error saving settings')
#
import sys

try:
    import ure as re
except ImportError:
    try:
        import re
    except ImportError:
        raise SystemExit

try:
    import utime as time
except ImportError:
    try:
        import time
    except ImportError:
        raise SystemExit

try:
    import ujson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise SystemExit


class SettingsWriter():
    def __init__(self, j, file='settings.txt', valid_json=True):
        # self.j = j
        # print(self.j)
        # for item in json.loads(j):
        #     print('--{}:{}--'.format(
        #         item,
        #         json.loads(j)[item]
        #     ))
        self.file = file
        try:
            self.j = json.loads(j)
            for item in self.j:
                print('DBG: json items: {}:{}'.format(
                    item,
                    self.j[item]
                ))
            self.valid_json =True
            print('DBG: JSON data loaded OK')
        except json.JSONDecodeError as e:
            print(type(e), e)
            # raise SystemExit
            self.j = ''
            self.valid_json=False
            # raise ValueError('ERR: given data could not be loaded as JSON: {}'.format(j))
            print('ERR: given data could not be loaded as JSON: {}'.format(j))

    def write_settings(self):
        if self.valid_json:
            try:
                with open(self.file, 'w') as f:
                    f.write(str(self.j))
                return True
            except:
                print('DBG error saving settings')
                return False
        else:
            print('ERR: given data could not be written as JSON')

    # def __init__(self, *args):
        # for args in args:
        #     print('DBG: args:{}'.format(args))
        #     print('DBG: len(args):{} , type(args): {}'.format(
        #         len(args),
        #         type(args)
        #     ))
        # try:
        #     jarg = json.load(*args)
        #     print('jarg: {} : {}'.format(
        #         type(jarg),
        #         jarg
        #     ))
        # except Exception as e:
        #     print('ERR: {} not json type {}'.format(
        #         type(args),
        #         *args
        #     ))

def main():
    s = '{"ssid":"' + 'some SSID' +\
                '","wifipassword":"' + 'somepassword' +\
                '","trick":"demo"' +\
                '}'
    sw = SettingsWriter(s)
    # print(sw.__dict__)

    print(sw)
    print(sw.__dict__)
    print(len(sw.__dict__))
    print(len(sw.j))
    print(sw.valid_json)
    sw.write_settings()


    # print('----')
    # print(s)
    # print(json.loads(s))
    # print(type(json.loads(s)))
    # for item in json.loads(s):
    #     print('{}:{}'.format(
    #         item,
    #         json.loads(s)[item]
    #     ))
    # print('----')
    # print(json.dumps(s))
    # print(type(json.dumps(s)))
    # print('----')

    print('----')

    s2 = '{"ssid":"' + 'some SSID' +\
                '","wifipassword":"' + 'somepassword' +\
                '}'
    sw2 = SettingsWriter(s2)
    # print(sw.__dict__)

    print(sw2)
    print(sw2.__dict__)
    print(len(sw2.__dict__))
    print(len(sw2.j))
    print(sw2.valid_json)
    sw2.write_settings()

if __name__ == '__main__':
    main()