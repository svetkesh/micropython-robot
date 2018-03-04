import json

s = '{"ssid":"some SSID","wifipassword":"somepassword","trick":"demo"}'
print(type(s), s)

j0 = json.loads(s)
print(type(j0), j0, j0['ssid'], j0['wifipassword'])

d0 = json.dumps(j0)
print(type(d0), d0)

j = json.loads(d0)
print(type(j), j, j['ssid'], j['wifipassword'])

# ----

print('--s2--')
ssid = "some SSID"
wifipassword = "somePassword"
trick = "demo"

s2 = {
    'ssid': ssid,
    'wifipassword': wifipassword,
    'trick': trick
}

print(type(s2), s2)

d2 = json.dumps(s2)
print(type(d2), d2)

j2 = json.loads(d2)
print(type(j2), j2)

# ---- dumps(**kwargs), loads(args) ----
print('--j_defs--')


def j_dumps(**kwargs):
    return json.dumps(kwargs)

# err with *args :
# def j_loads_args(*args):    # TypeError: the JSON object must be str, bytes or bytearray, not 'tuple'
#     return json.loads(args) # ... for any string


def j_loads(args):
    return json.loads(args)

# ----
print('--j_dumps , dumping to string--')

print(j_dumps(ssid="some SSID",
              wifipassword="somepassword",
              trick="demo",
              ))

print('chars0-4: {}', format(
    j_dumps(ssid="some SSID",
            wifipassword="somepassword",
            trick="demo",
            )[0:5]))

# ----
print('--j_loads , load to json --')

print(j_loads('{"ssid": "some SSID", "wifipassword": "somepassword", "trick": "demo"}'))  # err
# # TypeError: the JSON object must be str, bytes or bytearray, not 'tuple'

# print('\"')
# print(j_loads("{'ssid': 'some SSID', 'wifipassword': 'somepassword', 'trick': 'demo'}")) # err
# # json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

print('value for key \"ssid\":{}'.
      format(j_loads('{'
                     '"ssid": "some SSID", '
                     '"wifipassword": "somepassword", '
                     '"trick": "demo"'
                     '}')["ssid"]))


print('--s3--')
              
s3 = '{"ssid": "some SSID", "wifipassword": "somepassword", "trick": "demo"}'
print(j_loads(s3))

# ----
print('--dump and load json-file--')
print('--dump json to file--')


def dump_dict_to_file(file_name='exch.txt', **kwargs):
    with open(file_name, 'w') as f:
        json.dump(kwargs, f)

dump_dict_to_file(ssid="new SSID",
                  wifipassword="newpassword",
                  trick="newdemo",
                  )

print('--loading file into JSON--')


def loads_file_to_dict(file_name='exch.txt'):
    with open(file_name, 'r') as f:
        return json.load(f)

print(loads_file_to_dict())
print(loads_file_to_dict()['trick'])

print('--dump text formatted like json to file--')


def dump_formatted_json_text_to_file(txt, file_name='exch.txt'):
    j = json.loads(txt)
    print(type(j), j)
    with open(file_name, 'w') as f:
        json.dump(j, f)


j_f_text = '{"ssid":"super text SSID","wifipassword":"superTEXTpassword","trick":"TEXT-demo-trick"}'
# test dump text formatted like json to file

dump_formatted_json_text_to_file(j_f_text)
print('type :{}\nJSON :{}\ntrick:{}'.format(type(loads_file_to_dict()),
                          loads_file_to_dict(),
                          loads_file_to_dict()['trick']))

print('--end of tricks--')

