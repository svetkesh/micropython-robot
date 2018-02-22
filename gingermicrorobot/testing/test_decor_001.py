#  example 1

# def f(x):
#     print('starting f()')
#
#     def g(y):
#         print('Its g() , y={},x={}'.format(y, x))
#         return y + x + 5
#
#     print('Its f with g={} ,x={}'.format(g, x))
#     return g
#
#
# # nf1 = f(1)
# nf2 = f(3)
#
# # print('nf1(1)')
# # print(nf1(1))
#
# print('nf2(11)')
# print(nf2)
# print(nf2(11))

#  example 2

# def polynomial_creator(a, b, c):
#     def polynomial(x):
#         # print(a, b, c)
#         return a * x ** 2 + b * x + c
#
#     return polynomial
#
#
# p1 = polynomial_creator(2, 3, -1)
# # p2 = polynomial_creator(-1, 2, 1)
#
# for x in range(-4, 4, 1):
#     # print(x, p1(x), p2(x))
#     print(x, p1(x))
#     print()

#  example 3

def our_decorator(func):
    def function_wrapper(x):
        print("Before calling " + func.__name__)
        func(x)
        print("After calling " + func.__name__)

    return function_wrapper


def foo(x):
    print("Hi, foo has been called with " + str(x))


print("We call foo before decoration:")
foo("Hi")

print()

print("We now decorate foo with f:")
foo = our_decorator(foo)

print()

print("We call foo after decoration:")
foo(42)