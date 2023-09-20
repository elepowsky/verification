#%%

import numpy as np
import csv
import matplotlib.pyplot as plt

import sys # To automate paths
# sample command: python3 binning_stats.py room_number 

#%%

def computeChi_Short(tau, Tk):
    return -np.log(np.sum(np.exp(-tau/Tk)))

def computeChi(tau, Tk):
    stat_val = 0
    for k in range(len(Tk)):
        if Tk[k] >= 0.5:
            stat_val += np.exp(-tau/Tk[k])
    
    return -np.log(stat_val)

def InverseTau(chi: float, Tk: np.ndarray, epsilon: float) -> int:
    max_tau = np.max(Tk)
    min_tau = 0.5*np.max(Tk)
    while(computeChi(max_tau, Tk) <= chi):
        min_tau = max_tau
        max_tau = 2*max_tau

    tau_0 = 0.5*(max_tau-min_tau) + min_tau
    done_opt = False
    chi_0 = computeChi(tau_0, Tk)
    while not done_opt:
        error = np.abs(chi_0-chi)
        if error <= epsilon:
            done_opt = True
            return int(np.floor(tau_0)+1)
        else:
            if chi_0-chi > 0: # Guess is too high, reduce tau_0
                max_tau = tau_0
            else: # Guess is too low, increase tau_0
                min_tau = tau_0
        
        tau_0 = 0.5*(max_tau-min_tau) + min_tau
        if max_tau - min_tau <=3:
            return int(np.floor(max_tau)+1)

        chi_0 = computeChi(tau_0, Tk)

#%%

# fig, axs = plt.subplots(4,6)

# sample command: python3 binning_stats.py room_number 
if len(sys.argv) == 1:
    raise ValueError("Must include room_number as an argument, e.g.: 'python3 binning_stats.py 7' where '7' is the room_number")
elif len(sys.argv) == 2:
    room_number = int(sys.argv[1])
    room_number_str = str(room_number)
else:
    raise ValueError('Only supports layout_number argument; there are too many arguments in the attempted command')

rows = []
with open('pairs_room'+room_number_str+'_large.csv', 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)

data = np.array(rows).astype(float)
x_start = data[:,0]
x_start_min = min(x_start)
x_start_max = max(x_start)

y_start = data[:,1]
y_start_min = min(y_start)
y_start_max = max(y_start)

x_end   = data[:,2]
y_end   = data[:,3]
stepsz  = data[:,5]

n_bin_list = [5, 10, 20]
npoints = 100

step_list = [2, 4, 5, 10]
expected_times = np.zeros((len(n_bin_list),len(step_list)))
upper_times = np.zeros((len(n_bin_list),len(step_list)))

