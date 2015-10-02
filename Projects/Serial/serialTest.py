import serial
import time

def main():

    ser=serial.Serial('/dev/ttyACM0', 9600, timeout=10)
    while 1:
        str1 = ser.readline()
        print(str1)
if __name__ == '__main__':
    main()


