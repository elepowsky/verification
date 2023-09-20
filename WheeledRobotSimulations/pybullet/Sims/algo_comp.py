import numpy as np
import csv
import matplotlib.pyplot as plt

def readdata(folder, filename, datatype):
    rows = []
    with open(folder + filename + '.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    data = np.array(rows).astype('float')
    if datatype == 1:
        steps = data[:,3]
    else:
        steps = data[:,1]
    pdf = np.histogram(steps/10, bins=np.linspace(0, 1, 101))[0]
    cdf = np.cumsum(pdf)
    cdf = cdf / max(cdf)
    return cdf

#%%
folder = ''

empty_nosource_algo = readdata(folder, 'Room6_step10_source0_data_run1', 1)

empty_nosource_comp = readdata(folder, 'Room6_step10_source0_step_run1', 2)

empty_source_algo = readdata(folder, 'Room6_step10_source100_data_run1', 1)

empty_source_comp = readdata(folder, 'Room6_step10_source100_step_run1', 2)

obs_nosource_algo = readdata(folder, 'Room51_step10_source0_data_run1', 1)

obs_nosource_comp = readdata(folder, 'Room51_step10_source0_step_run1', 2)

obs_source_algo = readdata(folder, 'Room51_step10_source100_data_run1', 1)

obs_source_comp = readdata(folder, 'Room51_step10_source100_step_run1', 2)

#%%
x = np.linspace(0, 1, 100)

plt.figure(figsize=(4,2))
plt.grid(c='black',zorder=20,which='both', axis='both', alpha=0.2)
plt.plot(x,empty_nosource_algo,   color=[0,0,0],   linestyle='-',  label='Empty',    zorder=2)
plt.plot(x,empty_source_algo,     color=[0,0.7,0.2], linestyle='-',  label='Source',   zorder=1)
plt.plot(x,obs_nosource_algo,     color=[0,0,0],   linestyle='--', label='Obstacles',zorder=3)
plt.plot(x,obs_source_algo,     color=[0,0.7,0.2],   linestyle='--', label='Obstacles, Source',zorder=3)
#plt.legend(loc='lower right', ncol=1, fontsize=9, columnspacing=1)
plt.xlim((-0.015,1.015))
plt.ylim((-0.05,1.05))
plt.xticks([0.0,0.2,0.4,0.6,0.8,1.0], fontsize=9)
plt.yticks([0.0,0.25,0.50,0.75,1.0], fontsize=9)
plt.xlabel('Normalized Step Size', fontsize=10)
plt.ylabel('CDF', fontsize=10)
plt.title('Distance Between Measurements', fontsize=10)
plt.tight_layout()
plt.savefig('cdf_measurements_rev2.png', dpi=300)

plt.figure(figsize=(4,2))
plt.grid(c='black',zorder=20,which='both', axis='both', alpha=0.2)
plt.plot(x,empty_nosource_comp,   color=[0,0,0],   linestyle='-',  label='Empty',    zorder=2)
plt.plot(x,empty_source_comp,     color=[0,0.7,0.2], linestyle='-',  label='Source',   zorder=1)
plt.plot(x,obs_nosource_comp,     color=[0,0,0],   linestyle='--', label='Obstacles',zorder=3)
plt.plot(x,obs_source_comp,     color=[0,0.7,0.2],   linestyle='--', label='Obstacles, Source',zorder=3)
plt.legend(loc='lower right', ncol=1, fontsize=9, columnspacing=1)
plt.xlim((-0.015,1.015))
plt.ylim((-0.05,1.05))
plt.xticks([0.0,0.2,0.4,0.6,0.8,1.0], fontsize=9)
plt.yticks([0.0,0.25,0.50,0.75,1.0], fontsize=9)
plt.xlabel('Normalized Step Size', fontsize=10)
plt.ylabel('CDF', fontsize=10)
plt.title('Distance Between Turns', fontsize=10)
plt.tight_layout()
plt.savefig('cdf_turns_rev2.png', dpi=300)
