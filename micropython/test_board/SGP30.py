import time
from machine import I2C
import machine
from micropython import const
from math import exp, isnan


_SGP30_DEFAULT_I2C_ADDR  = const(0x58)
_SGP30_FEATURESET        = const(0x0020)

_SGP30_CRC8_POLYNOMIAL   = const(0x31)
_SGP30_CRC8_INIT         = const(0xFF)
_SGP30_WORD_LEN          = const(2)


class SGP30_Sensor:
    """
    A driver for the SGP30 gas sensor.
    """

    def __init__(self, i2c, address=_SGP30_DEFAULT_I2C_ADDR):
        """Initialize the sensor, get the serial # and verify that we found a proper SGP30"""
        self.i2c = i2c
        self.address = address
        # get unique serial, its 48 bits so we store in an array
        self.serial = self._i2c_read_words_from_cmd([0x36, 0x82], 0.01, 3)

        #Optional self test, should not be neccessary
        #self.test = self._i2c_read_words_from_cmd([0x20, 0x32], 2.2, 1)
        #if self.test != 0xD400:
        #    raise RuntimeError('SGP30 measure test not succesfull')

        #Checking firmware of the SGP30, should not be neccessary
        #featureset = self._i2c_read_words_from_cmd([0x20, 0x2f], 0.01, 1)
        #if featureset[0] != 0x1003:#_SGP30_FEATURESET:
        #   raise RuntimeError('SGP30 Not detected or different featureset')

        self.iaq_init()

    def iaq_init(self):
        """Initialize the IAQ algorithm"""
        # name, command, signals, delay
        self._run_profile(["iaq_init", [0x20, 0x03], 0, 0.01])

    def iaq_measure(self):
        """Measure the CO2eq and TVOC"""
        # name, command, signals, delay
        return self._run_profile(["iaq_measure", [0x20, 0x08], 2, 0.05])

    def raw_measure(self):
        """Measure Raw"""
        # name, command, signals, delay
        return self._run_profile(["raw_measure", [0x20, 0x50], 2, 0.025])

    def get_iaq_baseline(self):
        """Retreive the IAQ algorithm baseline for CO2eq and TVOC"""
        # name, command, signals, delay
        return self._run_profile(["iaq_get_baseline", [0x20, 0x15], 2, 0.01])


    def set_iaq_baseline(self, co2eq, tvoc):
        """Set the previously recorded IAQ algorithm baseline for CO2eq and TVOC"""
        if co2eq == 0 and tvoc == 0:
            raise RuntimeError('Invalid baseline')
        buffer = []
        for value in [tvoc, co2eq]:
            arr = [value >> 8, value & 0xFF]
            arr.append(self._generate_crc(arr))
            buffer += arr
        self._run_profile(["iaq_set_baseline", [0x20, 0x1e] + buffer, 0, 0.01])


    # Low level command functions

    def _run_profile(self, profile):
        """Run an SGP 'profile' which is a named command set"""
        name, command, signals, delay = profile

        return self._i2c_read_words_from_cmd(command, delay, signals)


    def _i2c_read_words_from_cmd(self, command, delay, reply_size):
        """Run an SGP command query, get a reply and CRC results if necessary"""
        # a word consists of two bytes and is followed by a crc checksum
        self.i2c.writeto(self.address, bytes(command))

        time.sleep(delay)
        if not reply_size:
            return None
        crc_result = self.i2c.readfrom(self.address, reply_size*3)
        result = []
        for i in range(reply_size):
            word = [crc_result[3*i], crc_result[3*i+1]]
            crc = crc_result[3*i+2]
            if self._generate_crc(word) != crc:
                raise RuntimeError('CRC Error')
            result.append(word[0] << 8 | word[1])
        return result

    def _i2c_write_words_to_cmd(self,cmd, data):
        """Write bytes of words including checksum via i2c
        data is an array of words"""
        buf = [(cmd>>8),(cmd & 0xFF)]
        for d in data:
            buf.append(d>>8)
            buf.append(d & 0xFF)
            buf.append(self._generate_crc([d>>8, d & 0xFF]))
        write_size = i2c.writeto(self.address,bytes(buf))
        return write_size

    def _generate_crc(self, data):
        """8-bit CRC algorithm for checking data"""
        crc = _SGP30_CRC8_INIT
        # calculates 8-Bit checksum with given polynomial
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ _SGP30_CRC8_POLYNOMIAL
                else:
                    crc <<= 1
        return crc & 0xFF

    def get_data(self):
        """Return a dictionary of data consisting of raw and processed values"""
        raw = self.raw_measure()
        iaq = self.iaq_measure()
        data_dict = {'SGP30_H2_RAW': raw[0], 'SGP30_ETOH_RAW': raw[1], 'SGP30_CO2EQ' : iaq[0], 'SGP30_TVOC':iaq[1]}
        return data_dict



if __name__ == '__main__':
    #simple test code
    i2c = machine.I2C(scl=machine.Pin(22),sda=machine.Pin(21), freq=10000)
    sgp = SGP30_Sensor(i2c)
    while(True):
        print(sgp.get_data())
        sleep(1)
