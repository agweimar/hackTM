# coding: utf-8

import gc
import machine
import json
from time import sleep

import SGP30, SHTC1

import sx127x
import config_lora 
from config_lora import uuid


VERSION=1

def pir_callback(p):
    global pir_flag
    print('PIR triggered')
    pir_flag=True

def timer_irq(timer):
    global send_flag
    #print('timer isr')
    send_flag=True

def send(lora, data_dict):

    print("LoRa Sender")

    payload = '{0},{1}'.format(uuid, data_dict)
    print("Sending packet: \n{}\n".format(payload))
    lora.println(payload) 

#i2c vars
scl_i2c = machine.Pin(22)
sda_i2c = machine.Pin(21)
freq_i2c = 100000

# init i2c
i2c = machine.I2C(scl = scl_i2c, sda = sda_i2c, freq=freq_i2c)
i2c_devices = i2c.scan()

# sensors
i2c = machine.I2C(scl = scl_i2c, sda = sda_i2c, freq=10000)

sgp = SGP30.SGP30_Sensor(i2c)
shtc = SHTC1.SHTC1_Sensor(i2c)

# PIR
pir_pin = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)
pir_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=pir_callback)
pir_flag=False
pir_delay=6*1000

# timer for max send intervals
timer = machine.Timer(1)
timer.init(period=pir_delay, mode=machine.Timer.PERIODIC, callback=timer_irq)
send_flag=False

# Controller(
               # pin_id_led = ON_BOARD_LED_PIN_NO, 
               # on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
               # pin_id_reset = PIN_ID_FOR_LORA_RESET, 
               # blink_on_start = (2, 0.5, 0.5))
controller = config_lora.Controller()
    
    
# SX127x(name = 'SX127x',
           # parameters = {'frequency': 433E6, 'tx_power_level': 2, 'signal_bandwidth': 125E3,
                         # 'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,
                         # 'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False},
           # onReceive = None)
           
# controller.add_transceiver(transceiver,
                               # pin_id_ss = PIN_ID_FOR_LORA_SS,
                               # pin_id_RxDone = PIN_ID_FOR_LORA_DIO0,
                               # pin_id_RxTimeout = PIN_ID_FOR_LORA_DIO1,
                               # pin_id_ValidHeader = PIN_ID_FOR_LORA_DIO2,
                               # pin_id_CadDone = PIN_ID_FOR_LORA_DIO3,
                               # pin_id_CadDetected = PIN_ID_FOR_LORA_DIO4,
                               # pin_id_PayloadCrcError = PIN_ID_FOR_LORA_DIO5)                        
lora = controller.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                      pin_id_ss = config_lora.Controller.PIN_ID_FOR_LORA_SS,
                                      pin_id_RxDone = config_lora.Controller.PIN_ID_FOR_LORA_DIO0)
print('lora', lora)
    

# LoRaDumpRegisters.dumpRegisters(lora)

while 1:

    if pir_flag==True and send_flag==True:
        #irq_state = machine.disable_irq()
        print("reading sensors")
        sgp_data = sgp.get_data()
        shtc_data = shtc.get_data()
        data_dict = sgp_data
        data_dict.update(shtc_data)
        #data_dict.update({'node_id':'3', 'node_name': 'sensor steht'})
        data_dict.update({'mac': uuid})
        print(data_dict)

        send(lora, json.dumps(data_dict))
        gc.collect()
        controller.show_text("sent: OK", x = 0, y = 0, clear_first=True)
        controller.show_text("MAC:"+uuid, x = 0, y = 8, clear_first=False)
        controller.show_text("T:" + str(round(shtc_data['T'],1)), x = 0, y = 16, clear_first=False)
        controller.show_text("RH:" + str(round(shtc_data['RH'],1)), x = 64, y = 16, clear_first=False)
        controller.show_text("Tv:"+str(sgp_data['SGP30_TVOC']), x = 0, y = 24, clear_first=False)
        controller.show_text("CO2eq:"+str(sgp_data['SGP30_CO2EQ']), x = 56, y = 24, clear_first=False)
        #controller.show_text_wrap("sent: OK     MAC:"+uuid+                "T:"+str(int(shtc_data['T']))+                " RH:"+str(int(shtc_data['RH']))+                "     TV:"+str(int(sgp_data['SGP30_TVOC']))+                " CO2EQ:"+str(int(sgp_data['SGP30_CO2EQ'])) )
        pir_flag=False
        send_flag=False
        #machine.enable_irq(irq_state)
