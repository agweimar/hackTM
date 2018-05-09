# TODO software

eine config.py für alle relevanten sachen.

testcode für deepsleep -> lora send (möglicherweise problematisch)

testcode für lora (ping pong mit gateway?)

# TODO doc

# TODO hardware

# lobo firmware build

```bash
cd ~
git clone https://github.com/agweimar/hackTM.git
git clone https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo.git
cd ~/MicroPython_ESP32_psRAM_LoBo/MicroPython_BUILD
rm -rf components/internalfs_image/image/*
rm components/micropython/esp32/modules/ssd1306.py
ln -s ~/hackTM/micropython/dep/* components/internalfs_image/image/
ln -s ~/hackTM/micropython/skeleton/* components/internalfs_image/image/
./BUILD erase clean
./BUILD -j4 -v 
./BUILD makefs
./BUILD flash flashfs
```
[LoBo Instructions](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/build)

```bash
cp ~/MicroPython_ESP32_psRAM_LoBo/MicroPython_BUILD/build/bootloader/bootloader.bin ~/hackTM/micropython/LoBo-firmware/
cp ~/MicroPython_ESP32_psRAM_LoBo/MicroPython_BUILD/build/phy_init_data.bin ~/hackTM/micropython/LoBo-firmware/
cp ~/MicroPython_ESP32_psRAM_LoBo/MicroPython_BUILD/build/MicroPython.bin ~/hackTM/micropython/LoBo-firmware/
cp ~/MicroPython_ESP32_psRAM_LoBo/MicroPython_BUILD/build/partitions_mpy.bin ~/hackTM/micropython/LoBo-firmware/
cp ~/MicroPython_ESP32_psRAM_LoBo/MicroPython_BUILD/build/spiffs_image.img ~/hackTM/micropython/LoBo-firmware/

```



# Example Code  

## SGP30 and SHTC1
```python
#import the libraries
import SGP30, SHTC1
import i2c

#initialize i2c
scl_i2c = machine.Pin(22)
sda_i2c = machine.Pin(21)
freq_i2c = 100000

i2c = machine.I2C(scl = scl_i2c, sda = sda_i2c, freq=freq_i2c)

#initialize a SGP30 and SHTC1 object

sgp = SGP30.SGP30_Sensor(i2c)
shtc = SHTC1.SHTC1_Sensor(i2c)

#read out data in your main loop
while 1:

    print("reading sensors")
    sgp_data = sgp.get_data()
    shtc_data = shtc.get_data()
    data_dict = sgp_data
    data_dict.update(shtc_data)
    print(data_dict)
    sleep(10)
    
```
TODO sleep, soft reset