for x, nb in enumerate(n_bin_list):
    xedges = np.linspace(x_start_min,x_start_max,nb+1)
    yedges = np.linspace(y_start_min,y_start_max,nb+1)
    sz = (len(xedges)-1)*(len(xedges)-1)

    # estimatedPointsPerBin = ((npoints/nb)**2)*(36*50)

    track_zeros = np.zeros(sz)
    
    for y, max_step in enumerate(step_list):
        # # SET THESE PARAMETERS
        # nb = 5 # number of bins in each direction (assuming a square environment)
        # max_step = 2 # maximum step size
        # # SET THESE PARAMETERS
        print(nb, max_step)
        
        matrix = np.zeros((sz,sz))

        index = 0
        indexList = []
        for ix in range(len(xedges)-1):
            for iy in range(len(yedges)-1):
                indexList.append([xedges[ix], yedges[iy], xedges[ix+1], yedges[iy], index])
                indexList.append([xedges[ix], yedges[iy], xedges[ix], yedges[iy+1], index])
                bufferx, buffery = [], []
                for row in range(len(data)):
                    if stepsz[row] <= max_step:
                        if x_start[row] >= xedges[ix] and x_start[row] < xedges[ix+1]:
                            if y_start[row] >= yedges[iy] and y_start[row] < yedges[iy+1]:
                                bufferx.append(x_end[row])
                                buffery.append(y_end[row])
                H, __, __ = np.histogram2d(bufferx, buffery, bins=(xedges, yedges))
                tmp = sum(sum(H))
                if tmp > 0.05:
                    H = H / sum(sum(H))
                else:
                    track_zeros[index] = 1.0
                # fig, ax = plt.subplots()
                # ax.pcolormesh(H)
                # ax.set_aspect('equal', 'box')
                # fig.tight_layout()
                # plt.show()
                matrix[:,index] = H.ravel(order='C')
                index += 1

        # axs[x,y].pcolormesh(matrix)
        # axs[x,y].set_aspect('equal', 'box')
        # axs[x,y].axis('off')
        
        with open('PData/Room'+room_number_str+'/P_bins'+str(nb)+'_maxstep'+str(max_step)+'.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(matrix)
            print("\nData saved:", file.name)

        Omega = matrix #np.genfromtxt('P_room6_bins'+str(nb)+'_maxstep'+str(max_step)+'.csv', delimiter=',')
        Tk = np.zeros(sz)
        
        if max_step <= step_list[0]+0.5: # max_step = minimal max_step ONLY
            for n in range(sz):
                D = np.copy(Omega)
                D[:,n] = 0
                vals = np.sort(np.linalg.eigvals(D))
                max_val = np.abs(vals[-1])
                if max_val > (1.-(1e-7)):
                    Tk[n] = 1e7
                else:
                    Tk[n] = -1.0/np.log(max_val)

            # Run a filter on the Tk[n] because eigvals ain't cutting it
            # Sort and search for the biggest multiplicative gap
            # Run some logic 
            tk_tmp = np.sort(Tk)
            tk_ratio = np.ones(sz)
            for k in range(1, sz):
                tk_ratio[k] = tk_tmp[k]/tk_tmp[k-1]
            
            # Conditions: tk_ratio > 10, tk_tmp > 1e4
            big_ratios = np.argwhere(tk_ratio > 10)
            if np.max(tk_ratio) >= 10:
                ratio_max = tk_ratio[big_ratios[0]]
                ratio_max_idx = big_ratios[0]
            else:
                ratio_max = np.max(tk_ratio)
                ratio_max_idx = np.argmax(tk_ratio)
            
            if ratio_max > 10. and tk_tmp[ratio_max_idx] > 5e3:
                print('Found a cutoff. High value is ', tk_tmp[ratio_max_idx],' and low value is ',tk_tmp[ratio_max_idx-1])
                print('Ratio: ', tk_ratio[ratio_max_idx])
                cutoff_value = tk_tmp[ratio_max_idx]-0.01
                badList = []
                for k in range(sz):
                    if Tk[k] >= cutoff_value:
                        Tk[k] = 0.1
                        track_zeros[k] = 1.0
                        badList.append([indexList[2*k], k])
                        badList.append([indexList[2*k+1], k])
                        
            else:
                cutoff_value = tk_tmp[-1] + 10
            
            if len(badList) > 0:
                print('Length of bad list: ', len(badList))
                badArray = np.zeros((int(len(badList)/2), 5))
                for k in range(int(len(badList)/2)):
                    badArray[k, 0] = badList[2*k][0][0]     # x0
                    badArray[k, 1] = badList[2*k][0][1]     # y0
                    badArray[k, 2] = badList[2*k][0][2]     # x1
                    badArray[k, 3] = badList[2*k+1][0][3]   # y1
                    badArray[k, 4] = badList[2*k][0][4]     # index
                
                np.savetxt('PData/Room'+room_number_str+'/badIdx_bins'+str(nb)+'.csv', badArray, delimiter=',')

        else: # max_step all non-minimal max_steps
            for n in range(sz):
                if track_zeros[n] >= 0.5:
                    Tk[n] = 0.1
                else:
                    D = np.copy(Omega)
                    D[:,n] = 0
                    vals = np.sort(np.linalg.eigvals(D))
                    max_val = np.abs(vals[-1])
                    if max_val > (1.-(1./(10.*cutoff_value))):
                        raise ValueError('Error in wall filtering!!!!')
                    else:
                        Tk[n] = -1.0/np.log(max_val)
        
        # # Run a filter on the Tk[n] because eigvals ain't cutting it
        # # Sort and search for the biggest multiplicative gap
        # # Run some logic 
        # tk_tmp = np.sort(Tk)
        # tk_ratio = np.ones(sz)
        # for k in range(1, sz):
        #     tk_ratio[k] = tk_tmp[k]/tk_tmp[k-1]
        
        np.savetxt('PData/Room'+room_number_str+'/TK_bins'+str(nb)+'_maxstep'+str(max_step)+'.csv', Tk, delimiter=',')
        
        tau_test = int(np.floor(5*sz*np.log(sz))+1)
        print('Number of steps to check: ', tau_test)
        print()
        tmp_chi = computeChi(tau_test, Tk)
        print(tmp_chi)
        print(computeChi_Short(tau_test, Tk))
        print()
        print('Inverse calculation: ', InverseTau(tmp_chi,Tk,1e-7), ' steps')
        print('Real number of steps: ', tau_test)
        
        # Euler-Mascheroni Constant: 0.57721566490153286
        euler_gamma = 0.57721566490153286
        # Gumbel Distribution Mean: mu + gamma*beta
        # Standard Gumbel: mu=0, beta=1 --> Mean = 0 + gamma*1 = gamma
        # Expected traversal time: 
        traversal_time_mean = InverseTau(euler_gamma, Tk, 1e-7)
        traversal_time_upper = InverseTau(4.600149226776579, Tk, 1e-7)
        print('Expected traversal time: ', traversal_time_mean, ' steps')
        print('Upper traversal time: ', traversal_time_upper, ' steps')
        np.savetxt('PData/Room'+room_number_str+'/E_bins'+str(nb)+'_maxstep'+str(max_step)+'.csv',[traversal_time_mean],delimiter=',')
        
        expected_times[x,y] = traversal_time_mean
        upper_times[x, y] = traversal_time_upper

with open('PData/Room'+room_number_str+'/ET.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(expected_times)
    print("\nData saved:", file.name)

with open('PData/Room'+room_number_str+'/UT.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(upper_times)
    print("\n Data saved:", file.name)

# fig.tight_layout()
# plt.show()

#%%

'''
fig, ax = plt.subplots()
ax.pcolormesh(matrix)
ax.set_aspect('equal', 'box')
ax.axis('off')
fig.tight_layout()
plt.show()
'''
