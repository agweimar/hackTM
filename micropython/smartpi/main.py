import gc
import machine
from time import sleep

import sx127x
import config_sensorboard

#GPIOs (all input):
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

        if len(data) == 3 and list(data.values()) != ['','','']:
            payload = controller.assemble_payload(data)
            controller.show_text("1: "+ str(list(data.values()[0])), x = 0, y = 0, clear_first = True)
            controller.show_text("2: "+ str(list(data.values()[0])), x = 0, y = 8, clear_first = True)
            controller.show_text("3: "+ str(list(data.values()[0])), x = 0, y = 16, clear_first = True)
            controller.lora_send(lora, payload)
            data={}
            print (data)
        else:
            print("No Data")
            controller.show_text("No Data", x = 0, y = 0, clear_first = True)
    sleep(3)
