#!/bin/bash
for i in $(ls *.py)
do 
	ampy -b 115200 -p /dev/ttyUSB0 put $i;
	echo $i;
done
