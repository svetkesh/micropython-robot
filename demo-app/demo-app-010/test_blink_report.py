import time

SHORT_SLEEP = 1.2
BLINK_SLEEP = 0.5

def blink_report(n_blinks):
    # networkpin.off()
    print('booooom')
    time.sleep(SHORT_SLEEP*2)
    for blinks in range (n_blinks):
        # networkpin.on()
        time.sleep(BLINK_SLEEP)
        # networkpin.off()
        print('blinks {}'.format(blinks))


def blink_twice(n_blinks, repeat_reports = 2):
    def blink_report(n_blinks):
        # networkpin.off()
        print('booooom')
        time.sleep(SHORT_SLEEP * 2)
        for blinks in range(n_blinks):
            # networkpin.on()
            time.sleep(BLINK_SLEEP)
            # networkpin.off()
            print('blinks {}'.format(blinks))
    for repeat in range(repeat_reports):
        blink_report(n_blinks)


if __name__ == "__main__":
    print('>Hello from main')
    # print('test repeated blink_report')
    # blink_report(3)
    # print('test repeated blink_twice')
    # blink_twice(3)
    print('test repeated blink_twice 3 times')
    blink_twice(n_blinks=7, repeat_reports=2)
    print('done. Thanks!')
