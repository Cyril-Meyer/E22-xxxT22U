import examples.basic
import examples.software_mode_switch


import serial.tools.list_ports

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=None, help='selected serial port')
    parser.add_argument('--list-port', action='store_true', help='list serial port')
    parser.add_argument('--default', action='store_true', help='reset default configuration')
    # read
    parser.add_argument('--recv', action='store_true', help='read serial')
    # write
    parser.add_argument('--send', action='store_true', help='write serial')
    parser.add_argument('--send-random', action='store_true', help='send random data')
    # software mode
    parser.add_argument('--enable-software-mode-switch', action='store_true', help='enable software mode switch')
    parser.add_argument('--software-mode-switch', action='store_true', help='example software mode switch')
    args = parser.parse_args()

    if args.list_port:
        for port in serial.tools.list_ports.comports():
            print(port.device)

    if args.port is None:
        print('ERROR: NO SERIAL PORT SPECIFIED')
        exit(0)

    if args.recv:
        print('> RECV')
        examples.basic.recv(args.port)

    if args.send:
        print('> SEND')
        examples.basic.send(args.port)

    if args.send_random:
        print('> SEND')
        examples.basic.send_random(args.port)

    if args.enable_software_mode_switch:
        print('> ENABLE SOFTWARE MODE SWITCH')
        examples.software_mode_switch.enable(args.port)
        print('> ENABLE SOFTWARE MODE SWITCH : FINISHED')

    if args.software_mode_switch:
        print('> SOFTWARE MODE SWITCH : BLINK 3 TIMES')
        examples.software_mode_switch.test(args.port)
        print('> SOFTWARE MODE SWITCH : FINISHED')
