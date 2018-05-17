import time
import machine
import ubinascii 

from controller_sensorboard import Controller

SOFT_SPI = True
IS_ESP32 = True
IS_MICROPYTHON = True

# millisecond
millisecond = time.ticks_ms

# Node Name
UUID = ubinascii.hexlify(machine.unique_id()).decode()  
NODE_NAME = 'SensorBoard_' + UUID
    

     
offline_flag = True

def pir_callback(p):
    global pir_flag
    #print('PIR triggered')
    pir_flag=True

def timer_callback(timer):
    global send_flag
    #print('timer isr')
    send_flag=True
