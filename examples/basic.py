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
