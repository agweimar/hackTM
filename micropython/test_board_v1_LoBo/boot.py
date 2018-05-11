# This file is executed on every boot (including wake-boot from deepsleep)

# import esp
# esp.osdebug(None)

# import webrepl
# webrepl.start()

# import gc
# gc.collect()
import machine
Pin_0 = machine.Pin(0)
Pin_0.init(mode = machine.Pin.IN, pull = machine.Pin.PULL_UP)
rtc = machine.RTC()
rtc.wake_on_ext0(Pin_0,0)
print('wake reason: ' + str(machine.wake_reason()))
if (machine.wake_reason() != (3,1)):
    print('going to sleep')
    machine.deepsleep(0)
print('running main.py')


