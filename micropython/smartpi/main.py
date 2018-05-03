import gc
import machine
from time import sleep

import sx127x
import config_sensorboard

#GPIOs:
#    0 -> Pin 36
#    1 -> Pin 37
#    2 -> Pin 38
#    3 -> Pin 39

uart_rx = 12
uart_tx = 13

uart = machine.UART(1, rx=uart_rx, tx=uart_tx)

controller = config_sensorboard.Controller()
lora = controller.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                      pin_id_ss = config_sensorboard.Controller.PIN_ID_FOR_LORA_SS,
                                      pin_id_RxDone = config_sensorboard.Controller.PIN_ID_FOR_LORA_DIO0)
data = {}

while True:

    for i in range(3):
        uart.write(str(i+1) + "\r\n")
        sleep(0.3)
        rec = uart.read()

        if rec != None:
            value = rec.decode()[:-2]
            data[i] = value
        else:
            print('No Data from Raspi')

        if len(data) == 3:
            payload = controller.assemble_payload(data)
            controller.lora_send(lora, payload)
            data={}
    sleep(3)
