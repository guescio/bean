#!/usr/bin/env python
#A script to print to screen the LightBlue Bean serial output.

import serial, time, sys

#create serial object to read from LightBlue Bean
ser = serial.Serial('/tmp/cu.LightBlue-Bean')#, timeout=10)

while True:
    try:
        #read line from serial output
        values = str(ser.readline().decode('utf-8')).strip()

        #print time stamp and serial output
        print(time.strftime('%Y%m%d%H%M%S'), values)

    except KeyboardInterrupt:
        print
        sys.exit(0)
