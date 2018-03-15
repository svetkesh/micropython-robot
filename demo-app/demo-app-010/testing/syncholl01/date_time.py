import time

print(time.time())
t = time.time()
time.sleep(5)
print(time.time())
print(t-time.time())