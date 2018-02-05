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

other_string = "Referer: http://192.168.4.1/?nextssid=xx&nextwifipassword=yy&nextrunmode=zz"

# comile settings
# re compile alfa-numeric string
r_alfanum = re.compile("\.(\w+)")
# nextssid
r_ssid = re.compile("nextssid=\.(\w+)")
# nextwifipassword
r_wifipassword = re.compile("nextwifipassword=\.(\w+)")
# nextrunmode
r_runmode = re.compile("nextrunmode=\.(\w+)")

print(other_string)
print(r_wifipassword)
print(r_ssid.search(other_string))
