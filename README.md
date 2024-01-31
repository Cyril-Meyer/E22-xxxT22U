# E22-xxxT22U
Ebyte E22-xxxT22U USB LoRa modules Library.

TLDR : E22-xxxT22U modules are wireless serial port.

This project aims to make them usable as simply as possible.
This library should work on any Windows, Linux, or Mac computer that has a
working Python setup.

### Quick demo
```python
# init
lora = E22('COM5')
# config
cfg = Config()
cfg.set(lora.config_get())
cfg.set_address(bytearray.fromhex('1234'))
cfg.software_mode_switch('transmission')
lora.config_set(cfg.get())
# send message
lora.send('XXX'.encode())
# recv message and print
lora.recv_print()
```

## Description

Ebyte E22-xxxT22U series are a new generation of LoRa wireless spread spectrum
module, a wireless serial port module based on SEMTECH's SX126x chip.

Multiple modules exists for different frequency band usage.
The communication is compatible between E22-230T/400T/900T series.

| E22-400T22U | E22-900T22U | E22-230T22U |
|:-----------:|:-----------:|:-----------:|
| 410.125 ~ 493.125 MHz | 850.125 ~ 930.125 MHz | 220.125 ~ 236.125 MHz |
| SX1268 | SX1262 | SX1262 |
| ![E22-400T22U](https://www.cdebyte.com/Uploadfiles/Picture/2023-2-17/20232171442365934.jpg) | ![E22-900T22U](https://www.cdebyte.com/Uploadfiles/Picture/2023-2-17/2023217156464860.jpg) | ![E22-230T22U](https://www.cdebyte.com/Uploadfiles/Picture/2023-2-17/20232171353438381.jpg) |
| [cdebyte.com](https://www.cdebyte.com/products/E22-400T22U) | [cdebyte.com](https://www.cdebyte.com/products/E22-900T22U) | [cdebyte.com](https://www.cdebyte.com/products/E22-230T22U) |

**🚧 WORK IN PROGRESS 🚧 TODO : ADD FUNCTIONALITY EXAMPLES AS RELAY**

## Usage
For basic "wireless serial port" usage, you can just use the Ebyte configuration
software as explained in [setup](#setup) and check basic [examples](#examples).
For software mode switching and everything not included in the tool, follow this
documentation.

### Setup
* To enter configuration mode press the side button 2s.
* Red constant light indicates configuration mode is enabled.

When in configuration mode, you can use Ebyte dedicated software to change some
parameters.

| RF Setting Example |
|:------------------:|
| <img src="https://github.com/Cyril-Meyer/E22-xxxT22U/assets/69190238/2f609a8c-fad1-4d18-ad86-d189e891e8d4" width="300"/> |

However, some parameters are not available, like the "Software Mode Switching"
activation.
This option is useful for some use cases, if you want to change configuration
on the fly.

The configuration system is based on register containg the configuration.
The list of all the register and their configuration is available in the
user manual : [E22-xxxT22U.pdf](docs/E22-xxxT22U_UserManual.pdf) (page 13 to 16).

The `E22.Config` class allow you to edit each option of the configuration
individually.

#### Implemented E22 options
* `set_address`
* `set_netid`
* `set_serial_baud`
* `set_serial_parity`
* `set_wireless_speed`
* `set_packet_size`
* `set_rssi_env_noise`
* `set_software_mode_switching`
* `set_transmitting_power`
* `set_channel`
* `set_rssi_bytes`
* `set_transmission_method_fixed`
* `set_relay_function`
* `set_listened_before_transmitting`
* `set_key`

#### Software mode switching
To enable software mode switching, put your E22 in configuration mode using the
side button, then run the activation example :
```
python run_example.py --port COMX --enable-software-mode-switch
```
To check if it worked, run the following example, the dongle will blink.
```
python run_example.py --port COMX --software-mode-switch
```

**🚧 WORK IN PROGRESS 🚧 TODO : ADD MORE ADVANCED CONFIGURATION EXAMPLES**

### Examples
Example with one E22 on port `COM5` and one on port `COM7`:

#### Basic transmission example
```
python run_example.py --port COM5 --recv
python run_example.py --port COM7 --send
```

**send spam data**
```
python run_example.py --port COM5 --send-spam
```

#### RSSI
```
python run_example.py --port COM7 --rssi
RSSI : Ambient=-87.5 dBm LastRecv=0.0 dBm
RSSI : Ambient=-88.0 dBm LastRecv=0.0 dBm
RSSI : Ambient=0.0 dBm LastRecv=0.0 dBm         <--- SPAM FROM ANOTHER E22
RSSI : Ambient=-88.0 dBm LastRecv=0.0 dBm
RSSI : Ambient=-88.0 dBm LastRecv=0.0 dBm
RSSI : Ambient=-88.0 dBm LastRecv=0.0 dBm
RSSI : Ambient=-88.0 dBm LastRecv=0.0 dBm
RSSI : Ambient=-88.0 dBm LastRecv=0.0 dBm
RSSI : Ambient=0.0 dBm LastRecv=0.0 dBm         <--- SPAM FROM ANOTHER E22
RSSI : Ambient=-88.0 dBm LastRecv=0.0 dBm
RSSI : Ambient=-88.0 dBm LastRecv=0.0 dBm
```

**🚧 WORK IN PROGRESS 🚧 TODO : ADD MORE EXAMPLES**
