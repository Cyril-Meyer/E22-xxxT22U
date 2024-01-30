from E22 import E22, Config


def enable(port):
    lora = E22(port)

    config = lora.config_get()
    cfg = Config()
    cfg.set(config)
    cfg.set_rssi_env_noise(True)
    lora.config_set(cfg.get())

    lora.close()
    return


def disable(port):
    lora = E22(port)

    config = lora.config_get()
    cfg = Config()
    cfg.set(config)
    cfg.set_rssi_env_noise(False)
    lora.config_set(cfg.get())

    lora.close()
    return


def get(port):
    lora = E22(port)

    while True:
        print(lora.get_rssi_env_noise())

    lora.close()
