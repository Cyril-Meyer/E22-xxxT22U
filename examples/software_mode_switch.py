import time

from E22 import E22, Config


def enable(port):
    lora = E22(port)

    config = lora.config_get()
    cfg = Config()
    cfg.set(config)
    cfg.set_software_mode_switching(True)
    lora.config_set(cfg.get())

    lora.close()
    return


def disable(port):
    lora = E22(port)

    config = lora.config_get()
    cfg = Config()
    cfg.set(config)
    cfg.set_software_mode_switching(False)
    lora.config_set(cfg.get())

    lora.close()
    return


def test(port):
    lora = E22(port)

    for i in range(3):
        lora.software_mode_switch('transmission')
        time.sleep(0.5)
        lora.software_mode_switch('configuration')
        time.sleep(0.5)

    lora.close()
    return
