# micropython-m5stickc-plus

This repository contains drivers for various components available on the
[M5StickC Plus](M5StickCPlus) platform. All drivers are written in pure
[Micropython](https://micropython.org/) and are intended to be used with the
generic Micropython build for ESP32-based boards.

[M5StickCPlus]: https://docs.m5stack.com/#/en/core/m5stickc_plus

## Example

```python
import random
import machine

import axp192
import colors
import pcf8563
import st7789

# Set up AXP192 PMU
i2c = machine.I2C(0, sda=machine.Pin(21), scl=machine.Pin(22), freq=400000)
pmu = axp192.AXP192(i2c)
print("Battery Status: {:.2f} V".format(pmu.batt_voltage()))

# Set up BM8563 RTC (it is a clone of the NXP PCF8563)
rtc = pcf8563.PCF8563(i2c)
print("Current Date and Time: {}", rtc.datetime())

# Set up ST7789 TFT
spi = machine.SPI(1, baudrate=20_000_000, polarity=1,
                  sck=machine.Pin(13, machine.Pin.OUT),
                  miso=machine.Pin(4, machine.Pin.IN),  # NC
                  mosi=machine.Pin(15, machine.Pin.OUT))

tft = st7789.ST7789(spi, 135, 240,
                        reset=machine.Pin(18, machine.Pin.OUT),
                        dc=machine.Pin(23, machine.Pin.OUT),
                        cs=machine.Pin(5, machine.Pin.OUT),
                        buf=bytearray(2048))

c = colors.rgb565(
    random.getrandbits(8),
    random.getrandbits(8),
    random.getrandbits(8),
)
tft.fill(c)
tft.text("Hello World", 10, 30, colors.WHITE, c)
```

Some of the modules in this repository make use of [`micropython.const`](const)
to optimize memory usage when deployed in [pre-compiled bytecode](mpy) form.

[const]: http://docs.micropython.org/en/latest/library/micropython.html#micropython.const
[mpy]: http://docs.micropython.org/en/latest/reference/mpyfiles.html

## Contributing

Contributions are welcome! Please read and follow the
[Code of Conduct](CODE_OF_CONDUCT.md) and make sure to acknowledge the
[Developer Certificate of Origin](https://developercertificate.org/) when
contributing.
