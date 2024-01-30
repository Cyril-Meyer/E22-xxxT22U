import time

import serial

from utils import set_bit, set_bits


class Config:
    def __init__(self, model='400T22U'):
        assert model in ['230T22U', '400T22U', '900T22U']
        self.model = model
        # 00H : ADDH, 01H : ADDL
        self.address = bytearray.fromhex('0000')
        # 02H : NETID
        self.netid = bytearray.fromhex('00')
        # 03H : REG0
        self.reg0 = bytearray.fromhex('62')
        # 04H : REG1
        self.reg1 = bytearray.fromhex('00')
        # 05H : REG2
        self.reg2 = bytearray.fromhex('17')
        # 06H : REG3
        self.reg3 = bytearray.fromhex('03')
        # 07H : CRYPT_H, 08H : CRYPT_L, write only
        self.crypt = bytearray.fromhex('0000')

    def get(self):
        return self.address + self.netid + self.reg0 + self.reg1 + self.reg2 + self.reg3 + self.crypt

    def set(self, data: bytearray):
        assert len(data) == 9
        self.address = data[0:2]
        self.netid = data[2:3]
        self.reg0 = data[3:4]
        self.reg1 = data[4:5]
        self.reg2 = data[5:6]
        self.reg3 = data[6:7]
        self.crypt = data[7:9]

    def set_address(self, address: bytearray):
        assert len(address) == 2
        # ADDH and ADDL
        self.address = address[0:2]

    def set_netid(self, netid: bytearray):
        assert len(netid) == 1
        # NETID
        self.netid = netid[0:1]

    def set_serial_baud(self, baudrate=9600):
        assert baudrate in [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
        # REG0 bits 7,6,5
        if baudrate in [1200, 2400, 4800, 9600]:
            self.reg0[0] = set_bit(self.reg0[0], 7, False)
        else:
            self.reg0[0] = set_bit(self.reg0[0], 7, True)
        if baudrate in [1200, 2400, 19200, 38400]:
            self.reg0[0] = set_bit(self.reg0[0], 6, False)
        else:
            self.reg0[0] = set_bit(self.reg0[0], 6, True)
        if baudrate in [1200, 4800, 19200, 57600]:
            self.reg0[0] = set_bit(self.reg0[0], 5, False)
        else:
            self.reg0[0] = set_bit(self.reg0[0], 5, True)

    def set_serial_parity(self, parity='8N1'):
        assert parity in ['8N1', '801', '8E1']
        # REG0 bits 4,3
        self.reg0[0] = set_bits(self.reg0[0], [4, 3], [False, False])
        if parity == '801':
            self.reg0[0] = set_bit(self.reg0[0], 3, True)
        if parity == '8E1':
            self.reg0[0] = set_bit(self.reg0[0], 4, True)

    def set_wireless_speed(self, speed=2):
        assert type(speed) is int
        assert 0 <= speed < 8
        # REG0 bits 2,1,0
        self.reg0[0] = set_bits(self.reg0[0],
                                [2, 1, 0],
                                [True if speed & (1 << (2 - n)) else False for n in range(3)])

    def set_packet_size(self, size=240):
        assert size in [240, 128, 64, 32]
        # REG1 bits 7,6
        if size == 240:
            self.reg1[0] = set_bits(self.reg1[0], [7, 6], [False, False])
        if size == 128:
            self.reg1[0] = set_bits(self.reg1[0], [7, 6], [False, True])
        if size == 64:
            self.reg1[0] = set_bits(self.reg1[0], [7, 6], [True, False])
        if size == 32:
            self.reg1[0] = set_bits(self.reg1[0], [7, 6], [True, True])

    def set_rssi_env_noise(self, enable=False):
        # REG1 bits 5 (= channel RSSI)
        self.reg1[0] = set_bit(self.reg1[0], 5, enable)

    # REG1 bits 4,3 are reserved

    def set_software_mode_switching(self, enable=False):
        # REG1 bits 2
        self.reg1[0] = set_bit(self.reg1[0], 2, enable)

    def set_transmitting_power(self, power=3):
        assert type(power) is int
        assert 0 <= power < 4
        # REG1 bits 1,0
        self.reg1[0] = set_bits(self.reg1[0],
                                [1, 0],
                                [False if power & (1 << (1 - n)) else True for n in range(2)])

    def set_channel(self, chan):
        if self.model == '230T22U':
            assert 0 <= chan <= 64
        if self.model == '400T22U':
            assert 0 <= chan <= 83
        if self.model == '900T22U':
            assert 0 <= chan <= 80
        # REG2
        self.reg2 = bytearray([chan])

    def set_rssi_bytes(self, enable=False):
        # REG3 bits 7 (= packet RSSI)
        self.reg3[0] = set_bit(self.reg3[0], 7, enable)

    def set_transmission_method_fixed(self, fixed=False):
        # REG3 bits 6
        self.reg3[0] = set_bit(self.reg3[0], 6, fixed)

    def set_relay_function(self, enable=False):
        # REG3 bits 5
        self.reg3[0] = set_bit(self.reg3[0], 5, enable)

    def set_listened_before_transmitting(self, enable=False):
        # REG3 bits 4
        self.reg3[0] = set_bit(self.reg3[0], 4, enable)

    # REG3 bits 3, 2, 1, 0 are reserved

    def set_key(self, key: bytearray):
        assert len(key) == 2
        # CRYPT_H and CRYPT_L
        self.crypt = key[0:2]


class E22:
    def __init__(self, serial_port, baudrate=9600, timeout=0.1):
        self.ser = serial.Serial(serial_port, baudrate=baudrate, timeout=timeout)

    def send(self, data: bytearray):
        self.ser.write(data)

    def recv(self, size=None):
        if size is None:
            return self.ser.read(self.ser.in_waiting)
        else:
            return self.ser.read(size)

    def recv_print(self, prefix=''):
        if self.ser.in_waiting > 0:
            print(f'{prefix}{self.ser.read(self.ser.in_waiting).hex()}')

    def close(self):
        self.ser.close()

    def get_rssi_env_noise(self, delay=0.2):
        time.sleep(delay)
        self.ser.write(bytearray.fromhex('C0C1C2C30002'))
        time.sleep(delay)
        data = bytearray(self.ser.read(self.ser.in_waiting))
        if len(data) == 0:
            return 'RSSI NOT ENABLED'
        return f'RSSI : Ambient={-data[3]/2} dBm LastRecv={-data[4]/2} dBm'

    # ----- E22 CONFIGURATION -----
    def config_get(self, delay=0.1) -> bytearray:
        # Check connectivity
        # C1 00 -> FF FF FF
        time.sleep(delay)
        self.ser.write(bytearray.fromhex('C100'))
        data = bytearray(self.ser.read(3))
        if not data == b'\xff\xff\xff':
            raise Exception('config_get: check connectivity', data)

        # Read configuration
        # C1 00 09 -> C1 00 09 + 9 bytes configuration
        time.sleep(delay)
        self.ser.write(bytearray.fromhex('C10009'))
        data = bytearray(self.ser.read(12))
        if not len(data) == 12:
            raise Exception('config_get: read config', data)

        return data[3:]

    def config_get_pid(self, delay=0.1) -> bytearray:
        # Read PID
        # C1 80 07 -> C1 80 07 + 7 bytes PID
        time.sleep(delay)
        self.ser.write(bytearray.fromhex('C18007'))
        data = bytearray(self.ser.read(10))
        if not len(data) == 10:
            raise Exception('config_get_pid', data)

        return data[3:]

    def config_set(self, config: bytearray, delay=0.1):
        assert len(config) == 9
        # Check connectivity
        # C1 00 -> FF FF FF
        time.sleep(delay)
        self.ser.write(bytearray.fromhex('C100'))
        data = bytearray(self.ser.read(3))
        if not data == b'\xff\xff\xff':
            raise Exception('config_set: check connectivity', data)

        # Set configuration
        # C0 00 09 + 9 bytes configuration -> C1 00 09 + 9 bytes configuration
        time.sleep(delay)
        self.ser.write(bytearray.fromhex('C00009') + config)
        data = bytearray(self.ser.read(12))
        if not len(data) == 12 or not bytearray(data) == bytearray.fromhex('C10009') + config:
            raise Exception('config_set: set config', data)

    def software_mode_switch(self, mode, delay=0.1):
        assert mode in ['transmission', 'configuration']
        time.sleep(delay)
        if mode == 'transmission':
            self.ser.write(bytearray.fromhex('C0C1C2C30200'))
        if mode == 'configuration':
            self.ser.write(bytearray.fromhex('C0C1C2C30201'))
        time.sleep(delay)
        data = bytearray(self.ser.read(5))
        if not len(data) == 5:
            raise Exception('software_mode_switch: software mode switct not enabled', data)
        if mode == 'transmission' and not data == bytearray.fromhex('C1C2C30200'):
            raise Exception('software_mode_switch: not set', data)
        if mode == 'configuration' and not data == bytearray.fromhex('C1C2C30201'):
            raise Exception('software_mode_switch: not set', data)
