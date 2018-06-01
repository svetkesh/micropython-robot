try:
    import ure as re
except ImportError:
    try:
        import re
    except ImportError:
        print("SKIP")
        raise SystemExit

print('\n---- re.compile(".+")')

r = re.compile(".+")
m = r.match("abc")
print('m.group(0): {}'.format(m.group(0)))
try:
    m.group(1)
except IndexError:
    print("m.group(1): IndexError")

# conversion of re and match to string
print('\n---- conversion of re and match to string')
str(r)
print('str(r): {}'.format(str(r)))
str(m)
print('str(m): {}'.format(str(m)))

print('\n---- re.compile("(.+)1")')

r = re.compile("(.+)1")
m = r.match("xyz781")
print('xyz781 re (.+)1 m.group(0): {}'.format(m.group(0)))
# print('xyz781 re (.+)1 m.groups(all): {}'.format(m.groups(all)))  # added by cch
print('xyz781 re (.+)1 m.group(1): {}'.format(m.group(1)))
# print('xyz781 re (.+)1 m.groups(all): {}'.format(m.groups(all)))  # added by cch
try:
    m.group(2)
except IndexError:
    print("xyz781 re (.+)1 m.group(2): IndexError")
# print('xyz781 re (.+)1 m.groups(all): {}'.format(m.groups(all)))  # added by cch

print('\n---- re.compile("[a-cu-z]")')

r = re.compile("[a-cu-z]")
m = r.match("a")
print('r.match("a") .group(0): {}'.format(m.group(0)))
m = r.match("z")
print('r.match("z") .group(0): {}'.format(m.group(0)))
m = r.match("d")
print('r.match("d"): {}'.format(m))
m = r.match("A")
print('r.match("A"): {}'.format(m))
print("====")

print('\n---- re.compile("[^a-cu-z]")')

r = re.compile("[^a-cu-z]")
m = r.match("a")
print('r.match("a"): {}'.format(m))
m = r.match("z")
print('r.match("z"): {}'.format(m))
m = r.match("d")
print('r.match("d") .group(0): {}'.format(m.group(0)))
m = r.match("A")
print('r.match("A") .group(0): {}'.format(m.group(0)))

print('\n---- re.compile("o+")')

r = re.compile("o+")
m = r.search("foobar")
print(m.group(0))
try:
    m.group(1)
except IndexError:
    print("IndexError")

print('\n---- re.match(".*", "foo")')

m = re.match(".*", "foo")
print(m.group(0))

print('\n---- re.search("w.r", "hello world")')

m = re.search("w.r", "hello world")
print(m.group(0))

print('\n---- abc')

m = re.match('a+?', 'ab');  print(m.group(0))
m = re.match('a*?', 'ab');  print(m.group(0))
m = re.match('^ab$', 'ab'); print(m.group(0))
m = re.match('a|b', 'b');   print(m.group(0))
m = re.match('a|b|c', 'c'); print(m.group(0))

print('\n---- Case where anchors fail to match')

# Case where anchors fail to match
r = re.compile("^b|b$")
m = r.search("abc")
print('re.compile("^b|b$") .search("abc"): {}'.format(m))

print('\n---- Caught invalid regex')

try:
    re.compile("*")
except:
    print("Invalid compiled regex re.compile(\"*\") is safely caught")

print('\n---- bytes objects')

# bytes objects
m = re.match(rb'a+?', b'ab');  print(m.group(0))

print('\n---- testing against GET request')

s = "http://192.168.101.102/?headx=0.37"
r = re.compile("headx=0\.(\d+)")
m = r.search(s)
try:
    print('string: {} re: {} .\nfound: {}'.format(s, str(r), m.group(0)))
except:
    print('string: {} re: {} \n{}'.format(s, str(r), "None found"))

# added definition for headx

print('\n---- added definition for headx/handy...')
s = "http://192.168.101.102/?headx=0.37"
r_number = re.compile("0\.(\d+)")
r_headx = re.compile("headx=0\.(\d+)")
m_headx = r_headx.search(s)

try:
    print('string: {}\n    re: {}\n found: {}'.format(
        s, str(r_headx), m_headx.group(0)))
except:
    print('string: {}\n    re: {}\n found: {}'.format(
        s, str(r_headx), "None found"))

print('\n---- looking for exact headx/handy value:')

try:
    s_headx = str(m_headx.group(0))
    print('source string: {}'.format(s_headx))
    headx = r_number.search(s_headx)
    print('  value found: {}'.format(headx.group(0)))
    f_headx = float(headx.group(0))
    print('  float value: {} , value+2 = {} '.format(f_headx, f_headx+2))

except:
    print('source string: {}'.format('None found'))
    print('  value found: {}'.format('None found'))
    print('Error searching value for headx')












