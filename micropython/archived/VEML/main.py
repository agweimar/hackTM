# coding: utf-8

import gc
import machine
import utime
import sx127x
import config_sensorboard
from time import sleep
import VEML6040

controller = config_sensorboard.Controller()
veml = VEML6040.VEML6040(controller.i2c)
veml.startSensorAuto()

while 1:
    controller.show_text("Red: " + str(veml.getRed()),x=0,y=0,clear_first = True)
    controller.show_text("Green: " + str(veml.getGreen()), x = 0, y = 8, clear_first = False)
    controller.show_text("Blue: " + str(veml.getBlue()), x = 0, y = 16, clear_first = False)
    controller.show_text("White " + str(veml.getWhite()), x = 0, y = 24, clear_first = False)
    controller.show_text("Ambient: " + str(veml.getAmbientLight()), x = 0, y = 32, clear_first = False)
    sleep(1)

