# Copyright (c) 2020 Sebastian Wicki
# Copyright (c) 2019 Ivan Belokobylskiy
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
#
# Based on https://github.com/devbis/st7789py_mpy
#
# Notable modifications:
#   - Added support for text()
#   - Pre-allocated shared buffer for text() and draw_rect()
#   - Minor memory optimizations for bytecode builds by using shorter error
#     messages, more aggressive inlining, and making most consts private
"""
Driver for the ST7789 display controller.
"""

import sys

import framebuf
import ustruct
from micropython import const
from utime import sleep_ms

# commands
_ST77XX_NOP = const(0x00)
_ST77XX_SWRESET = const(0x01)
_ST77XX_RDDID = const(0x04)
_ST77XX_RDDST = const(0x09)

_ST77XX_SLPIN = const(0x10)
_ST77XX_SLPOUT = const(0x11)
_ST77XX_PTLON = const(0x12)
_ST77XX_NORON = const(0x13)

_ST77XX_INVOFF = const(0x20)
_ST77XX_INVON = const(0x21)
_ST77XX_DISPOFF = const(0x28)
_ST77XX_DISPON = const(0x29)
_ST77XX_CASET = const(0x2a)
_ST77XX_RASET = const(0x2b)
_ST77XX_RAMWR = const(0x2c)
_ST77XX_RAMRD = const(0x2e)

_ST77XX_PTLAR = const(0x30)
_ST77XX_COLMOD = const(0x3a)
_ST7789_MADCTL = const(0x36)

_ST7789_MADCTL_MY = const(0x80)
_ST7789_MADCTL_MX = const(0x40)
_ST7789_MADCTL_MV = const(0x20)
_ST7789_MADCTL_ML = const(0x10)
_ST7789_MADCTL_BGR = const(0x08)
_ST7789_MADCTL_MH = const(0x04)
_ST7789_MADCTL_RGB = const(0x00)

_ST7789_RDID1 = const(0xda)
_ST7789_RDID2 = const(0xdb)
_ST7789_RDID3 = const(0xdc)
_ST7789_RDID4 = const(0xdd)

ColorMode_65K = const(0x50)
ColorMode_262K = const(0x60)
ColorMode_12bit = const(0x03)
ColorMode_16bit = const(0x05)
ColorMode_18bit = const(0x06)
ColorMode_16M = const(0x07)

_BUF_DEFAULT_LEN = const(512)

_PIXEL_LEN = const(2)

_FONT_HEIGHT = const(8)
_FONT_WIDTH = const(8)


