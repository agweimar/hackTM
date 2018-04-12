# coding: utf-8

import gc
import machine

import display_ssd1306_i2c
from time import sleep

#import network
#wlan = network.WLAN()
#wlan.active(True)

import SGP30, SHTC1



# oled vars
scl_oled = 15
sda_oled = 4
oled_width = 128
oled_height = 64
freq_oled = 400000

# i2c vars
scl_i2c = machine.Pin(22)
sda_i2c = machine.Pin(21)
freq_i2c = 100000

# PIR vars
pir_pin = machine.Pin(13, machine.Pin.IN)
# ???
pir_delay = 1


def reset_pin(pin, duration_low = 0.05, duration_high = 0.05):
    pin.value(0)
    sleep(duration_low)
    pin.value(1)
    sleep(duration_high)


# init OLED -- reset maybe not needed?!
prst = machine.Pin(16, machine.Pin.OUT)
reset_pin(prst)

display = display_ssd1306_i2c.Display(width = oled_width, height = oled_height, scl_pin_id = scl_oled, sda_pin_id = sda_oled, freq = freq_oled)

display.show_text("Display working!", x = 0, y = 10)

for k in range(3):
    i = 3-k
    display.show_text("starting test in", x = 0, y = 30, clear_first=False)
    display.show_text(str(i), x = k*10, y = 50, clear_first=False)
    sleep(1)

# init i2c
i2c = machine.I2C(scl = scl_i2c, sda = sda_i2c, freq=freq_i2c)
i2c_devices = i2c.scan()

# test
display.show_text("I2C Devices", x = 0, y = 5, clear_first=True)
display.show_text(str(i2c_devices), x = 0, y = 20, clear_first=False)

for k in range(3):
    i = 3-k
    display.show_text("sensor values in", x = 0, y = 40, clear_first=False)
    display.show_text(str(i), x = k*10, y = 50, clear_first=False)
    sleep(1)

# sensors

i2c = machine.I2C(scl = scl_i2c, sda = sda_i2c, freq=10000)

sgp = SGP30.SGP30_Sensor(i2c)
shtc = SHTC1.SHTC1_Sensor(i2c)

print("mem free: %d - mem alloc %d" % (gc.mem_free(), gc.mem_alloc()))
gc.collect()
print("mem free: %d - mem alloc %d" % (gc.mem_free(), gc.mem_alloc()))

dur = 0
while dur < 2:
    sgp_data = sgp.get_data()
    shtc_data = shtc.get_data()
    display.show_text("H2_raw: "+ str(sgp_data['SGP30_H2_RAW']), x = 0, y = 0, clear_first=True)
    display.show_text("EtOH_raw: "+str(sgp_data['SGP30_ETOH_RAW']), x = 0, y = 10, clear_first=False)
    display.show_text("Tvoc: "+str(sgp_data['SGP30_TVOC']), x = 0, y = 20, clear_first=False)
    display.show_text("CO2eq: "+str(sgp_data['SGP30_CO2EQ']), x = 0, y = 30, clear_first=False)
    display.show_text("T[C] " + str(shtc_data[0]), x = 0, y = 40, clear_first=False)
    display.show_text("RH " + str(shtc_data[1]), x = 0, y = 50, clear_first=False)
    sleep(3)
    dur += 1

print("mem free: %d - mem alloc %d" % (gc.mem_free(), gc.mem_alloc()))
gc.collect()
print("mem free: %d - mem alloc %d" % (gc.mem_free(), gc.mem_alloc()))

# Lora Connectivity Test
# todo


# PIR test
# todo
while True:
    if pir_pin.value():
        display.show_text("Motion detected", x = 0, y = 0, clear_first = True)
    else:
        display.show_text("No", x = 30, y = 0, clear_first = True)
        display.show_text("motion detected", x = 0, y = 10, clear_first = False)
    sleep(pir_delay)


# optional test code (bluetooth wifi etc)
