### howto flash board
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 --before default_reset --after no_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 bootloader.bin 0xf000 phy_init_data.bin 0x10000 MicroPython.bin 0x8000 partitions_mpy.bin

- do a hard reset of you board by pressing the RST pushbutton

esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 --before default_reset --after no_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x150000 spiffs_image.img

- hard reset again --- and you should be up and running

sdkconfig:
- copied from firmware build directory

