# -1.0 ... 1.0

# f_headx = -0.999
#
# while f_headx < 1:
#
#     # posx = ((int(f_headx) + 1) / 200) * (110 - 70)
#     # posx = ((f_headx + 1) / 200) * (70)
#     # posx = ((f_headx + 1) / 200) * (70)
#     # posx = ((f_headx + 1)/2)# * (70)  # norm
#     posx = int(((f_headx + 1)/2) * 110 + 30)  # norm
#
#     print('{:.3} : {}'.format(f_headx, posx))
#
#     #
#     f_headx += 0.09
#


# 0.0 ... 1.0
f_headx = 0.009

while f_headx < 1:

    # posx = ((int(f_headx) + 1) / 200) * (110 - 70)
    # posx = ((f_headx + 1) / 200) * (70)
    # posx = ((f_headx + 1) / 200) * (70)
    # posx = ((f_headx + 1)/2)# * (70)  # norm
    posx = int(f_headx  * 75 + 40)         # norm 40..115

    print('{:.3} : {}'.format(f_headx, posx))

    #
    f_headx += 0.09
