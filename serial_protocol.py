import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.timeout =1
print(ser.name)

while True:
    i = input('type here: ').strip()
    ser.write(i.encode())
    time.sleep(0.1)
    print(ser.readline())

ser.close()
