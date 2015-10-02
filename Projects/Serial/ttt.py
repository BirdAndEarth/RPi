import serial

ser = serial.Serial("/dev/ttyAMA0",115200)

ser.write("\n")
ser.write("Hello World!  ----From Raspi!----")
ser.write("\n")

val = ""

while 1:
    val=ser.readline()
    print(val)
    f = open('tttt.txt', 'a')
    f.write(val)
    f.close()


