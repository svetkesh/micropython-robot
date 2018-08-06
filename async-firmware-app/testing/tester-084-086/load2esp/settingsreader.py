"""
Read settings from file and retuns dictionary for good-formatted file.
Return value for key for setting from given good-formatted file.
Else returns False.

Short ver for loading to ESP.
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
    Read settings from file and retuns dictionary for good-formatted file.
    Return value for key for setting from given good-formatted file.
    Else returns False.

    Short ver for loading to ESP.

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



