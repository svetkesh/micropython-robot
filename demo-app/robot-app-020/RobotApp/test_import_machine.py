try:
    import machine
    print('DBG: import ESP8266 "machine" library - done')
except ImportError:
    print('DBG: Could not import ESP8266 "machine" library\n'
          'loading MachineDesktopSubsitutor.machine as desktop subsitution')
    from MachineDesktopSubsitutor.machine import PWM as PWM
    from MachineDesktopSubsitutor.machine import PWM as PWM

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
