import machine

#GPIOs:
#    0 -> Pin 36
#    1 -> Pin 37
#    2 -> Pin 38
#    3 -> Pin 39

uart_rx = 22
uart_tx = 21

uart = machine.UART(1, rx=uart_rx, tx=uart_tx)

s = ''
while True:

    inp = uart.read()
    if inp != None:
    	s += inp.decode()
    if s.endswith('\r'):
        print(s)
        s=''


