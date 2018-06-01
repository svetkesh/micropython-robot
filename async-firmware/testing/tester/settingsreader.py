"""
Read settings from file and retuns dictionary for good-formatted file.
    Else returns False

--
Good-formatted file:
{"ssid":"some SSID","wifipassword":"otherpassword","trick":"demo"}

Bad formatted file examples:

text before "{" :
someextrawaste{"ssid":"some SSID","wifipassword":"otherpassword","trick":"demo"}

used ' instead "
{'ssi':'some SSID','wifipassword':'otherpassword','trick':'demo'}

spaces before
{ "ssid" : "some SSID" , "wifipassword" : "otherpassword" , "trick" : "demo" }


"""

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
    """
    Read file and returns dictionare of "settings"
    Default file for reading settings is
    file='settings.txt'
    some_settings_reader_object = SettingsReader(file='settings.txt')

    Usage:

print('--start demo--')
print('--assign ang get repr()--')
sr4 = SettingsReader(file='settings.txt')
print('DBG sr4: type: {},\nsr4: {}'.format(type(sr4), sr4))
print('DBG is valid_formatted_json: {}'.format(sr4.valid_formatted_json))

print('--read and load--')
j = sr4.read_settings()
print('DBG j {} {} , \nif j: {}'.format(type(j), j,
                                        True if j else False))

print('--iterate dictionary--')
if j:
    print('j: {} , {}'.format(type(j), j))
    for item in j:
        print('j-key: {}, j-value: {}'.format(item, j[item]))
else:
    print('ERR iterate settings')

print('--access elements--')# staright compare to existent object
if j:
    print(j['trick'])
else:
    print('ERR could nod read value for j[\'trick\']')

print('--safe access to value--')
try:
    print(j['ssid'])
except Exception as e:
    print('ERR could nod read value for j[\'ssid\'] {}, {}'.format(type(e), e))

print('--access to non-existent value--')
try:
    print(j['non-existent'])
except Exception as e:
    print('ERR could not get value for non-existent key: {}, {}'.format(type(e), e))

print('--end demo--')
>>

# for file settings.txt
# {"ssid":"some SSID","wifipassword":"otherpassword","trick":"demo"}

--start demo--
--assign ang get repr()--
DBG sr4: type: <class '__main__.SettingsReader'>,
sr4: id: 139621927291648, Settings from: settings.txt: \
 {'wifipassword': 'otherpassword', 'trick': 'demo', 'ssid': 'some SSID'}
DBG is valid_formatted_json: True
--read and load--
DBG j <class 'dict'> {'wifipassword': 'otherpassword', 'trick': 'demo', 'ssid': 'some SSID'} ,
if j: True
--iterate dictionary--
j: <class 'dict'> , {'wifipassword': 'otherpassword', 'trick': 'demo', 'ssid': 'some SSID'}
j-key: wifipassword, j-value: otherpassword
j-key: trick, j-value: demo
j-key: ssid, j-value: some SSID
--access elements--
demo
--safe access to value--
some SSID
--access to non-existent value--
ERR could not get value for non-existent key: <class 'KeyError'>, 'non-existent'
--end demo--

Process finished with exit code 0

# for file settings.txt
# sometext{"ssid":"some SSID","wifipassword":"otherpassword","trick":"demo"}

--start demo--
--assign ang get repr()--
ERR loading settings from file: settings.txt, json.load(f) <class 'json.decoder.JSONDecodeError'>,\
 Expecting value: line 1 column 1 (char 0)
DBG sr4: type: <class '__main__.SettingsReader'>,
sr4: id: 140407360031488, Settings from: settings.txt: False
DBG is valid_formatted_json: True
--read and load--
ERR loading settings from file: settings.txt, json.load(f) <class 'json.decoder.JSONDecodeError'>,\
 Expecting value: line 1 column 1 (char 0)
DBG j <class 'bool'> False ,
if j: False
--iterate dictionary--
ERR iterate settings
--access elements--
ERR could nod read value for j['trick']
--safe access to value--
ERR could nod read value for j['ssid'] <class 'TypeError'>, 'bool' object is not subscriptable
--access to non-existent value--
ERR could not get value for non-existent key: <class 'TypeError'>, 'bool' object is not subscriptable
--end demo--

Process finished with exit code 0

    """

    def __init__(self, file='settings.txt', valid_formatted_json=True, *args, **kwargs):
        self.file = file
        self.valid_formatted_json = valid_formatted_json
        # print(args)
        for args in args:
            # print(args)
            self.args = args

        # # for key, value in args.items():
        # print('DBG: args:{}, type(args):{}'.format(args, type(args)))

        # print(kwargs)
        # for kwargs in kwargs:
        #     print('DBG: kwargs:{}, '.format(kwargs))
        #     self.kwargs = kwargs
        for key, value in kwargs.items():
            # print('DBG: kwargs:{}, kwargs.items():{}, key: {}, value: {}'.format(kwargs, kwargs.items(), key, value))
            setattr(self, key, value)

    def read_settings(self):
        try:
            # print('DBG: self.file:{}'.format(self.file))
            with open(self.file, 'r') as f:
                # print('DBG file content: {}'.format(f.read()))
                try:
                    j = json.load(f)
                    # print('DBG: j = json.load(f): {}, {}'.format(type(j), str(j)))
                    # for key in j:
                    #     print('DBG: key:value of j: {}:{}'.format(key, j[key]))
                except Exception as e:
                    print('ERR loading settings from file: {}, j'
                          'son.load(f) {}, {}'.format(self.file, type(e), e))
                    return False
                return j

        except Exception as e:
            print('ERR reading file {}, {}'.format(type(e), e))
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

    def __repr__(self):
        return 'id: {}, Settings from: {}: {}'.format(id(self), self.file, self.read_settings())

    def read_value(self, key):
        try:
            if self.valid_formatted_json:
                values = self.read_settings()
                return values[key]

        except Exception as e:
            print('ERR {}, {}\nreading value from {} for {}'.format(type(e), e, self.file, key))
            self.valid_formatted_json = False
            return False


# # # examples of usage
# print('--start demo--')
# print('--assign ang get repr()--')
# sr4 = SettingsReader(file='settings.txt')
# print('DBG sr4: type: {},\nsr4: {}'.format(type(sr4), sr4))
# print('DBG is valid_formatted_json: {}'.format(sr4.valid_formatted_json))
#
# print('--read and load--')
# j = sr4.read_settings()
# print('DBG j {} {} , \nif j: {}'.format(type(j), j,
#                                         True if j else False))
#
# print('--iterate dictionary--')
# if j:
#     print('j: {} , {}'.format(type(j), j))
#     for item in j:
#         print('j-key: {}, j-value: {}'.format(item, j[item]))
# else:
#     print('ERR iterate settings')
#
# print('--access elements--')# staright compare to existent object
# if j:
#     print(j['trick'])
# else:
#     print('ERR could nod read value for j[\'trick\']')
#
# print('--safe access to value--')
# try:
#     print(j['ssid'])
# except Exception as e:
#     print('ERR could nod read value for j[\'ssid\'] {}, {}'.format(type(e), e))
#
# print('--access to non-existent value--')
# try:
#     print(j['non-existent'])
# except Exception as e:
#     print('ERR could not get value for non-existent key: {}, {}'.format(type(e), e))
#
# print('--end demo--')

