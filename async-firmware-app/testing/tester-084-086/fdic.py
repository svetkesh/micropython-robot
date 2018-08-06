import string


def function1():
    print("called function 1")


def function2():
    print("called function 2")


def function3():
    print("called function 3")


def function1x(key):
    print("called function 1x for {}".format(key))


def function2x(key):
    print("called function 2x for {}".format(key))


def function3x(key):
    print("called function 3x for {}".format(key))


tokenDict = {"cat": function1, "dog": function2, "bear": function3}

tokenDictx = {"cat": function1x, "dog": function2x, "bear": function3x}

# simulate, say, lines read from a file
lines = ["cat", "bear", "cat", "dog"]

for line in lines:
    # lookup the function to call for each line
    functionToCall = tokenDict[line]

    # and call it
    functionToCall()

print("----")

for line in lines:
    # lookup the function to call for each line
    functionToCall = tokenDictx[line]

    # and call it
    functionToCall(line)


