import numpy as np
import csv
import matplotlib.pyplot as plt

#%%
rows = []
with open('log_files/F_Video/Config8_Maxstep2_trial2_source.csv', 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row)
        
data = np.array(rows).astype('float')[1:,:]

xmin = min(data[:,0])
xmax = max(data[:,0])
ymin = min(data[:,1])
ymax = max(data[:,1])

xmin = min(xmin,-3)
xmax = max(xmax,1)
ymin = min(ymin,6)
ymax = max(ymax,11)

data = data[:]

print('x range: '+str(xmin)+' : '+str(xmax))
print('x width: '+str(xmax-xmin))
print('y range: '+str(ymin)+' : '+str(ymax))
print('y width: '+str(ymax-ymin))

xedges = np.linspace(xmin,xmax,5)
yedges = np.linspace(ymin,ymax,6)

H, __, __ = np.histogram2d(data[:,0], data[:,1], bins=(xedges,yedges))

covered = np.zeros(np.shape(H))
covered[H > 0] = 1

coverage = sum(sum(covered))/18
print(coverage)

fig, ax = plt.subplots()
im = ax.pcolormesh(covered.T, cmap=plt.colormaps['binary'], vmin=0, vmax=1)
ax.set_aspect('equal', 'box')
# plt.scatter((data[:,0]-xmin)/(xmax-xmin)*4, (data[:,1]-ymin)/(ymax-ymin)*4)
fig.tight_layout()
plt.show()
