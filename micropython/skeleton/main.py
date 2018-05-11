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
timer_delay = 1000*5
timer = machine.Timer(1)
timer.init(period=timer_delay, mode=machine.Timer.PERIODIC, callback=timer_callback)
send_flag=False

# Initialize controller
# add lora transceiver
controller = config_sensorboard.Controller()
lora = controller.add_transceiver(sx127x.SX127x(name = 'LoRa',
    parameters = {'frequency': 868.3E6, 'tx_power_level': 10, 'signal_bandwidth': 125E3,
                               'spreading_factor': 10, 'coding_rate': 1, 'preamble_length': 12,
                               'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': True
    }))

controller.show_text("Hello HackTM!", x = 0, y = 0, clear_first=True)
gc.collect()

while 1:

    if send_flag==True:
        payload = "x"
        controller.lora_send(lora, payload)
        print("sending %s" % payload)
        gc.collect()

    #sleep(3)
    #gc.collect()
