import numpy as np
import csv
import math
import matplotlib.pyplot as plt

bins = 3
step_num = 5
rooms = 10
times = 5000

mins = np.zeros((5,5000,10))
maxs = np.zeros((5,5000,10))
means = np.zeros((5,5000,10))

folder = 'Coverage/'

for n, room_num in enumerate(np.arange(1,11)): #np.arange(1,11):
    for i_s, step_size in enumerate([2,4,6,8,10]):
        rows = []
        with open(folder+'Room'+str(room_num)+'_steps'+str(step_size)+'_Tmin.csv', 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                rows.append(row)
        data = np.array(rows)
        mins[i_s,:,n] = data[0,:]
        rows = []
        with open(folder+'Room'+str(room_num)+'_steps'+str(step_size)+'_Tmax.csv', 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                rows.append(row)
        data = np.array(rows)
        maxs[i_s,:,n] = data[0,:]
        rows = []
        with open(folder+'Room'+str(room_num)+'_steps'+str(step_size)+'_Tmean.csv', 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                rows.append(row)
        data = np.array(rows)
        means[i_s,:,n] = data[0,:]

temp = np.sum(np.sum(mins, axis=2),axis=0)
max_it = int(math.ceil((list(x == 50 for x in temp).index(True)/ 1000.0)) * 1000)

x = 0 + np.arange(max_it)*10

# plt.figure()
# colors = plt.cm.plasma(np.linspace(0,1,rooms))
# for room_num in np.arange(1,11):
#     for i_s, step_size in enumerate([2,4,6,8,10]):
#         plt.plot(x,mins[i_s,:max_it,room_num-1],color=colors[room_num-1])
#         plt.plot(x,maxs[i_s,:max_it,room_num-1],color=colors[room_num-1])
# plt.xscale('log')

# mins_plt = np.min(mins,axis=0)
# maxs_plt = np.max(maxs,axis=0)

# plt.figure(figsize=(4,3))
# plt.grid(c='black',zorder=20,which='major',axis='both', alpha=0.2)
# colors = plt.cm.viridis(np.linspace(0,1,rooms))
# for room_num in np.arange(1,11):
#     plt.fill_between(x,mins_plt[:max_it,room_num-1],
#                      maxs_plt[:max_it,room_num-1],
#                      color=colors[room_num-1],alpha=0.1)
#     plt.plot(x,mins_plt[:max_it,room_num-1],color=colors[room_num-1],label='Room '+str(room_num))
# plt.xscale('log')
# # plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.7),
# #            ncol=4, fontsize=8, columnspacing=1)
# plt.xlim((10,10000))
# plt.ylim((-0.05,1.05))
# plt.xlabel('Iteration', fontsize=10)
# plt.ylabel('Fraction Covered', fontsize=10)
# plt.title('Empirical Coverage vs. Time', fontsize=10)
# plt.tight_layout()
# # plt.savefig('cdf_turns.png', dpi=300)


mins_plt = np.min(mins,axis=2)
maxs_plt = np.max(maxs,axis=2)
means_plt = np.mean(means,axis=2)

def convert(steps,max_step):
    times = steps*(3 + max_step*100/2/10) / 60
    return times

xs = np.zeros((5,len(x)))

for i_s, step_size in enumerate([2,4,6,8,10]):
    xs[i_s,:] = convert(x, step_size)

#%%

temp_x = xs.flatten().reshape(-1,1)
temp_min = mins_plt[:,:max_it].flatten().reshape(-1,1)
temp_max = maxs_plt[:,:max_it].flatten().reshape(-1,1)

temp_min = np.concatenate((temp_x,temp_min), axis=1)
temp_max = np.concatenate((temp_x,temp_max), axis=1)

temp_min = temp_min[temp_min[:, 0].argsort()]
temp_max = temp_max[temp_max[:, 0].argsort()]

# xmax = [[temp_max[0,0],temp_max[0,1]]]
# for row in temp_max[:-1,:]:
#     if row[1] > xmax[-1][1]:
#         xmax.append([row[0],row[1]])
# xmax.append([temp_max[-1,0],temp_max[-1,1]])
# xmax = np.array(xmax)

# xmin = [[temp_min[-1,0],temp_min[-1,1]]]
# for row in np.flipud(temp_min[:-1,:]):
#     if row[1] < xmin[-1][1]:
#         xmin.append([row[0],row[1]])
# xmin.append([temp_min[0,0],temp_min[0,1]])
# xmin = np.flipud(np.array(xmin))

x = np.linspace(0.9,1100,10000)
# ymin = np.interp(x, xmin[:,0], xmin[:,1])
# ymax = np.interp(x, xmax[:,0], xmax[:,1])

mins_interp = np.zeros((5,10000))
for i, row in enumerate(mins_plt):
    mins_interp[i,:] = np.interp(x, xs[i,:], row[:max_it])

mins_i = np.min(mins_interp,axis=0)

maxs_interp = np.zeros((5,10000))
for i, row in enumerate(maxs_plt):
    maxs_interp[i,:] = np.interp(x, xs[i,:], row[:max_it])

maxs_i = np.max(maxs_interp,axis=0)

plt.figure()
plt.plot(temp_min[:,0], temp_min[:,1])
plt.plot(temp_max[:,0], temp_max[:,1])
# plt.plot(xmin[:,0], xmin[:,1])
# plt.plot(xmax[:,0], xmax[:,1])
# plt.plot(x,ymin)
# plt.plot(x,ymax)
plt.plot(x,mins_i)
plt.plot(x,maxs_i)
plt.xscale('log')
plt.xlim((0.9,1100))

#%%
plt.figure(figsize=(4,4/1.54))
plt.grid(c='black',zorder=20,which='major',axis='both', alpha=0.2)

# plt.plot(xmin[:,0], xmin[:,1],color='black')
# plt.plot(xmax[:,0], xmax[:,1],color='black')

plt.fill_between(x,
                 mins_i,
                 maxs_i,
                 color='black',alpha=0.2)

colors = plt.cm.viridis(np.linspace(0,1,step_num))
for i_s, step_size in enumerate([2,4,6,8,10]):
    # plt.fill_between(xs[i_s,:],mins_plt[i_s,:max_it],
    #                  maxs_plt[i_s,:max_it],
    #                  color=colors[i_s],alpha=0.1)
    plt.plot(xs[i_s,1:],means_plt[i_s,1:max_it],color=colors[i_s],label=str(step_size)+' m')
    # plt.plot(xs[i_s,:],mins_plt[i_s,:max_it],color=colors[i_s],linestyle='--')
    # plt.plot(xs[i_s,:],maxs_plt[i_s,:max_it],color=colors[i_s],linestyle='--')
    # plt.plot(x,mins_interp[i_s,:],color=colors[i_s],linestyle='--')
    # plt.plot(x,maxs_interp[i_s,:],color=colors[i_s],linestyle='--')

plt.xscale('log')
legend = plt.legend(loc='lower right', ncol=1, fontsize=7, columnspacing=1, title="Max Step (m)")
plt.setp(legend.get_title(),fontsize=7)
# plt.legend(loc='upper center', ncol=5, fontsize=7.5, columnspacing=1)
plt.xlim((0.9,1100))
plt.ylim((-0.03,1.03))
plt.xlabel('Time (minutes)', fontsize=10)
plt.ylabel('Fraction Covered', fontsize=10)
# plt.title('Empirical Coverage vs. Time', fontsize=10)
plt.tight_layout()
plt.savefig('Empirical_Rev5.pdf', dpi=300)

# n_lines = 5
# x = np.linspace(0, 10, 100)
# y = np.sin(x[:, None] + np.pi * np.linspace(0, 1, n_lines))
# c = np.arange(1., n_lines + 1)

# cmap = plt.get_cmap("jet", len(c))
# norm = matplotlib.colors.BoundaryNorm(np.arange(len(c)+1)+0.5,len(c))
# sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
# sm.set_array([])  # this line may be ommitted for matplotlib >= 3.1

# fig, ax = plt.subplots(dpi=100)
# for i, yi in enumerate(y.T):
#     ax.plot(x, yi, c=cmap(i))
# fig.colorbar(sm, ticks=c)
# plt.show()
