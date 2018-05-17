# What's in this directory?

```
.
+-- upload_to_board.sh 
+-- LoBo-firmware
|   +-- flash_board.sh
|   +-- ...
+-- dep
|   +-- ...
+-- skeleton
|   +-- ...
|   +-- ...
+-- archived
|   +-- continental
|   +-- drone
|   +-- VEML
|   +-- sx1276_wei1234
|   +-- ...
|   +-- old
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

