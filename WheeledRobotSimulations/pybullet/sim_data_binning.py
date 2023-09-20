import numpy as np
import csv
import matplotlib.pyplot as plt

#Sims/Room'+self.room_number_str+'/step'+str(int(self._max_step))+'_run'

rows = []
with open('Sims/Room6/step2_run1.csv', 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)

data = np.array(rows).astype(float)
iteration = data[:,0]
x         = data[:,1]
y         = data[:,2]
steps     = data[:,3]
counts    = data[:,4]

fig, ax = plt.subplots()
ax.plot(x[:3000],y[:3000],color='black')
ax.set_aspect('equal', 'box')
fig.tight_layout()
plt.show()

# for nb in [5,10,20]:
#     xedges = np.linspace(-4.95,4.95,nb+1)
#     yedges = np.linspace(-4.95,4.95,nb+1)
#     H, __, __ = np.histogram2d(x, y, bins=(xedges, yedges))
    
    
#     # rows = []
#     # with open('PData/Room3/badIdx_bins'+str(nb)+'_copy.csv', 'r') as file:
#     #     csvreader = csv.reader(file)
#     #     for row in csvreader:
#     #         rows.append(row)
#     # badIdx = np.array(rows)[:,-1].astype('float').astype('int')
#     badIdx = []
    
#     H_temp = H.ravel()
#     H_temp[badIdx] = 0
#     H = H_temp.reshape(np.shape(H))
    
#     covered = np.zeros(np.shape(H))
#     covered[H > 0] = 1
    
#     fig, ax = plt.subplots()
#     im = ax.pcolormesh(covered.T, cmap=plt.colormaps['binary'], vmin=0, vmax=1)
#     ax.set_aspect('equal', 'box')
#     fig.tight_layout()
#     plt.show()