class ST7789:
    def __init__(self, spi, width, height, reset, dc, cs=None, buf=None,
                 xstart=-1, ystart=-1, init=True,
                 color_mode=ColorMode_65K | ColorMode_16bit):
        """
        display = st7789.ST7789(
            SPI(1, baudrate=40000000, phase=0, polarity=1),
            240, 240,
            reset=machine.Pin(5, machine.Pin.OUT),
            dc=machine.Pin(2, machine.Pin.OUT),
            buf=bytearray(128),
        )
        """
        self.width = width
        self.height = height
        self.spi = spi
        self.reset = reset
        self.dc = dc
        self.cs = cs

        if buf is None:
            buf = bytearray(_BUF_DEFAULT_LEN)
        self.buf = memoryview(buf)

        if sys.byteorder == 'little':
            self._to_be16 = lambda c: (c << 8) & 0xff00 | (c >> 8) & 0x00ff
        else:
            self._to_be16 = lambda c: c

        if xstart >= 0 and ystart >= 0:
            self.xstart = xstart
            self.ystart = ystart
        elif (self.width, self.height) == (240, 240):
            self.xstart = 0
            self.ystart = 0
        elif (self.width, self.height) == (135, 240):
            self.xstart = 52
            self.ystart = 40
        else:
            # Unsupported display. Only 240x240 and 135x240 are supported
            # without xstart and ystart provided
            raise ValueError("invalid argument(s) value")
        if init:
            self.hard_reset()
            self.soft_reset()
            self.sleep_mode(False)
            sleep_ms(10)
            self._set_color_mode(color_mode)
            self._set_mem_access_mode(4, True, True, False)
            self.inversion_mode(True)
            sleep_ms(10)
            self.write(_ST77XX_NORON)
            sleep_ms(10)
            self.fill(0)
            self.write(_ST77XX_DISPON)
            sleep_ms(10)

    def cs_low(self):
        if self.cs:
            self.cs.off()

    def cs_high(self):
        if self.cs:
            self.cs.on()

    def write(self, command=None, data=None):
        """SPI write to the device: commands and data"""
        self.cs_low()
        if command is not None:
            self.dc.off()
            self.spi.write(bytes([command]))
        if data is not None:
            self.dc.on()
            self.spi.write(data)
        self.cs_high()

    def hard_reset(self):
        self.cs_low()
        if self.reset is not None:
            self.reset.on()
            sleep_ms(10)
            self.reset.off()
            sleep_ms(10)
            self.reset.on()
            sleep_ms(10)
        self.cs_high()

    def soft_reset(self):
        self.write(_ST77XX_SWRESET)
        sleep_ms(120)

    def sleep_mode(self, value):
        if value:
            self.write(_ST77XX_SLPIN)
        else:
            self.write(_ST77XX_SLPOUT)

    def inversion_mode(self, value):
        if value:
            self.write(_ST77XX_INVON)
        else:
            self.write(_ST77XX_INVOFF)

    def _set_color_mode(self, mode):
        self.write(_ST77XX_COLMOD, bytes([mode & 0x77]))

    def _set_mem_access_mode(self, rotation, vert_mirror, horz_mirror, is_bgr):
        rotation &= 7
        value = {
            0: 0,
            1: _ST7789_MADCTL_MX,
            2: _ST7789_MADCTL_MY,
            3: _ST7789_MADCTL_MX | _ST7789_MADCTL_MY,
            4: _ST7789_MADCTL_MV,
            5: _ST7789_MADCTL_MV | _ST7789_MADCTL_MX,
            6: _ST7789_MADCTL_MV | _ST7789_MADCTL_MY,
            7: _ST7789_MADCTL_MV | _ST7789_MADCTL_MX | _ST7789_MADCTL_MY,
        }[rotation]

        if vert_mirror:
            value = _ST7789_MADCTL_ML
        elif horz_mirror:
            value = _ST7789_MADCTL_MH

        if is_bgr:
            value |= _ST7789_MADCTL_BGR
        self.write(_ST7789_MADCTL, bytes([value]))

    def _encode_pos(self, x, y):
        """Encode a postion into bytes."""
        return ustruct.pack(">HH", x, y)

    def _encode_pixel(self, color):
        """Encode a pixel color into bytes."""
        return ustruct.pack(">H", color)

    def _set_columns(self, start, end):
        if start > end or end >= self.width:
            return
        start += self.xstart
        end += self.xstart
        self.write(_ST77XX_CASET, self._encode_pos(start, end))

    def _set_rows(self, start, end):
        if start > end or end >= self.height:
            return
        start += self.ystart
        end += self.ystart
        self.write(_ST77XX_RASET, self._encode_pos(start, end))

    def set_window(self, x0, y0, x1, y1):
        self._set_columns(x0, x1)
        self._set_rows(y0, y1)
        self.write(_ST77XX_RAMWR)

    def vline(self, x, y, length, color):
        self.fill_rect(x, y, 1, length, color)

    def hline(self, x, y, length, color):
        self.fill_rect(x, y, length, 1, color)

    def pixel(self, x, y, color):
        self.set_window(x, y, x, y)
        self.write(None, self._encode_pixel(color))

    def blit_buffer(self, buffer, x, y, width, height):
        self.set_window(x, y, x + width - 1, y + height - 1)
        self.write(None, buffer)

    def rect(self, x, y, w, h, color):
        self.hline(x, y, w, color)
        self.vline(x, y, h, color)
        self.vline(x + w - 1, y, h, color)
        self.hline(x, y + h - 1, w, color)

    def fill_rect(self, x, y, width, height, color):
        buf_len = len(self.buf)
        chunks, rest = divmod(width * height * _PIXEL_LEN, buf_len)
        f = framebuf.FrameBuffer(
            self.buf, buf_len // _PIXEL_LEN, 1, framebuf.RGB565)
        f.fill(self._to_be16(color))

        self.set_window(x, y, x + width - 1, y + height - 1)
        if chunks:
            for _ in range(chunks):
                self.write(None, self.buf)
        if rest:
            self.write(None, self.buf[:rest])

    def fill(self, color):
        self.fill_rect(0, 0, self.width, self.height, color)

    def line(self, x0, y0, x1, y1, color):
        # Line drawing function.  Will draw a single pixel wide line starting at
        # x0, y0 and ending at x1, y1.
        steep = abs(y1 - y0) > abs(x1 - x0)
        pixel = self._encode_pixel(color)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx // 2
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1
        while x0 <= x1:
            if steep:
                self.set_window(y0, x0, y0, x0)
                self.write(None, pixel)
            else:
                self.set_window(x0, y0, x0, y0)
                self.write(None, pixel)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1

    def text(self, s, x, y, fg, bg):
        text_width = len(s) * _FONT_WIDTH
        text_mem = text_width * _FONT_HEIGHT * _PIXEL_LEN
        if text_mem > len(self.buf):
            raise ValueError("buffer too small")

        f = framebuf.FrameBuffer(self.buf, text_width,
                                 _FONT_HEIGHT, framebuf.RGB565)
        f.fill(self._to_be16(bg))
        f.text(s, 0, 0, self._to_be16(fg))
        self.blit_buffer(self.buf[:text_mem], x, y, text_width, _FONT_HEIGHT)
