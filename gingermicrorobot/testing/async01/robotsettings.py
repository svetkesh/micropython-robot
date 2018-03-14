"""
Robot settings reader, and writer, and updater.

Usage:

print(rs)
print(rs.settings)

rs.settings = some_string
print(rs)
print(rs.settings)

rs.settings = some_dict
print(rs)
print(rs.settings)
print(rs.settings['trick'])

rs.settings['trick'] = 'Super Trick'
print(rs)
print(rs.settings)
print(rs.settings['trick'])

new_dict = {
    'ssid': ssid,
    'wifipassword': wifipassword,
    'trick': trick,
}

print(new_dict)
new_dict['trick'] = 'Mind Blow'
print(new_dict)

rs.settings = new_dict

>>
<__main__.RobotSettings object at 0x7f4f07240e10>
<class 'dict'>
DBG: settings.setter running
DBG: writing file
<__main__.RobotSettings object at 0x7f4f07240e10>
no tricks here
DBG: settings.setter running
DBG: writing file
<__main__.RobotSettings object at 0x7f4f07240e10>
{'wifipassword': 'somePassword', 'trick': 'demo', 'ssid': 'some SSID'}
demo
<__main__.RobotSettings object at 0x7f4f07240e10>
{'wifipassword': 'somePassword', 'trick': 'Super Trick', 'ssid': 'some SSID'}
Super Trick
{'wifipassword': 'somePassword', 'trick': 'demo', 'ssid': 'some SSID'}
{'wifipassword': 'somePassword', 'trick': 'Mind Blow', 'ssid': 'some SSID'}
DBG: settings.setter running
DBG: writing file

somefile.txt contens>>
{"wifipassword": "somePassword", "trick": "Mind Blow", "ssid": "some SSID"}
"""
import asyncio

class RobotSettings:
    """
    Read and write settings from file.
    """

    def __init__(self, settings, filename='settings.txt'):
        self.filename = filename
        self._settings = settings

    # def readsettings(self):
    #     pass
    #
    # def writesettings(self):
    #     pass

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        print('DBG: settings.setter running')
        try:
            import ujson as json
        except ImportError:
            try:
                import json
            except ImportError:
                raise SystemExit
        # “Ask forgiveness not permission”
        try:
            with open(self.filename, 'w') as f:
                json.dump(value, f)
                print('DBG: writing file')
        except Exception as e:
            print(type(e), e)
            print('DBG: nothing to write into file')

        self._settings = value


# ssid = "some SSID"
# wifipassword = "somePassword"
# trick = "demo"
#
# some_dict = {
#     'ssid': ssid,
#     'wifipassword': wifipassword,
#     'trick': trick
# }
#
# some_string = 'no tricks here'
#
# rs = RobotSettings(
#     filename='somefile.txt',
#     settings=dict
# )
#
# print(rs)
# print(rs.settings)
#
# rs.settings = some_string
# print(rs)
# print(rs.settings)
#
# rs.settings = some_dict
# print(rs)
# print(rs.settings)
# print(rs.settings['trick'])
#
# rs.settings['trick'] = 'Super Trick'
# print(rs)
# print(rs.settings)
# print(rs.settings['trick'])
#
# new_dict = {
#     'ssid': ssid,
#     'wifipassword': wifipassword,
#     'trick': trick,
# }
#
# print(new_dict)
# new_dict['trick'] = 'Mind Blow'
# print(new_dict)
#
# rs.settings = new_dict

# async test ----
ssid = "some SSID"
wifipassword = "somePassword"
trick = "demo"

c = {
    'ssid': ssid,
    'wifipassword': wifipassword,
    'trick': trick
}

some_string = 'no tricks here'

rs = RobotSettings(
    filename='somefile.txt',
    settings=c              # settings are not saved into file
)

rs.settings = c           # settings are SAVED into file
print(rs)
print(rs.settings)
print(rs.settings['trick'])

print(asyncio.iscoroutine(rs))

# http://stackabuse.com/python-async-await-tutorial/
# https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md


