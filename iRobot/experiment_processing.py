import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.stats import kstest

filename = 'log_files/F_Video/log_20230919_step_200_trial04.txt'

with open(filename) as file_in:
    lines = []
    for line in file_in:
        lines.append(line)

steps = []
for line in lines:
    if line[0:6] == 'Next S':
        steps.append(float(line[11:]))
        
print(len(steps))

#%%

plt.figure()
plt.plot(steps)
plt.axhline(100,color='black')
plt.axhline(10,color='black')
plt.axhline(0,color='black')
plt.axhline(np.mean(steps),color='red')
plt.title('Step Size')

pdf = np.histogram(steps, bins=np.linspace(0, 200, 101))[0]
cdf = np.cumsum(pdf)
cdf = cdf / max(cdf)

plt.figure()
plt.plot(np.linspace(0, 1, 100), cdf)
plt.title('CDF')
plt.grid('on')

steps_copy = np.array(steps)/200

#%%

if 'ref' in locals():
    pass
else:
    rows = []
    with open('ref_dist.csv', 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    ref = np.array(rows).astype('float')

#%%
for i_s in np.arange(0, len(steps_copy)+1, 20):
    try:
        result_ks = kstest(steps_copy[:i_s].reshape((-1,1)).squeeze(),ref.squeeze())
        print(result_ks.pvalue)
    except KeyboardInterrupt:
        break
    except:
        continue
    
    if result_ks.pvalue > 0:
        if np.log10(result_ks.pvalue) < np.log10(0.005/50):
            print('TRIGGER HERE: ', i_s)
            # break
