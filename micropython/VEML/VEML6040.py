import time
from machine import I2C
import machine
from micropython import const
from math import exp, isnan


#VEML6040 I2C ADDRESS

_VEML6040_I2C_ADDRESS    = const(0x10)

# REGISTER CONF (00H) SETTINGS

_VEML6040_IT_40MS        = const(0x00)
_VEML6040_IT_80MS        = const(0x10)
_VEML6040_IT_160MS       = const(0x20)
_VEML6040_IT_320MS       = const(0x30)
_VEML6040_IT_640MS       = const(0x40)
_VEML6040_IT_1280MS      = const(0x50)

_VEML6040_TRIG_DISABLE   = const(0x00)
_VEML6040_TRIG_ENABLE    = const(0x04)

_VEML6040_AF_AUTO        = const(0x00)
_VEML6040_AF_FORCE       = const(0x02)

_VEML6040_SD_ENABLE      = const(0x00)
_VEML6040_SD_DISABLE     = const(0x01)

#COMMAND CODES

_COMMAND_CODE_CONF       = const(0x00)
_COMMAND_CODE_RED        = const(0x08)
_COMMAND_CODE_GREEN      = const(0x09)
_COMMAND_CODE_BLUE       = const(0x0A)
_COMMAND_CODE_WHITE      = const(0x0B)

#G SENSITIVITY

_VEML6040_GSENS_40MS     = 0.25168
_VEML6040_GSENS_80MS     = 0.12584
_VEML6040_GSENS_160MS    = 0.06292
_VEML6040_GSENS_320MS    = 0.03146
_VEML6040_GSENS_640MS    = 0.01573
_VEML6040_GSENS_1280MS   = 0.007865

lastConfiguration = 0

class VEML6040:

	def __init__(self, i2c, address=_VEML6040_I2C_ADDRESS):
		self.i2c = i2c
		self.address = address


	def setConfiguration(self, configuration):

		
		self.i2c.writeto(self.address, bytes([_COMMAND_CODE_CONF,configuration, 0]))
		self.lastConfiguration = configuration

        def read(self, commandCode):
		self.i2c.writeto(self.address, bytes([commandCode]))
		data = self.i2c.readfrom(self.address, 2)
                data = data[0] + (data[1]<<8)
		return data

	def getRed(self):
		return self.read(_COMMAND_CODE_RED)

	def getGreen(self):
		return self.read(_COMMAND_CODE_GREEN)
	
	def getBlue(self):
		return self.read(_COMMAND_CODE_BLUE)
	
	def getWhite(self):
		return self.read(_COMMAND_CODE_WHITE)

	def getAmbientLight(self):
		sensorValue = self.read(_COMMAND_CODE_GREEN)
	
		if lastConfiguration == _VEML6040_IT_40MS:
			ambientLightInLux = sensorValue * _VEML6040_GSENS_40MS
		elif lastConfiguration == _VEML6040_IT_80MS:
			ambientLightInLux = sensorValue * _VEML6040_GSENS_80MS
		elif lastConfiguration == _VEML6040_IT_160MS:
				ambientLightInLux = sensorValue * _VEML6040_GSENS_160MS
		elif lastConfiguration == _VEML6040_IT_320MS:
				ambientLightInLux = sensorValue * _VEML6040_GSENS_320MS
		elif lastConfiguration == _VEML6040_IT_640MS:
				ambientLightInLux = sensorValue * _VEML6040_GSENS_640MS
		elif lastConfiguration == _VEML6040_IT_1280MS:
				ambientLightInLux = sensorValue * _VEML6040_GSENS_1280MS
		else:
			ambientLightInLux = -1
		return ambientLightInLux

	def getCCT(self, offset):
		red = self.read(_COMMAND_CODE_RED)
		green = int.from_bytes(self._i2c_read_words_from_cmd(_COMMAND_CODE_GREEN,0.01,2),byteorder='big')
		blue = self.read(_COMMAND_CODE_BLUE)

		ccti = (float(red) - float(blue)) / float(green)
		ccti = ccti + offset
		cct = 4278.6 * pow(ccti, -1.2455)

		return cct

	def startSensorAuto(self):
		self.setConfiguration(_VEML6040_IT_320MS + _VEML6040_AF_AUTO + _VEML6040_SD_ENABLE);



if __name__ == '__main__':
    #simple test code
    i2c = machine.I2C(scl=machine.Pin(22),sda=machine.Pin(21), freq=10000)
    veml = VEML6040(i2c)
    #while(True):
    #    print(veml.get_data())
    #    sleep(1)
