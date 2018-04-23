#!/bin/bash
cd firmware
esptool.py --chip esp32 --baud 576000 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20180409-v1.9.3-521-gd6cf5c67.bin

sleep 5

ampy -b 115200 -p /dev/ttyUSB0 reset

cd ../test_board
for i in $(ls)
do 
	ampy -b 115200 -p /dev/ttyUSB0 put $i
	echo $i "transferred"
done

ampy -b 115200 -p /dev/ttyUSB0 reset

echo "Finished"
