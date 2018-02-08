'''

# DBG: r_wifipassword NOT found
# b'GET /favicon.ico HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36\r\nAccept: image/webp,image/apng,image/*,*/*;q=0.8\r\nReferer: http://192.168.4.1/?nextssid=xx&nextwifipassword=yy&nextrunmode=zz\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9,ru;q=0.8,uk;q=0.7\r\n\r\n'


# some_string = "b'GET /favicon.ico HTTP/1.1" \
#               "\r\nHost: 192.168.4.1" \
#               "\r\nConnection: keep-alive" \
#               "\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36" \
#               "\r\nAccept: image/webp,image/apng,image/*,*/*;q=0.8" \
#               "\r\nReferer: http://192.168.4.1/?nextssid=xx&nextwifipassword=yy&nextrunmode=zz" \
#               "\r\nAccept-Encoding: gzip, deflate" \
#               "\r\nAccept-Language: en-US,en;q=0.9,ru;q=0.8,uk;q=0.7" \
#               "\r\n" \
#               "\r\n'"
# "

'''

import re
# import ujson
import json

# other_string = "Referer: http://192.168.4.1/?nextssid=xx&nextwifipassword=yy&nextrunmode=zz"
#
# # comile settings
# # re compile alfa-numeric string
# r_alfanum = re.compile("\.(\w+)")
# # nextssid
# r_ssid = re.compile("nextssid=\.(\w+)")
# # nextwifipassword
# r_wifipassword = re.compile("nextwifipassword=\.(\w+)")
# # nextrunmode
# r_runmode = re.compile("nextrunmode=\.(\w+)")
#
# print(other_string)
# print(r_wifipassword)
# print(r_ssid.search(other_string))

import re
# request = "http://192.168.4.1/?nextssid=xx&nextwifipassword=yy&nextrunmode=zz"
# # >>>
# r_nextssid = re.compile("nextssid=(\w+)")
# # >>>
# print(r_nextssid)
# re.compile('nextssid=(\\w+)')
# # >>>
# print(r_nextssid.search(request))
# # <_sre.SRE_Match object; span=(20, 31), match='nextssid=xx'>
# # >>>
# nextssid = r_nextssid.search(request).groups(0)
#
# print(nextssid)
# # ('xx',)
# print(type(nextssid))
# # <class 'tuple'>
#
# print(len(nextssid))
# # 1
# print(nextssid[0])

# --

request = "http://192.168.4.1/?nextssid=Me x and y #123&nextwifipassword=yy&nextrunmode=zz"
# request = b'GET /?nextssid=xx&nextwifipassword=yy&nextrunmode=zz HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9,ru;q=0.8,uk;q=0.7\r\n\r\n'
# request = request.decode("utf-8")

# request = "b'GET /favicon.ico HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36\r\nAccept: image/webp,image/apng,image/*,*/*;q=0.8\r\nReferer: http://192.168.4.1/?nextssid=xx&nextwifipassword=yy&nextrunmode=zz\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9,ru;q=0.8,uk;q=0.7\r\n\r\n' \
# "
#
# r_nextssid = re.compile('nextssid=(\\w+)')
r_nextssid = re.compile('nextssid=([a-zA-Z0-9_\s\@\!\@\#\%\*\-]+)')
print(r_nextssid.search(request))
print(r_nextssid.search(request) is not None)

nextssid = r_nextssid.search(request).groups(0)
print(nextssid[0])

ssid = r_nextssid.search(request).group(1)

try:
    with open('config.txt', 'w') as f:
        f.write('{"ssid":"' + ssid +
                # '","ssidpss":"' + wifipassword.group(0)+
                '","trick":"demo"' +
                '}')
except:
    print('DBG error saving settings')

# read JSON
try:
    with open('config.txt', 'r') as f:
        j = json.load(f)
        # print(f.read())
        print(j)
        print(j['ssid'])
        print(j['trick'])
except:
    print('ERR reading file')


