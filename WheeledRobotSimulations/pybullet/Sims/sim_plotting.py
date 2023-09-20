import numpy as np
import csv
import matplotlib.pyplot as plt

#%%
filename = 'Trials-NoSource\Coverage\Full_Data_bins10.csv'

rows = []
with open(filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row)
coverage = np.array(rows).astype('float')
coverage_mean = np.mean(coverage, axis=1)
coverage_max = np.max(coverage, axis=1)
coverage_min = np.min(coverage, axis=1)
coverage_std = np.std(coverage, axis=1)

#%%
filename = 'Trials-NoSource/KS/Full_Data21.csv'

rows = []
with open(filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row)
temp1 = np.array(rows).astype('float')

filename = 'Trials-NoSource/KS/Full_Data31.csv'

rows = []
with open(filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row)
temp2 = np.array(rows).astype('float')

filename = 'Trials-NoSource/KS/Full_Data41.csv'

rows = []
with open(filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row)
temp3 = np.array(rows).astype('float')

KS_nosource = np.concatenate((temp1, temp2, temp3), axis=1)
KS_nosource_mean = np.concatenate(([0],np.mean(KS_nosource, axis=1)), axis=0)
KS_nosource_max = np.concatenate(([0],np.max(KS_nosource, axis=1)), axis=0)
KS_nosource_min = np.concatenate(([0],np.min(KS_nosource, axis=1)), axis=0)
KS_nosource_std = np.concatenate(([0],np.std(KS_nosource, axis=1)), axis=0)

#%%
filename = 'Trials-Source100/KS/Full_Data.csv'

rows = []
with open(filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row)
KS = np.array(rows).astype('float')
KS_mean = np.concatenate(([0],np.mean(KS, axis=1)), axis=0)
KS_max = np.concatenate(([0],np.max(KS, axis=1)), axis=0)
KS_min = np.concatenate(([0],np.min(KS, axis=1)), axis=0)
KS_std = np.concatenate(([0],np.std(KS, axis=1)), axis=0)

#%%
x_KS = np.arange(0,50001,100)
x_coverage = np.arange(0,50000,10)

fig, ax1 = plt.subplots(figsize=(4,4/1.54))

ax1.grid(axis='both', color='black', alpha=0.1)

# ax1.fill_between(x_KS,
#                  KS_min,
#                  KS_max,
#                  color='blue',alpha=0.1)
LB = KS_mean-KS_std
LB[LB<-5] = -5
ax1.fill_between(x_KS[1:],
                 LB[1:],
                 KS_mean[1:]+KS_std[1:],
                 color='black',alpha=0.2)
ax1.plot(x_KS[1:],KS_mean[1:],color='black',linewidth=2,linestyle='--',label='Source')

# ax1.fill_between(x_KS,
#                  KS_nosource_min,
#                  KS_nosource_max,
#                  color='black',alpha=0.1)
UB = KS_nosource_mean+KS_nosource_std
UB[UB>0] = 0
ax1.fill_between(x_KS[1:],
                 KS_nosource_mean[1:]-KS_nosource_std[1:],
                 UB[1:],
                 color='black',alpha=0.2)
ax1.plot(x_KS[1:],KS_nosource_mean[1:],color='black',linewidth=2,label='Absence')

ax1.set_xscale('log')

ax2 = ax1.twinx()

UB = coverage_mean+coverage_std
UB[UB>1] = 1
ax2.fill_between(x_coverage[1:],
                 coverage_mean[1:]-coverage_std[1:],
                 UB[1:],
                 color=[0,0.7,0.2],alpha=0.2)
ax2.plot(x_coverage,coverage_mean,color=[0,0.7,0.2],linewidth=2)

ax1.set_xlim((90,11000))
ax1.set_ylim((-5.2,0.2))
ax2.set_ylim((-0.04,1.04))

ax1.set_xlabel('Step Number', fontsize=10)
ax1.set_ylabel('Log Significance', fontsize=10)
ax2.set_ylabel('Fraction Covered', color=[0,0.6,0.2])
ax2.tick_params(axis='y', labelcolor=[0,0.6,0.2])
ax1.legend()

plt.tight_layout()
plt.savefig('Simulation_Rev2.pdf', dpi=300)
