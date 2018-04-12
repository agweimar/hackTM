from time import sleep
import machine

def send(lora):
    counter = 0
    print("LoRa Sender")

    while True:
        payload = '{0}'.format(counter)
        print("Sending packet: \n{}\n".format(payload))
        lora.println(payload) 
        
        counter += 1
        if counter > 255:
            counter = 0
        sleep(6)
        #machine.deepsleep(1000*10)
