import time
import machine
import ubinascii 

from controller_sensorboard import Controller

SOFT_SPI = True
IS_ESP32 = True
IS_MICROPYTHON = True

def mac2eui(mac):
    mac = mac[0:6] + 'fffe' + mac[6:] 
    return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:] 
    
# millisecond
millisecond = time.ticks_ms

# Node Name
UUID = ubinascii.hexlify(machine.unique_id()).decode()  
    
NODE_NAME = 'SensorBoard_' + UUID

     
