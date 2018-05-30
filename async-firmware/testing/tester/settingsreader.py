import sys
import os

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


class SettingsReader:
    # try:
    #     with open('settings.txt', 'r') as f:
    #         j = json.load(f)
    #         # print(f.read())
    #         print(j)
    #         print(j['ssid'])
    #         print(j['wifipassword'])
    #         print(j['trick'])
    # except:
    #     print('ERR reading file')
    #
    def __init__(self, file='settings.txt', valid_formatted_json=True, *args, **kwargs):
        self.file = file
        self.valid_formatted_json = valid_formatted_json
        print(args)
        for args in args:
            print(args)
            self.args = args

        # for key, value in args.items():
        print('DBG: args:{}, type(args):{}'.format(args, type(args)))

        print(kwargs)
        # for kwargs in kwargs:
        #     print('DBG: kwargs:{}, '.format(kwargs))
        #     self.kwargs = kwargs
        for key, value in kwargs.items():
            print('DBG: kwargs:{}, kwargs.items():{}, key: {}, value: {}'.format(kwargs, kwargs.items(), key, value))
            setattr(self, key, value)

    def read_settings(self):
        print('DBG SettingsReader.read_settings() running')
        try:
            print('DBG: self.file:{}'.format(self.file))
            # with open(self.file, 'r') as f:
            with open(self.file, 'r') as f:
                print('DBG: self.file:{}'.format(self.file))
                print('DBG: f.read() :{}'.format(f.read()))
                try:
                    j = json.load(f)
                except:
                    print('ERR j = json.load(f)')
                # print(f.read())
                print(j)
                # print(j['ssid'])
                # print(j['wifipassword'])
                # print(j['trick'])

                return j
        except:
            print('ERR reading file')
            self.valid_formatted_json = False
            return False

    def rs(self):
        print('DBG SettingsReader.rs() running')
        # f = open(self.file)
        print(os.getcwd())
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in '%s': %s" % (cwd, files))
        f = open(self.file, 'r')
        rf = f.read()
        print(rf)
        f.close()

    def ls(self):
        print('DBG SettingsReader.ls() running')
        # f = open(self.file)
        print(os.getcwd())
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in '%s': %s" % (cwd, files))
        f = open(self.file, 'r')
        print(f)
        ls = json.load(f)
        # ls = json.loads(f)
        print('DBG: ls:'.format(ls))
        # print(ls[1])
        print('DBG: ls[\'ssid\']:'.format(ls['ssid']))
        f.close()
        # for item in ls:
        #     print(item)


# # sr = SettingsReader('foo', 'setting a', 13)
# sr = SettingsReader('foo', 'setting a', 13) #
# # sr = SettingsReader('foo', 'setting a', 13, file='some_file') # TypeError:
# #  __init__() got multiple values for argument 'file'
#
# print(sr.__dir__())
# print(dir(sr))
# print(sr.file)

# sr2 = SettingsReader()
# j = sr2.read_settings()
# print('DBG: {}, {}'.format(type(j), j))

# sr3 = SettingsReader(file='data.txt')
# j = sr3.read_settings()
# print(j)
# print('----')
# sr3.rs()

sr4 = SettingsReader(file='settings.txt')
j = sr4.read_settings()
print('----')
print('j: {}'.format(j))
# print('----')
# sr4.rs()
# print('----')
sr4.ls()
print('----')
sr4.read_settings()
