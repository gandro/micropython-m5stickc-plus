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
Driver for the AXP192 power management unit.
"""

from micropython import const

_AXP192_I2C_DEFAULT_ADDR = const(0x34)

_AXP192_POWER_STATUS = const(0x00)
_AXP192_MODE_CHARGING_STATUS = const(0x01)

_AXP192_EXTEN_DCDC2_CTRL = const(0x10)
_AXP192_EXTEN_DCDC2_CTRL_EXTEN = const(0b0000_0100)
_AXP192_EXTEN_DCDC2_CTRL_DCDC2 = const(0b0000_0001)

_AXP192_DCDC13_LDO23_CTRL = const(0x12)
_AXP192_DCDC13_LDO23_CTRL_LDO3 = const(0b0000_1000)
_AXP192_DCDC13_LDO23_CTRL_LDO2 = const(0b0000_0100)
_AXP192_DCDC13_LDO23_CTRL_DCDC3 = const(0b0000_0010)
_AXP192_DCDC13_LDO23_CTRL_DCDC1 = const(0b0000_0001)

_AXP192_LDO23_OUT_VOLTAGE = const(0x28)
_AXP192_LDO23_OUT_VOLTAGE_LDO2_3_0V = const(0b1100_0000)
_AXP192_LDO23_OUT_VOLTAGE_LDO2_MASK = const(0b1111_0000)
_AXP192_LDO23_OUT_VOLTAGE_LDO3_3_0V = const(0b0000_1100)
_AXP192_LDO23_OUT_VOLTAGE_LDO3_MASK = const(0b0000_1111)

_AXP192_VBUS_IPSOUT = const(0x30)
_AXP192_VBUS_IPSOUT_IGNORE_VBUSEN = const(0b1000_0000)
_AXP192_VBUS_IPSOUT_VHOLD_LIMIT = const(0b0100_0000)
_AXP192_VBUS_IPSOUT_VHOLD_VOLTAGE_4_4V = const(0b0010_0000)
_AXP192_VBUS_IPSOUT_VHOLD_VOLTAGE_MASK = const(0b0011_1000)
_AXP192_VBUS_IPSOUT_VBUS_LIMIT_CURRENT = const(0b0000_0010)
_AXP192_VBUS_IPSOUT_VBUS_LIMIT_CURRENT_500mA = const(0b0000_0001)
_AXP192_VBUS_IPSOUT_VBUS_LIMIT_CURRENT_100mA = const(0b0000_0000)

_AXP192_POWER_OFF_VOLTAGE = const(0x31)
_AXP192_POWER_OFF_VOLTAGE_2_6V = const(0b0000)
_AXP192_POWER_OFF_VOLTAGE_2_7V = const(0b0001)
_AXP192_POWER_OFF_VOLTAGE_2_8V = const(0b0010)
_AXP192_POWER_OFF_VOLTAGE_2_9V = const(0b0011)
_AXP192_POWER_OFF_VOLTAGE_3_0V = const(0b0100)
_AXP192_POWER_OFF_VOLTAGE_3_1V = const(0b0101)
_AXP192_POWER_OFF_VOLTAGE_3_2V = const(0b0110)
_AXP192_POWER_OFF_VOLTAGE_3_3V = const(0b0111)
_AXP192_POWER_OFF_VOLTAGE_MASK = const(0b0111)

_AXP192_POWER_OFF_BATT_CHGLED_CTRL = const(0x32)
_AXP192_POWER_OFF_BATT_CHGLED_CTRL_OFF = const(0b1000_0000)

_AXP192_CHARGING_CTRL1 = const(0x33)
_AXP192_CHARGING_CTRL1_ENABLE = const(0b1000_0000)
_AXP192_CHARGING_CTRL1_VOLTAGE_4_36V = const(0b0110_0000)
_AXP192_CHARGING_CTRL1_VOLTAGE_4_20V = const(0b0100_0000)
_AXP192_CHARGING_CTRL1_VOLTAGE_4_15V = const(0b0010_0000)
_AXP192_CHARGING_CTRL1_VOLTAGE_4_10V = const(0b0000_0000)
_AXP192_CHARGING_CTRL1_VOLTAGE_MASK = const(0b0110_0000)
_AXP192_CHARGING_CTRL1_CHARGING_THRESH_15PERC = const(0b0001_0000)
_AXP192_CHARGING_CTRL1_CHARGING_THRESH_10PERC = const(0b0000_0000)
_AXP192_CHARGING_CTRL1_CHARGING_THRESH_MASK = const(0b0001_0000)
_AXP192_CHARGING_CTRL1_CURRENT_100mA = const(0b0000_0000)
_AXP192_CHARGING_CTRL1_CURRENT_MASK = const(0b0000_1111)

_AXP192_CHARGING_CTRL2 = const(0x34)

_AXP192_BACKUP_BATT = const(0x35)
_AXP192_BACKUP_BATT_CHARGING_ENABLE = const(0b1000_0000)
_AXP192_BACKUP_BATT_CHARGING_VOLTAGE_2_5V = const(0b0110_0000)
_AXP192_BACKUP_BATT_CHARGING_VOLTAGE_3_0V = const(0b0010_0000)
_AXP192_BACKUP_BATT_CHARGING_VOLTAGE_3_1V = const(0b0000_0000)
_AXP192_BACKUP_BATT_CHARGING_VOLTAGE_MASK = const(0b0110_0000)
_AXP192_BACKUP_BATT_CHARGING_CURRENT_400uA = const(0b0000_0011)
_AXP192_BACKUP_BATT_CHARGING_CURRENT_200uA = const(0b0000_0010)
_AXP192_BACKUP_BATT_CHARGING_CURRENT_100uA = const(0b0000_0001)
_AXP192_BACKUP_BATT_CHARGING_CURRENT_50uA = const(0b0000_0000)
_AXP192_BACKUP_BATT_CHARGING_CURRENT_MASK = const(0b0000_0011)

_AXP192_PEK = const(0x36)
_AXP192_PEK_SHORT_PRESS_1S = const(0b1100_0000)
_AXP192_PEK_SHORT_PRESS_512mS = const(0b1000_0000)
_AXP192_PEK_SHORT_PRESS_256mS = const(0b0100_0000)
_AXP192_PEK_SHORT_PRESS_128mS = const(0b0000_0000)
_AXP192_PEK_SHORT_PRESS_MASK = const(0b1100_0000)
_AXP192_PEK_LONG_PRESS_2_5S = const(0b0011_0000)
_AXP192_PEK_LONG_PRESS_2_0S = const(0b0010_0000)
_AXP192_PEK_LONG_PRESS_1_5S = const(0b0001_0000)
_AXP192_PEK_LONG_PRESS_1_0S = const(0b0000_0000)
_AXP192_PEK_LONG_PRESS_MASK = const(0b0011_0000)
_AXP192_PEK_LONG_PRESS_POWER_OFF = const(0b0000_1000)
_AXP192_PEK_PWROK_DELAY_64mS = const(0b0000_0100)
_AXP192_PEK_PWROK_DELAY_32mS = const(0b0000_0000)
_AXP192_PEK_PWROK_DELAY_MASK = const(0b0000_0100)
_AXP192_PEK_POWER_OFF_TIME_12S = const(0b0000_0011)
_AXP192_PEK_POWER_OFF_TIME_8S = const(0b0000_0010)
_AXP192_PEK_POWER_OFF_TIME_6S = const(0b0000_0001)
_AXP192_PEK_POWER_OFF_TIME_4S = const(0b0000_0000)
_AXP192_PEK_POWER_OFF_TIME_MASK = const(0b0000_0011)

_AXP192_BATT_TEMP_LOW_THRESH = const(0x38)
_AXP192_BATT_TEMP_HIGH_THRESH = const(0x39)
_AXP192_BATT_TEMP_HIGH_THRESH_DEFAULT = const(0b1111_1100)

_AXP192_IRQ_1_ENABLE = const(0x40)
_AXP192_IRQ_2_ENABLE = const(0x41)
_AXP192_IRQ_3_ENABLE = const(0x42)
_AXP192_IRQ_4_ENABLE = const(0x43)
_AXP192_IRQ_5_ENABLE = const(0x4a)

_AXP192_IRQ_1_STATUS = const(0x44)
_AXP192_IRQ_2_STATUS = const(0x45)
_AXP192_IRQ_3_STATUS = const(0x46)
_AXP192_IRQ_4_STATUS = const(0x47)
_AXP192_IRQ_5_STATUS = const(0x4d)

_AXP192_IRQ_3_PEK_SHORT_PRESS = const(0b0000_0010)
_AXP192_IRQ_3_PEK_LONG_PRESS = const(0b0000_0001)

_AXP192_ADC_ACIN_VOLTAGE_H = const(0x56)
_AXP192_ADC_ACIN_VOLTAGE_L = const(0x57)
_AXP192_ADC_ACIN_CURRENT_H = const(0x58)
_AXP192_ADC_ACIN_CURRENT_L = const(0x59)
_AXP192_ADC_VBUS_VOLTAGE_H = const(0x5a)
_AXP192_ADC_VBUS_VOLTAGE_L = const(0x5b)
_AXP192_ADC_VBUS_CURRENT_H = const(0x5c)
_AXP192_ADC_VBUS_CURRENT_L = const(0x5d)
_AXP192_ADC_INTERNAL_TEMP_H = const(0x5e)
_AXP192_ADC_INTERNAL_TEMP_L = const(0x5f)

_AXP192_ADC_BATT_VOLTAGE_H = const(0x78)
_AXP192_ADC_BATT_VOLTAGE_L = const(0x79)

_AXP192_ADC_BATT_POWER_H = const(0x70)
_AXP192_ADC_BATT_POWER_M = const(0x71)
_AXP192_ADC_BATT_POWER_L = const(0x72)

_AXP192_ADC_BATT_CHARGE_CURRENT_H = const(0x7a)
_AXP192_ADC_BATT_CHARGE_CURRENT_L = const(0x7b)
_AXP192_ADC_BATT_DISCHARGE_CURRENT_H = const(0x7c)
_AXP192_ADC_BATT_DISCHARGE_CURRENT_L = const(0x7d)
_AXP192_ADC_APS_VOLTAGE_H = const(0x7e)
_AXP192_ADC_APS_VOLTAGE_L = const(0x7f)

_AXP192_ADC_ENABLE_1 = const(0x82)
_AXP192_ADC_ENABLE_1_BATT_VOL = const(0b1000_0000)
_AXP192_ADC_ENABLE_1_BATT_CUR = const(0b0100_0000)
_AXP192_ADC_ENABLE_1_ACIN_VOL = const(0b0010_0000)
_AXP192_ADC_ENABLE_1_ACIN_CUR = const(0b0001_0000)
_AXP192_ADC_ENABLE_1_VBUS_VOL = const(0b0000_1000)
_AXP192_ADC_ENABLE_1_VBUS_CUR = const(0b0000_0100)
_AXP192_ADC_ENABLE_1_APS_VOL = const(0b0000_0010)
_AXP192_ADC_ENABLE_1_TS_PIN = const(0b0000_0001)

_AXP192_ADC_ENABLE_2 = const(0x83)
_AXP192_ADC_ENABLE_2_TEMP_MON = const(0b1000_0000)
_AXP192_ADC_ENABLE_2_GPIO0 = const(0b0000_1000)
_AXP192_ADC_ENABLE_2_GPIO1 = const(0b0000_0100)
_AXP192_ADC_ENABLE_2_GPIO2 = const(0b0000_0010)
_AXP192_ADC_ENABLE_2_GPIO3 = const(0b0000_0001)

_AXP192_ADC_TS = const(0x84)
_AXP192_ADC_TS_SAMPLE_200HZ = const(0b1100_0000)
_AXP192_ADC_TS_SAMPLE_100HZ = const(0b1000_0000)
_AXP192_ADC_TS_SAMPLE_50HZ = const(0b0100_0000)
_AXP192_ADC_TS_SAMPLE_25HZ = const(0b0000_0000)
_AXP192_ADC_TS_SAMPLE_MASK = const(0b1100_0000)
_AXP192_ADC_TS_OUT_CUR_80uA = const(0b0011_0000)
_AXP192_ADC_TS_OUT_CUR_60uA = const(0b0010_0000)
_AXP192_ADC_TS_OUT_CUR_40uA = const(0b0001_0000)
_AXP192_ADC_TS_OUT_CUR_20uA = const(0b0000_0000)
_AXP192_ADC_TS_OUT_CUR_MASK = const(0b0011_0000)
_AXP192_ADC_TS_PIN_TEMP_MON = const(0b0000_0000)
_AXP192_ADC_TS_PIN_EXTERN_ADC = const(0b0000_0100)
_AXP192_ADC_TS_PIN_OUT_ALWAYS = const(0b0000_0011)
_AXP192_ADC_TS_PIN_OUT_SAVE_ENG = const(0b0000_0010)
_AXP192_ADC_TS_PIN_OUT_CHG = const(0b0000_0001)
_AXP192_ADC_TS_PIN_OUT_DIS = const(0b0000_0000)
_AXP192_ADC_TS_PIN_OUT_MASK = const(0b0000_0011)

_AXP192_GPIO0_FUNCTION = const(0x90)
_AXP192_GPIO0_FUNCTION_FLOATING = const(0b0000_0111)
_AXP192_GPIO0_FUNCTION_LOW_OUTPUT = const(0b0000_0101)
_AXP192_GPIO0_FUNCTION_ADC_INPUT = const(0b0000_0100)
_AXP192_GPIO0_FUNCTION_LDO_OUTPUT = const(0b0000_0010)
_AXP192_GPIO0_FUNCTION_GENERAL_INPUT = const(0b0000_0001)
_AXP192_GPIO0_FUNCTION_OPEN_DRAIN_OUTPUT = const(0b0000_0000)

_AXP192_GPIO0_LDO_VOLTAGE = const(0x91)
_AXP192_GPIO0_LDO_VOLTAGE_3_3V = const(0b1111_0000)
_AXP192_GPIO0_LDO_VOLTAGE_2_8V = const(0b1010_0000)
_AXP192_GPIO0_LDO_VOLTAGE_1_8V = const(0b0000_0000)


class M5StickCPlus:
    @staticmethod
    def on_init(device):
        # Set LDO2 and LDO3 to 3.0V
        device.write(_AXP192_LDO23_OUT_VOLTAGE,
                     _AXP192_LDO23_OUT_VOLTAGE_LDO2_3_0V |
                     _AXP192_LDO23_OUT_VOLTAGE_LDO3_3_0V)

        # Enable EXTEN, Disable DCDC2
        device.write(_AXP192_EXTEN_DCDC2_CTRL,
                     _AXP192_EXTEN_DCDC2_CTRL_EXTEN)

        # Enable LDO2, LDO3, DCDC1
        val = device.read(_AXP192_DCDC13_LDO23_CTRL)
        device.write(_AXP192_DCDC13_LDO23_CTRL, val |
                     _AXP192_DCDC13_LDO23_CTRL_LDO2 |
                     _AXP192_DCDC13_LDO23_CTRL_LDO3 |
                     _AXP192_DCDC13_LDO23_CTRL_DCDC1)

        # ADC Sample Rate 200Hz, TS Pin 80uA, Temp Mon, Energy Saving
        device.write(_AXP192_ADC_TS,
                     _AXP192_ADC_TS_SAMPLE_200HZ |
                     _AXP192_ADC_TS_OUT_CUR_80uA |
                     _AXP192_ADC_TS_PIN_TEMP_MON |
                     _AXP192_ADC_TS_PIN_OUT_SAVE_ENG)

        # ADC Enable Battery, VBus, ACIn, APS, TS
        device.write(_AXP192_ADC_ENABLE_1,
                     _AXP192_ADC_ENABLE_1_BATT_VOL |
                     _AXP192_ADC_ENABLE_1_BATT_CUR |
                     _AXP192_ADC_ENABLE_1_ACIN_VOL |
                     _AXP192_ADC_ENABLE_1_ACIN_CUR |
                     _AXP192_ADC_ENABLE_1_VBUS_VOL |
                     _AXP192_ADC_ENABLE_1_VBUS_CUR |
                     _AXP192_ADC_ENABLE_1_APS_VOL |
                     _AXP192_ADC_ENABLE_1_TS_PIN)

        # VBus limit 500mA, Vbus hold at 4.4V
        device.write(_AXP192_VBUS_IPSOUT,
                     _AXP192_VBUS_IPSOUT_VHOLD_LIMIT |
                     _AXP192_VBUS_IPSOUT_VHOLD_VOLTAGE_4_4V |
                     _AXP192_VBUS_IPSOUT_VBUS_LIMIT_CURRENT |
                     _AXP192_VBUS_IPSOUT_VBUS_LIMIT_CURRENT_500mA)

        # Automatically power off at 3.0V
        device.write(_AXP192_POWER_OFF_VOLTAGE,
                     _AXP192_POWER_OFF_VOLTAGE_3_0V)

        # Battery charging voltage 4.2V, current 100mA
        device.write(_AXP192_CHARGING_CTRL1,
                     _AXP192_CHARGING_CTRL1_ENABLE |
                     _AXP192_CHARGING_CTRL1_VOLTAGE_4_20V |
                     _AXP192_CHARGING_CTRL1_CHARGING_THRESH_10PERC |
                     _AXP192_CHARGING_CTRL1_CURRENT_100mA)

        # PEK Short Press 128ms, Long Press 1.5s, Power Off 4s
        device.write(_AXP192_PEK,
                     _AXP192_PEK_SHORT_PRESS_128mS |
                     _AXP192_PEK_LONG_PRESS_1_5S |
                     _AXP192_PEK_LONG_PRESS_POWER_OFF |
                     _AXP192_PEK_PWROK_DELAY_64mS |
                     _AXP192_PEK_POWER_OFF_TIME_4S)

        # Ensure high temp threshold default value
        device.write(_AXP192_BATT_TEMP_HIGH_THRESH,
                     _AXP192_BATT_TEMP_HIGH_THRESH_DEFAULT)

        # RTC Backup Battery Enable at 3.0V, charging with 200uA
        device.write(_AXP192_BACKUP_BATT,
                     _AXP192_BACKUP_BATT_CHARGING_ENABLE |
                     _AXP192_BACKUP_BATT_CHARGING_VOLTAGE_3_0V |
                     _AXP192_BACKUP_BATT_CHARGING_CURRENT_200uA)

        # Set GPIO0 as LDOIO0 at 3.3V
        device.write(_AXP192_GPIO0_LDO_VOLTAGE,
                     _AXP192_GPIO0_LDO_VOLTAGE_3_3V)
        device.write(_AXP192_GPIO0_FUNCTION,
                     _AXP192_GPIO0_FUNCTION_LDO_OUTPUT)


class AXP192:
    def __init__(self, i2c, addr=_AXP192_I2C_DEFAULT_ADDR, board=None):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(1)
        if self.read(_AXP192_POWER_STATUS) == 0xff:
            raise ValueError("device not found")
        if board is not None:
            board.on_init(self)

    def read(self, regaddr):
        self.i2c.readfrom_mem_into(self.addr, regaddr, self.buf)
        return self.buf[0]

    def write(self, regaddr, val):
        self.buf[0] = val
        self.i2c.writeto_mem(self.addr, regaddr, self.buf)

    def batt_voltage(self):
        val = self.read(_AXP192_ADC_BATT_VOLTAGE_H) << 4
        val |= self.read(_AXP192_ADC_BATT_VOLTAGE_L)
        return val * 1.1 / 1000  # 1.1mV per LSB

    def batt_power(self):
        val = self.read(_AXP192_ADC_BATT_POWER_H) << 16
        val |= self.read(_AXP192_ADC_BATT_POWER_M) << 8
        val |= self.read(_AXP192_ADC_BATT_POWER_L)
        return val * 1.1 * 0.5 / 1000  # 1.1mV * 0.5mA per LSB

    def batt_charge_current(self):
        val = self.read(_AXP192_ADC_BATT_CHARGE_CURRENT_H) << 5
        val |= self.read(_AXP192_ADC_BATT_CHARGE_CURRENT_L)
        return val * 0.5 / 1000  # 0.5mA per LSB

    def batt_discharge_current(self):
        val = self.read(_AXP192_ADC_BATT_DISCHARGE_CURRENT_H) << 5
        val |= self.read(_AXP192_ADC_BATT_DISCHARGE_CURRENT_L)
        return val * 0.5 / 1000  # 0.5mA per LSB

    def acin_voltage(self):
        val = self.read(_AXP192_ADC_ACIN_VOLTAGE_H) << 4
        val |= self.read(_AXP192_ADC_ACIN_VOLTAGE_L)
        return val * 1.7 / 1000  # 1.7mV per LSB

    def acin_current(self):
        val = self.read(_AXP192_ADC_ACIN_CURRENT_H) << 4
        val |= self.read(_AXP192_ADC_ACIN_CURRENT_L)
        return val * 0.625 / 1000  # 0.625mA per LSB

    def vbus_voltage(self):
        val = self.read(_AXP192_ADC_VBUS_VOLTAGE_H) << 4
        val |= self.read(_AXP192_ADC_VBUS_VOLTAGE_L)
        return val * 1.7 / 1000  # 1.7mV per LSB

    def vbus_current(self):
        val = self.read(_AXP192_ADC_VBUS_CURRENT_H) << 4
        val |= self.read(_AXP192_ADC_VBUS_CURRENT_L)
        return val * 0.375 / 1000  # 0.375mA per LSB

    def aps_voltage(self):
        val = self.read(_AXP192_ADC_APS_VOLTAGE_H) << 4
        val |= self.read(_AXP192_ADC_APS_VOLTAGE_L)
        return val * 1.4 / 1000  # 1.4mV per LSB

    def internal_temp(self):
        val = self.read(_AXP192_ADC_INTERNAL_TEMP_H) << 4
        val |= self.read(_AXP192_ADC_INTERNAL_TEMP_L)
        return val * 0.1 - 144.7  # 0.1C per LSB, offset 144.7C

    def pek_button(self, long=False):
        val = self.read(_AXP192_IRQ_3_STATUS)
        val &= _AXP192_IRQ_3_PEK_SHORT_PRESS | _AXP192_IRQ_3_PEK_LONG_PRESS
        self.write(_AXP192_IRQ_3_STATUS, val)  # clear bits
        if long:
            val &= _AXP192_IRQ_3_PEK_LONG_PRESS
        return bool(val)

    def power_off(self):
        val = self.read(_AXP192_POWER_OFF_BATT_CHGLED_CTRL)
        val |= _AXP192_POWER_OFF_BATT_CHGLED_CTRL_OFF
        self.write(_AXP192_POWER_OFF_BATT_CHGLED_CTRL, val)
