import socket
import time
import datetime
import numpy as np
import sys

# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import time
import csv
import numpy as np

import math
import statistics as stat
import pandas as pd
from scipy.optimize import curve_fit

PYTHONUNBUFFERED = True

# ----------------------------------------------------------------------

# DETECTOR-SPECIFIC CODE OMITTED

# ----------------------------------------------------------------------

while True:
    
    try:
        
        server = '##:##:##:##:##:##'
        port = 7

        size = 1024
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.connect((server,port))
        print(f'Connected to {server}:{port}')
        
        break
        
    except:
        
        continue

while True:
    
    data = s.recv(size)
    if data:
        
        data = data.decode().strip()
        print(data)
        if data == 'quit':
            break
        
        elif data == 'connect':
            # DETECTOR-SPECIFIC CODE OMITTED
            s.send(bytes('Connected','UTF-8'))
        
        elif data == 'on':
            # DETECTOR-SPECIFIC CODE OMITTED
            s.send(bytes('HV on','UTF-8'))
            
        elif data == 'off':
            # DETECTOR-SPECIFIC CODE OMITTED
            s.send(bytes('HV off','UTF-8'))
            
        elif data.isdigit():
            spec = np.zeros(2048,)
            for i in range(int(data)):
                print(i)
                # DETECTOR-SPECIFIC CODE OMITTED
            message = str(int(sum(spec)))
            s.send(bytes(message,'UTF-8'))
            
        else:
            message = str(datetime.datetime.now())
            s.send(bytes(message,'UTF-8'))

print('Closing socket')
s.close()
HVoff()

