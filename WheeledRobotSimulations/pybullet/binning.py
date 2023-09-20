#%%
import numpy as np
import csv
import matplotlib.pyplot as plt

rows = []
with open('random-walk-pairs-room6-full.csv', 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)

data = np.array(rows).astype(float)
x_start = data[:,0]
y_start = data[:,1]
x_end   = data[:,2]
y_end   = data[:,3]
stepsz  = data[:,5]

#%%

# SET THESE PARAMETERS
nb = 5 # number of bins in each direction (assuming a square environment)
max_step = 2 # maximum step size

# SET THESE PARAMETERS

xedges = np.linspace(min(x_start),max(x_start),nb+1)
yedges = np.linspace(min(y_start),max(y_start),nb+1)

sz = (len(xedges)-1)*(len(xedges)-1)
matrix = np.zeros((sz,sz))

index = 0
for ix in range(len(xedges)-1):
    for iy in range(len(yedges)-1):
        # current_column_idx = int((len(yedges)-1)*ix + iy)
        bufferx, buffery = [], []
        for row in range(len(data)):
            if stepsz[row] <= max_step:
                if x_start[row] >= xedges[ix] and x_start[row] < xedges[ix+1]:
                    if y_start[row] >= yedges[iy] and y_start[row] < yedges[iy+1]:
                        bufferx.append(x_end[row])
                        buffery.append(y_end[row])
        H, __, __ = np.histogram2d(bufferx, buffery, bins=(xedges, yedges))
        H = H / sum(sum(H))
        # fig, ax = plt.subplots()
        # ax.pcolormesh(H)
        # ax.set_aspect('equal', 'box')
        # fig.tight_layout()
        # plt.show()
        matrix[:,index] = H.ravel(order='C')
        index += 1

np.savetxt('P_'+str(max_step)+'.csv', matrix, delimiter=',')

print()
print('Mean column sum: ', np.mean(np.sum(matrix, axis=0)))
print('Std of column sum: ', np.std(np.sum(matrix, axis=0)))
print('Mean row sum: ', np.mean(np.sum(matrix, axis=1)))
print('Std of row sum: ', np.std(np.sum(matrix, axis=1)))
print()

#%%
fig, ax = plt.subplots()
ax.pcolormesh(matrix)
ax.set_aspect('equal', 'box')
fig.tight_layout()
plt.show()

#%%
# Repeat but with matmul in order to visualize diffusion
P0 = np.copy(matrix)
for k in range(4):
    P0 = np.matmul(P0, matrix)

fig, ax = plt.subplots()
ax.pcolormesh(P0)
ax.set_aspect('equal', 'box')
fig.tight_layout()
plt.show()
