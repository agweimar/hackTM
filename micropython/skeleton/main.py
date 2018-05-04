# coding: utf-8

import gc
import machine

import sx127x
import config_sensorboard

from time import sleep

def timer_callback(timer):
    global send_flag
    #print('timer isr')
    send_flag=True

# timer for max send intervals
timer = machine.Timer(1)
timer.init(period=pir_delay, mode=machine.Timer.PERIODIC, callback=timer_callback)
send_flag=False

# Initialize controller
# add lora transceiver
controller = config_sensorboard.Controller()
lora = controller.add_transceiver(sx127x.SX127x(name = 'LoRa'))

controller.show_text("Hello HackTM!", x = 0, y = 0, clear_first=True)
gc.collect()

while 1:

    #sleep(3)
    #gc.collect()
