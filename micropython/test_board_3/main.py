# coding: utf-8

import gc
import machine

from time import sleep

import SGP30, SHTC1

import sx127x
import config_lora 
from config_lora import uuid

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

    print("reading sensors")
    sgp_data = sgp.get_data()
    shtc_data = shtc.get_data()
    data_dict = sgp_data
    data_dict.update(shtc_data)
    data_dict.update({'node_id':'2', 'node_name': 'wenig_schlitz'})
    print(data_dict)
    send(lora, data_dict)
    gc.collect()
    sleep(10)
