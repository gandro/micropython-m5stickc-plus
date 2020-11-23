# Copyright (c) 2020 Sebastian Wicki
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
I2C-based driver for the DHT12 temperature and humidity sensor.
"""
from micropython import const

_DHT12_I2C_DEFAULT_ADDR = const(0x5c)

class DHT12:
    def __init__(self, i2c, addr=_DHT12_I2C_DEFAULT_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(5)

    def measure(self):
        buf = self.buf
        self.i2c.readfrom_mem_into(self.addr, 0x00, buf)
        if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
            raise Exception("checksum error")

    def humidity(self):
        return self.buf[0] + (self.buf[1] * 0.1)

    def temperature(self):
        t = self.buf[2] + ((self.buf[3] & 0b0111_1111) * 0.1)
        if self.buf[2] & 0b1000_0000:
            t = -t
        return t
