import serial
import time
import numpy as np

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM5', 115200, timeout=1)

time.sleep(2)

total = np.zeros(3,)
# while True:
for i in range(60):
    time.sleep(1)
    line = ser.readline()   # read a byte
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        words = string.split(',')
        counts = np.array([int(word) for word in words])
        total += counts
        print(counts)
        # ser.flushInput()

print(sum(total)/60/3)

ser.close()
