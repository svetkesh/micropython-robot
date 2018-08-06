"""
meter DC drive params for ESP 8266 firmware 1.9.3 2018.04+
"""

P_MIN = -1000
P_MAX = 1000

M_MIN = -1000
M_MAX = 1000

P_STEP = 600
M_STEP = 600

res = dict()

# for check in range(1, 4):
#     u = input('{} current U:'.format(check))
#     print('{} : {}'.format(check, u))
#     res[check] = u
#

for p in range(P_MIN, P_MAX, P_STEP):
    for m in range(M_MIN, M_MAX, M_STEP):
        pm = set()
        pm = (p, m)
        u = input('{} current U:'.format(pm))
        print('{} : {}'.format(pm, u))
        res[pm] = u

print(res)

for r in res:
    print(r, res[r])


