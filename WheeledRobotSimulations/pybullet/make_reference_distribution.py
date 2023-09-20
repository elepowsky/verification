import numpy as np
import csv
import matplotlib.pyplot as plt

#%%
folder = 'Sims/Trials-NoSource'

for room_num in [6]:
    
    steps = np.empty((0,))
    
    for step_size in [2,4,6,8,10]:
                
        for trial in np.arange(1,5):
    
            rows = []
            with open(folder+'/Room'+str(room_num)+'/step'+str(step_size)+'_run'+str(trial)+'.csv', 'r') as file:
                csvreader = csv.reader(file)
                header = next(csvreader)
                for row in csvreader:
                    rows.append(row)
            
            data = np.array(rows).astype(float)
            steps = np.concatenate((steps, data[:,3]/step_size), axis=0)

np.savetxt('ref_dist.csv',steps,delimiter=',')

#%%
pdf = np.histogram(steps, bins=np.linspace(0, 1, 101))[0]

plt.figure()
plt.plot(np.linspace(0, 1, 100), pdf)
plt.title('PDF')

cdf = np.cumsum(pdf)
cdf = cdf / max(cdf)

plt.figure()
plt.plot(np.linspace(0, 1, 100), cdf)
plt.title('CDF')
