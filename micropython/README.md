# What's in this directory?

```
.
+-- upload_to_board.sh	- script for uploading all *.py files from currect directory to esp32
+-- LoBo-firmware	- working LoBo MicroPython firmware for our boards
|   +-- flash_board.sh	- bash script for flashing the firmware
|   +-- ...
+-- dep			- dependencies/drivers for our sensorboard which you probably won't need to change
|   +-- ...
+-- skeleton		- this is where you want to start developing your application
|   +-- ...
+-- archived
|   +-- continental	- continental test drive data
|   +-- drone		- drone flight data
|   +-- VEML		- working test code for VEML6040 
|   +-- sx1276_wei1234	- sx1276 driver examples written by "Wei1234c"
|   +-- ...
|   +-- old		- really old
|   |   +-- ...
```

## HOWTO: build LoBo firmware

[LoBo Instructions/dependencies](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/build)

```bash
cd ~
git clone https://github.com/agweimar/hackTM.git
git clone https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo.git
cd ~/MicroPython_ESP32_psRAM_LoBo/MicroPython_BUILD
```
remove example files from the internalfs image directory and the ssd1306 driver
```bash
rm -rf components/internalfs_image/image/*
rm components/micropython/esp32/modules/ssd1306.py
```
(optional) link the micropython files to the internalfs image
```bash
ln -s ~/hackTM/micropython/dep/* components/internalfs_image/image/
ln -s ~/hackTM/micropython/skeleton/* components/internalfs_image/image/
```
since the ssd1306 uses the framebuffer module you have to enable it first
```bash
./BUILD.sh menuconfig
```
Make sure your console is at least 19 lines by 80 columns, otherwise this will fail without any message.

go to:

MicroPython -> Modules -> [\*] Enable framebuffer 

Then build the firmware and the fs image

```bash
./BUILD.sh -j4 -v 
./BUILD.sh makefs
```

erase your flash to make sure everything is nice and clean

```bash
./BUILD.sh erase
```
then flash the firmware and fs image

```bash
./BUILD.sh flash flashfs
```

Note:

building/flashing the fs image is optional, you can also just use adafruit-ampy

to upload the mycropython files to your board

## TODO software

use config_sensorboard.py more extensively

## TODO doc

code documentation (doxygen?)

