from time import sleep
from config_lora import uuid
import machine

def send(lora):
    counter = 0
    print("LoRa Sender")

    while True:
        payload = '{0},{1}'.format(uuid, counter)
        print("Sending packet: \n{}\n".format(payload))
        lora.println(payload) 
        
        counter += 1
        if counter > 255:
            counter = 0
        sleep(6)
        #machine.deepsleep(1000*10)
