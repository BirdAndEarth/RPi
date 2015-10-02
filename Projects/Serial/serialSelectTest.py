#
# serial port select program for Raspberry pi.
# 2014/12/8 shiu

import serial
import sys
import os, os.path
import commands
import time

RESET_DELAY = 3 # in sec

serialPorts = []
serialPortsExists = []
try:
    serialPorts = commands.getoutput('ls /dev/ttyAC*').split('\n')
except Exception, e:
    print(e)

# try:
#     #serialPorts += commands.getoutput('ls /dev/ttyUSB*').split('\n')
# except Exception, e:
#     print(e)

for serialport in serialPorts:
    try:
        sys.stdout.write('cheking: ' + serialport + '\t')

        ser = serial.Serial(serialport, 115200, timeout = 0.1)
        time.sleep(RESET_DELAY)
        ser.write('?\n')
        s = ser.readline()
        serialPortsExists.append(s)
        ser.close()
        print(s)

    except Exception, e:
        print(e)
        serialPortsExists.append('0')
        ser.close()

#print(serialPortsExists)
#print(serialPorts)


for serialPortsExist in serialPortsExists:
    if "Da" in serialPortsExist:
        print('reset')
        print(serialPortsExist)
        ser = serial.Serial(serialPorts[serialPortsExists.index(serialPortsExist)], 1200, timeout = 0.1)
        ser.close()


# for i in range(0, len(serialPortsExists)):
#     if serialPortsExists[i] == "Davinci32U-002":
#         print('reset DaVinci32U-002')
#         ser = serial.Serial(serialPorts[i], 1200, timeout = 0.1)
#         time.sleep(0.3)
#         ser.close()




