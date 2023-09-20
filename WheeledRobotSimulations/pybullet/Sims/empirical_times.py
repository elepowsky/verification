import numpy as np
import csv
import matplotlib.pyplot as plt

def readdata(filename, folder='Times/'):
    rows = []
    with open(folder + filename + '.csv', 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    data = np.array(rows).astype('float')
    return data

means = np.empty((3,5,10))
maxes = np.empty((3,5,10))

for room in np.arange(1,11):
    data = readdata('Room'+str(room)+'_Tmean')
    means[:,:,room-1] = data[:,:]
    data = readdata('Room'+str(room)+'_Tmax')
    maxes[:,:,room-1] = data[:,:]

emp_mean = np.mean(means, axis=2)
emp_max  = np.max(maxes, axis=2)

# means5 = np.empty((1,5,10))
# maxes5 = np.empty((1,5,10))

# for room in np.arange(1,11):
#     if room != 5:
#         data = readdata('Room'+str(room)+'_Tmean')
#         means5[:,:,room-1] = data[0,:]
#         data = readdata('Room'+str(room)+'_Tmax')
#         maxes5[:,:,room-1] = data[0,:]

# emp_mean5 = np.mean(means5, axis=2)
# emp_max5  = np.max(maxes5, axis=2)

