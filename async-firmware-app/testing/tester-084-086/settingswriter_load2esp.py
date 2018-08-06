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

    Setting writer.

    Write settings into file.
    Validate given data to be loaded as JSON.

    j: string to be stored

    valid_formatted_json=True: Attribute storing either loaded data could be
    presented as JSON

    file='settings.txt' File to store valid JSON data

    Short ver for ESP

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

    def write_settings(self):
        if self.valid_formatted_json:
            try:
                with open(self.file, 'w') as f:
                    print('DBG: 186 j         :{}'.format(str(self.j)))
                    print('DBG: 187 self.j_str:{}'.format(str(self.j_str)))
                    # f.write(str(self.j))
                    f.write(str(self.j_str))
                return True
            except Exception as e:
                print('DBG error saving settings {}, {}'.format(type(e), e))
                return False
        else:
            print('ERR: given data could not be written as JSON')

