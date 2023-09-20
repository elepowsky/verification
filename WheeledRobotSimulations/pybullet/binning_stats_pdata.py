#%%

import numpy as np
import csv
import matplotlib.pyplot as plt
import time
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

def imageMean(im_base, range_x_px, range_y_px):
    # Normalized 0-1
    # -- invert y 
    range_y_new = [960-range_y_px[1], 960-range_y_px[0]]

    # switch y and x
    return (1./255.)*np.mean(im_base[range_y_new[0]:range_y_new[1], range_x_px[0]:range_x_px[1]])
    


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

start_time = time.time()

img_path = 'Rooms/Room'+room_number_str+'.jpg'
ppi = 96
im_base = plt.imread(img_path)
im_base = 255-im_base
# im_base[48+192:48+288, 48+576:48+672] = 255-im_base[48+192:48+288, 48+576:48+672]
# fig, ax = plt.subplots()
# im_base2 = ax.imshow(im_base[47:1007,48:1008], cmap='binary', extent=[0, 960, 0, 960])
# ax.axis('on')
'''
[(x_min, x_max), (y_min, y_max)]

[(nominal_x_pixels), (nominal_y_pixels)]   (e.g., the point 5,0 --> 960, 480)

Transformations to match ***indices*** of im_read array: 

-- invert y-axis [960 - nominal_y] (960, 480) --> (960, 480)

-- switch x and y --> (960, 480) --> (480, 960)

Claim: im_base[480, 960] corresponds to physical (x, y) of (5, 0)


FOR BINS:
x, y: (1, 2), (2, 3)                        <-- physical coordinates
x_px, y_px: (576, 672), (672, 768)          <-- For plot commands
-- invert y: (576, 672), (288, 192)
-- switch x, y: (192, 288), (576, 672)      <-- arguments / indices of img array

'''

# ax.plot((576, 576), (672, 768), 'r')
# ax.plot((672, 672), (672, 768), 'r')
# ax.plot((576, 672), (672, 672), 'r')
# ax.plot((576, 672), (768, 768), 'r')
# fig.savefig('tmp_fig.png')
# breakpoint()
# print(np.mean(im_base[:10,:10]))
# 255 black
# 0 white
# breakpoint()

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

npoints = 60

NA = 36
ND = 50

step_list = [2, 4, 6, 8, 10]
n_steps = len(step_list)

expected_times = np.zeros((len(n_bin_list),len(step_list)))
upper_times = np.zeros((len(n_bin_list),len(step_list)))

