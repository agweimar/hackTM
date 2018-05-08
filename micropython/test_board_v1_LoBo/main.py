# coding: utf-8

import gc
import machine

import sx127x
import config_sensorboard
from time import sleep

def pir_callback(p):
    global pir_flag
    #print('PIR triggered')
    pir_flag=True

def timer_callback(timer):
    global send_flag
    #print('timer isr')
    send_flag=True

# PIR
pir_pin = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)
#pir_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=pir_callback)
pir_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_callback)
pir_flag=False
pir_delay=1000*10

# timer for max send intervals
##### timer interrupt and soft reboot dont work well toegether this way --- -> OSError: 261
timer = machine.Timer(1)
timer.init(period=pir_delay, mode=machine.Timer.PERIODIC, callback=timer_callback)
send_flag=False

# Initialize controller
# add lora transceiver
controller = config_sensorboard.Controller()
lora = controller.add_transceiver(sx127x.SX127x(name = 'LoRa'))

gc.collect()

while 1:

    if send_flag==True:
        # disabling and reenabling interrupts causes reboots
        #irq_state = machine.disable_irq()
        controller.show_text("Timer triggered")
        sleep(0.5)
        controller.show_text("...", clear_first=True)
        if pir_flag:
            data = controller.collect_data()
            payload = controller.assemble_payload(data)
            controller.lora_send(lora, payload)
            lora.sleep()

            controller.show_text("sent: OK", x = 0, y = 0, clear_first=True)
            controller.show_text("MAC:"+config_sensorboard.UUID, x = 0, y = 8, clear_first=False)
            controller.show_text("T:" + str(round(data['T'],1)), x = 0, y = 16, clear_first=False)
            controller.show_text("RH:" + str(round(data['RH'],1)), x = 64, y = 16, clear_first=False)
            controller.show_text("Tv:"+str(data['SGP30_TVOC']), x = 0, y = 24, clear_first=False)
            controller.show_text("CO2eq:"+str(data['SGP30_CO2EQ']), x = 56, y = 24, clear_first=False)

            pir_flag=False
        send_flag=False

        gc.collect()
        # see above
        #machine.enable_irq(irq_state)
