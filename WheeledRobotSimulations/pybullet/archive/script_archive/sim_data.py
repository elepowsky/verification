import numpy as np
import csv
import matplotlib.pyplot as plt

rows = []
with open('Sims/Room8/run_7.csv', 'r') as file:
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
ax.plot(x,y,color='black')
ax.set_aspect('equal', 'box')
fig.tight_layout()
plt.show()

for nb in [5,10,15,20]:
    xedges = np.linspace(-5,5,nb+1)
    yedges = np.linspace(-5,5,nb+1)
    H, __, __ = np.histogram2d(x, y, bins=(xedges, yedges))
    
    covered = np.zeros(np.shape(H))
    covered[H > 0] = 1
    
    fig, ax = plt.subplots()
    im = ax.pcolormesh(covered.T, cmap=plt.colormaps['binary'], vmin=0, vmax=1)
    ax.set_aspect('equal', 'box')
    fig.tight_layout()
    plt.show()