for x, nb in enumerate(n_bin_list):
    xedges = np.linspace(x_start_min-1e-6,x_start_max+1e-6,nb+1)
    yedges = np.linspace(y_start_min-1e-6,y_start_max+1e-6,nb+1)
    sz = (len(xedges)-1)*(len(xedges)-1)

    x_edge_px = np.linspace(0, 960, nb+1)
    y_edge_px = np.linspace(0, 960, nb+1)


    # im_base = plt.imread(img_path)
    # im_base = 255-im_base
    # im_base[48+192:48+288, 48+576:48+672] = 255-im_base[48+192:48+288, 48+576:48+672]
    fig, ax = plt.subplots()
    im_base2 = ax.imshow(im_base[47:1007,48:1008], cmap='binary', extent=[0, 960, 0, 960])
    ax.axis('on')
    # estimatedPointsPerBin = int((int((npoints/nb))**2)*(NA*ND)/step_list[-1])*step_list

    track_zeros = np.zeros(sz)
    
    mainList = [[] for x in range(n_steps)]
    for row in range(len(data)):
        k = n_steps - 1
        while k >= 0 and stepsz[row] <= step_list[k]+1e-8:
            mainList[k].append(row)
            k -= 1
            if k < 0:
                break

    binList = [[] for x in range(sz)]
    for row in range(len(data)):
        xIdx = np.max(np.argwhere(xedges < x_start[row])).astype(int)
        yIdx = np.max(np.argwhere(yedges < y_start[row])).astype(int)
        mainIdx = int(xIdx*(len(yedges)-1)+yIdx)
        binList[mainIdx].append(row)
        

    for y, max_step in enumerate(step_list):
        # # SET THESE PARAMETERS
        # nb = 5 # number of bins in each direction (assuming a square environment)
        # max_step = 2 # maximum step size
        # # SET THESE PARAMETERS
        print(nb, max_step)
        
        # ePPB = estimatedPointsPerBin[y]

        matrix = np.zeros((sz,sz))

        index = 0
        indexList = []
        for ix in range(len(xedges)-1):
            for iy in range(len(yedges)-1):
                indexList.append([xedges[ix], yedges[iy], xedges[ix+1], yedges[iy], index])
                indexList.append([xedges[ix], yedges[iy], xedges[ix], yedges[iy+1], index])

                # Run pixel test for whether or not it's an obstacle
                if imageMean(im_base[47:1007,48:1008], [int(x_edge_px[ix]), int(x_edge_px[ix+1])], [int(y_edge_px[iy]), int(y_edge_px[iy+1])]) >= 0.6:
                    track_zeros[index] = 1.0
                    ax.plot((int(x_edge_px[ix]), int(x_edge_px[ix])), (int(y_edge_px[iy]), int(y_edge_px[iy+1])), 'r')
                    ax.plot((int(x_edge_px[ix+1]), int(x_edge_px[ix+1])), (int(y_edge_px[iy]), int(y_edge_px[iy+1])), 'r')
                    ax.plot((int(x_edge_px[ix]), int(x_edge_px[ix+1])), (int(y_edge_px[iy]), int(y_edge_px[iy])), 'r')
                    ax.plot((int(x_edge_px[ix]), int(x_edge_px[ix+1])), (int(y_edge_px[iy+1]), int(y_edge_px[iy+1])), 'r')
                    
                    '''
                    plt.plot((int(y_edge_px[iy]), int(y_edge_px[iy+1])), (int(x_edge_px[ix]), int(x_edge_px[ix])), 'r')
                    plt.plot((int(y_edge_px[iy]), int(y_edge_px[iy+1])), (int(x_edge_px[ix+1]), int(x_edge_px[ix+1])),'r')
                    plt.plot((int(y_edge_px[iy]), int(y_edge_px[iy])), (int(x_edge_px[ix]), int(x_edge_px[ix+1])), 'r')
                    plt.plot((int(y_edge_px[iy+1]), int(y_edge_px[iy+1])), (int(x_edge_px[ix]), int(x_edge_px[ix+1])), 'r')
                    '''
                else:
                    idxList = list(set(binList[index]) & set(mainList[y]))
                    if len(idxList) > 0:
                        bufferx = x_end[idxList]
                        buffery = y_end[idxList]
                    else:
                        bufferx = []
                        buffery = []
                    
                    H, __, __ = np.histogram2d(bufferx, buffery, bins=(xedges, yedges))
                    tmp = sum(sum(H))
                    if tmp > 0.5:
                        H = H / tmp
                        # if tmp < ePPB*0.1 and max_step <= step_list[0]+0.5:
                        #     track_zeros[index] = 1.0
                    # else:
                    #     track_zeros[index] = 1.0
                    # fig, ax = plt.subplots()
                    # ax.pcolormesh(H)
                    # ax.set_aspect('equal', 'box')
                    # fig.tight_layout()
                    # plt.show()
                
                    matrix[:,index] = H.ravel(order='C')
                
                index += 1

        if max_step <= step_list[0] + 0.1:
            fig.savefig('Rooms/Room'+room_number_str+'_reduced_bins'+str(nb)+'_copy.jpg')
            # breakpoint()
        
        # axs[x,y].pcolormesh(matrix)
        # axs[x,y].set_aspect('equal', 'box')
        # axs[x,y].axis('off')
        
        with open('PData/Room'+room_number_str+'/P_bins'+str(nb)+'_maxstep'+str(max_step)+'_copy.csv', 'w', newline='') as file:
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
                if max_val > (1.-(1e-7)) or track_zeros[n] >= 0.5:
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
            
            badList = []
            
            if ratio_max > 10. and tk_tmp[ratio_max_idx] > 5e3:
                print('Found a cutoff. High value is ', tk_tmp[ratio_max_idx],' and low value is ',tk_tmp[ratio_max_idx-1])
                print('Ratio: ', tk_ratio[ratio_max_idx])
                cutoff_value = tk_tmp[ratio_max_idx]-0.01
                
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
                
                np.savetxt('PData/Room'+room_number_str+'/badIdx_bins'+str(nb)+'_copy.csv', badArray, delimiter=',')

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
        
        np.savetxt('PData/Room'+room_number_str+'/TK_bins'+str(nb)+'_maxstep'+str(max_step)+'_copy.csv', Tk, delimiter=',')
        
        # tau_test = int(np.floor(5*sz*np.log(sz))+1)
        # print('Number of steps to check: ', tau_test)
        # print()
        # tmp_chi = computeChi(tau_test, Tk)
        # print(tmp_chi)
        # print(computeChi_Short(tau_test, Tk))
        # print()
        # print('Inverse calculation: ', InverseTau(tmp_chi,Tk,1e-7), ' steps')
        # print('Real number of steps: ', tau_test)
        
        # Euler-Mascheroni Constant: 0.57721566490153286
        euler_gamma = 0.57721566490153286
        # Gumbel Distribution Mean: mu + gamma*beta
        # Standard Gumbel: mu=0, beta=1 --> Mean = 0 + gamma*1 = gamma
        # Expected traversal time: 
        traversal_time_mean = InverseTau(euler_gamma, Tk, 1e-7)
        traversal_time_upper = InverseTau(4.600149226776579, Tk, 1e-7)
        print('Expected traversal time: ', traversal_time_mean, ' steps')
        print('Upper traversal time: ', traversal_time_upper, ' steps')
        np.savetxt('PData/Room'+room_number_str+'/E_bins'+str(nb)+'_maxstep'+str(max_step)+'_copy.csv',[traversal_time_mean],delimiter=',')
        
        expected_times[x,y] = traversal_time_mean
        upper_times[x, y] = traversal_time_upper

with open('PData/Room'+room_number_str+'/ET_copy.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(expected_times)
    print("\nData saved:", file.name)

with open('PData/Room'+room_number_str+'/UT_copy.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(upper_times)
    print("\n Data saved:", file.name)

# fig.tight_layout()
# plt.show()
end_time = time.time()
print('Total time elapsed: ', end_time-start_time, ' seconds')

#%%

'''
fig, ax = plt.subplots()
ax.pcolormesh(matrix)
ax.set_aspect('equal', 'box')
ax.axis('off')
fig.tight_layout()
plt.show()
'''
