#
# serial port select program for Raspberry pi.
# 2014/12/8 shiu

import serial
import sys
import os, os.path
import commands
import time

RESET_DELAY = 3 # in sec
NAME = 's:'

def main():
    # check TowerDetector ports
    PortPath = SerialPortPath('?:TowerDetector1.0')

    # if exits, reset the port
    if PortPath == '':
        print ('There is no ' + 'TowerDetector1.0')
        sys.exit()
    else :
        resetDevice(PortPath)
    try:
        ser = serial.Serial(PortPath, 115200, timeout = 0.1)
    except Exception, e:
        ser.close()
        print('cant open ... /t bye!')
        sys.exit()


    ser.write('n\n')
    print('Normal mode START')


    while (True):
        val=ser.readline()
        sys.stdout.write(val)






# Get serial port path
def SerialPortPath(deviceName):

    serialPorts = []
    serialPortsExists = []

    try:
        serialPorts = commands.getoutput('ls /dev/ttyAC*').split('\n')
    except Exception, e:
        print(NAME + 'no /dev/ttyAC*')
    # try:
    #     serialPorts += commands.getoutput('ls /dev/ttyUSB*').split('\n')
    # except Exceptio, e:
    #     print(NAME & 'no /dev/ttyUSB*')

    for serialport in serialPorts:
        try:
            sys.stdout.write('cheking: ' + serialport + '\t')

            ser = serial.Serial(serialport, 115200, timeout = 0.1)

            # wait for the device restart
            time.sleep(RESET_DELAY)
            ser.write('w\r')
            time.sleep(1)
            ser.write('w\n')
            time.sleep(1)
            ser.write('w\r')
            time.sleep(1)
            ser.write('w\n')
            time.sleep(1)
            ser.write('?\r\n')
            s = ser.readline()
            serialPortsExists.append(s)
            ser.close()
            print(s)

        except Exception, e:
            serialPortsExists.append('0')
            # ser.close()
            return 'no device'

    portPath = ''

    for serialPortsExist in serialPortsExists:
        if deviceName in serialPortsExist:
            portPath = str(serialPorts[serialPortsExists.index(serialPortsExist)])
            # ser = serial.Serial(portPath, 1200, timeout = 0.1)
            # ser.close()
            # print ('serialPortsExist' + portPath)
    return portPath

# Reset Device
def resetDevice(DevicePort):
    try:
        print('reseting ' + DevicePort + '...')
        p = serial.Serial(DevicePort, 1200, timeout = 0.1)
        p.close()
        time.sleep(10)

        # p = serial.Serial(DevicePort, 115200, timeout = 0.1)
        # p.close()

        # time.sleep(10)
        print(DevicePort + ' rebooted. ')

    except Exception, e:
        return False

    return True


if __name__ == '__main__':
    main()


