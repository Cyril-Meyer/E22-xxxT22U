import time

from E22 import E22


def recv(port):
    lora = E22(port)

    while True:
        lora.recv_print('$>')

    lora.close()


def send(port):
    lora = E22(port)

    while True:
        lora.send(input().encode())

    lora.close()


def send_spam(port):
    lora = E22(port)

    while True:
        for i in range(16):
            lora.send(f'SPAM'.encode())
        time.sleep(2.5)

    lora.close()
