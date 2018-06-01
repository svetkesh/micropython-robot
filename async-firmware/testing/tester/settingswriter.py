"""
Setting writer.

Write settings into file.
Validate given data to be loaded as JSON.

j: string to be stored

valid_formatted_json=True: Attribute storing either loaded data could be 
presented as JSON 
 
file='settings.txt' File to store valid JSON data

Usage:

s = '{"ssid":"' + 'some SSID' +\
            '","wifipassword":"' + 'somepassword' +\
            '","trick":"demo"' +\
            '}'

print('--explore given string to load as JSON--')
print('DBG: s                  :{}'.format(s))
print('DBG: json.loads(s)      :{}'.format(json.loads(s)))
print('DBG: type(json.loads(s)):{}'.format(type(json.loads(s))))
for item in json.loads(s):
    print('{}:{}'.format(
        item,
        json.loads(s)[item]
    ))
print('--dumps given string--')
print('DBG: json.dumps(s)        :{}'.format(json.dumps(s)))
print('DBG: type(json.dumps(s))) :{}'.format(type(json.dumps(s))))
print('----')

sw = SettingsWriter(s)

print('DBG: sw              :{}'.format(sw))
print('DBG: sw.__dict__     :{}'.format(sw.__dict__))
print('DBG: len(sw.__dict__):{}'.format(len(sw.__dict__)))
print('DBG: len(sw.j)       :{}'.format(len(sw.j)))
print('DBG: sw.valid_formatted_json   :{}'.format(sw.valid_formatted_json))
sw.write_settings()

print('--explore string non valid to load as JSON--')

s2 = '{"ssid":"' + 'some SSID' +\
            '","wifipassword":"' + 'somepassword' +\
            '}'
sw2 = SettingsWriter(s2)
# print(sw.__dict__)

print(sw2)
print(sw2.__dict__)
print(len(sw2.__dict__))
print(len(sw2.j))
print(sw2.valid_formatted_json)
sw2.write_settings()

>>
--explore given string to load as JSON--
DBG: s                  :{"ssid":"some SSID","wifipassword":"somepassword","trick":"demo"}
DBG: json.loads(s)      :{'ssid': 'some SSID', 'trick': 'demo', 'wifipassword': 'somepassword'}
DBG: type(json.loads(s)):<class 'dict'>
ssid:some SSID
trick:demo
wifipassword:somepassword
--dumps given string--
DBG: json.dumps(s)        :"{\"ssid\":\"some SSID\",\"wifipassword\":\"somepassword\",\"trick\":\"demo\"}"
DBG: type(json.dumps(s))) :<class 'str'>
----
DBG: json items: ssid:some SSID
DBG: json items: trick:demo
DBG: json items: wifipassword:somepassword
DBG: JSON data loaded OK
DBG: sw              :<__main__.SettingsWriter object at 0x7ff4d0882c88>
DBG: sw.__dict__     :{'j': {'ssid': 'some SSID', 'trick': 'demo', 'wifipassword': 'somepassword'}, 'valid_formatted_json': True, 'file': 'settings.txt'}
DBG: len(sw.__dict__):3
DBG: len(sw.j)       :3
DBG: sw.valid_formatted_json   :True
--explore string non valid to load as JSON--
<class 'json.decoder.JSONDecodeError'> Unterminated string starting at: line 1 column 36 (char 35)
ERR: given data could not be loaded as JSON:{"ssid":"some SSID","wifipassword":"somepassword}
<__main__.SettingsWriter object at 0x7ff4cf224278>
{'j': '', 'valid_formatted_json': False, 'file': 'settings.txt'}
3
0
False
ERR: given data could not be written as JSON

Process finished with exit code 0
    
"""

# try:
#     with open('settings.txt', 'w') as f:
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


class SettingsWriter:
    """
    Write settings into file.
    Validate given data to be loaded as JSON.
    
    j: string to be stored
    
    valid_formatted_json=True: Attribute storing either loaded data could be 
    presented as JSON 
     
    file='settings.txt' File to store valid JSON data
    """
    def __init__(self, j, file='settings.txt', valid_formatted_json=True):
        self.file = file
        self.j_str = j
        try:
            self.j = json.loads(j)
            for item in self.j:
                print('DBG: json items: {}:{}'.format(
                    item,
                    self.j[item]
                ))
            self.valid_formatted_json = True
            print('DBG: JSON data loaded OK')
        except json.JSONDecodeError as e:
            print(type(e), e)
            print('ERR: given data could not be loaded as JSON:{}'.format(j))

            # tolerant variant to handle
            # JSON loading errors:
            self.j = ''

            self.valid_formatted_json = False

            # non-# tolerant variant to handle JSON:
            # raise ValueError('ERR: given data'
            #                  ' could not be loaded'
            #                  ' as JSON: {}'.format(j))

            # to raise exception and obtain
            # detailed explanation for
            # exact root for error
            # uncomment "raise" and
            # you can get something like:
            # ...
            # json.decoder.JSONDecodeError:
            #   Unterminated string starting at:
            #   line 1 column 36 (char 35)
            # ...
            # ValueError: ERR: given data
            #   could not be loaded as JSON:
            #   {"ssid":"some SSID","wifipassword":"somepassword}

    def write_settings(self):
        if self.valid_formatted_json:
            try:
                with open(self.file, 'w') as f:
                    print('DBG: 186 j         :{}'.format(str(self.j)))
                    print('DBG: 187 self.j_str:{}'.format(str(self.j_str)))
                    # f.write(str(self.j))
                    f.write(str(self.j_str))
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
    # pass

    s = '{"ssid":"some SSID' + \
        '","wifipassword":' + '"otherpassword' + \
        '","trick":"demo"' + \
        '}'

    print('--explore given string to load as JSON--')
    print('DBG: s                  :{}'.format(s))
    print('DBG: json.loads(s)      :{}'.format(json.loads(s)))
    print('DBG: type(json.loads(s)):{}'.format(type(json.loads(s))))
    for item in json.loads(s):
        print('{}:{}'.format(
            item,
            json.loads(s)[item]
        ))
    print('--dumps given string--')
    print('DBG: json.dumps(s)        :{}'.format(json.dumps(s)))
    print('DBG: type(json.dumps(s))) :{}'.format(type(json.dumps(s))))
    print('----')

    sw = SettingsWriter(s)

    print('DBG: sw              :{}'.format(sw))
    print('DBG: sw.__dict__     :{}'.format(sw.__dict__))
    print('DBG: len(sw.__dict__):{}'.format(len(sw.__dict__)))
    print('DBG: len(sw.j)       :{}'.format(len(sw.j)))
    print('DBG: sw.valid_formatted_json   :{}'.format(sw.valid_formatted_json))
    sw.write_settings()


if __name__ == '__main__':
    main()
