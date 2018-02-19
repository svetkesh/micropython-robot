try:
    import machine
    print('DBG: import ESP8266 "machine" library - done')
except ImportError:
    print('DBG: Could not import ESP8266 "machine" library\n'
          'loading machinedesktop.machine as desktop substitution')
    from machinedesktop import PWM as PWM
    from machinedesktop import Pin as Pin
    #
    # with importing from .dir "cannot perform relative import" raised
    # Traceback(most    recent    call    last):
    # File
    # "/home/arkadii/Documents/projects/micropython-robot/gingermicrorobot/machinedesktop/test_import_machinedesktop.py",\
    # line    11, in < module >
    # from .machinedesktop import Pin as Pin
    # SystemError: Parent module '' not loaded, cannot perform relative import
    #
    # try:
    #     from .machinedesktop import Pin as Pin
    #     print('DBG: imported from \".machinedesktop\"')
    # except ImportError:
    #     try:
    #         from machinedesktop import Pin as Pin
    #         print('DBG: imported from \"machinedesktop\"')
    #     except ImportError:
    #         from ..machinedesktop.machinedesktop import Pin as Pin
    #         print('DBG: imported from \"..machinedesktop.machinedesktop\"')
    # finally:
    #     print('DBG: Pin module could not be imported')

try:
    import ure as re
    print('DBG: import microRE "ure" library successful')
except ImportError:
    try:
        import re
        print('DBG: import standard library RE "re" successful')
    except ImportError:
        print('DBG: import could not be done neither re neither micro "ure"')
        raise SystemExit


def main():
    p = PWM(5)
    p.duty(73)


if __name__ == "__main__":
    main()
