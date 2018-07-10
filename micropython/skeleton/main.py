# coding: utf-8
import gc
import machine
import utime
import sx127x
from config_sensorboard import *
import config_sensorboard
from time import sleep

def pir_callback(p):
    global pir_flag
    #print('PIR triggered')
    pir_flag=True

def timer_callback(timer):
    global update_flag
    #print('timer isr')
    update_flag=True

pir_flag = False
offline_flag = False
update_flag = False

# PIR
pir_pin = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)
#pir_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=pir_callback)
pir_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_callback)

# timer for max send intervals
##### timer interrupt and soft reboot dont work well toegether this way --- -> OSError: 261
timer_delay=1000*10
timer = machine.Timer(1)
timer.init(period=timer_delay, mode=machine.Timer.PERIODIC, callback=timer_callback)

# Initialize controller
# add lora transceiver
controller = config_sensorboard.Controller()

lora_parameters = {'frequency': 868.3E6, 'tx_power_level': 14, 'signal_bandwidth': 125E3,
                'spreading_factor': 9, 'coding_rate': 1, 'preamble_length': 12,
                'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': True}
lora_sx127x = sx127x.SX127x(name='LoRa', parameters=lora_parameters)

lora = controller.add_transceiver(lora_sx127x)

# sx127x.SX127x(name = 'LoRa'),
                    # parameters = {'frequency': 867.7E6, 'tx_power_level': 14, 'signal_bandwidth': 125E3,
                            #    'spreading_factor': 9, 'coding_rate': 1, 'preamble_length': 12,
                            #    'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': True}))
gc.collect()

while True:

    if update_flag:
        data = controller.collect_data()
        payload = controller.assemble_payload(data)

        controller.show_text("MAC:" + config_sensorboard.UUID, x = 0, y = 8, clear_first=True)
        controller.show_text("T:" + str(round(data['T'],1)), x = 0, y = 16, clear_first=False)
        controller.show_text("RH:" + str(round(data['RH'],1)), x = 64, y = 16, clear_first=False)
        controller.show_text("Tv:"+str(data['SGP30_TVOC']), x = 0, y = 24, clear_first=False)
        controller.show_text("CO2eq:"+str(data['SGP30_CO2EQ']), x = 56, y = 24, clear_first=False)

        if offline_flag:
            data_str = str(utime.ticks_us())

            for k in data.keys():
                data_str += " " + str(data[k])
            data_str += "\n\r"
            with open('log.txt','w') as f:
                f.write(data_str)

        controller.lora_send(lora, payload)
        lora.sleep()
        update_flag=False

    if pir_flag:
        controller.show_text("Motion detected", x = 0, y = 0, clear_first=False)
    else:
        controller.show_text("No Motion", x = 0, y = 0, clear_first=False)

    gc.collect()
    # see above
    #machine.enable_irq(irq_state)
