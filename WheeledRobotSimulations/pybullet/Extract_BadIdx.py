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
if len(sys.argv) <= 2:
    raise ValueError("Must include room_number and maxstep as an argument, e.g.: 'python3 binning_stats.py 7 6' where '7' is the room_number and 6 the maxstep")
elif len(sys.argv) == 3:
    room_number = int(sys.argv[1])
    room_number_str = str(room_number)
    max_step_str = str(int(sys.argv[2]))
    max_step = float(sys.argv[2])
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

'''
rows = []
with open('AltData/Room'+room_number_str+'/maxstep'+max_step_str+'_part1of1.csv', 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)

data = np.array(rows).astype(float)
XX = data[:, 0]
YY = data[:, 1]

x_start_min = min(XX)
x_start_max = max(XX)

y_start_min = min(YY)
y_start_max = max(YY)

# x_end   = data[:,2]
# y_end   = data[:,3]
# stepsz  = data[:,5]
'''

n_bin_list = [5, 10, 20]

# step_list = [2, 4, 6, 8, 10]
# n_steps = len(step_list)

# expected_times = np.zeros(len(n_bin_list))
# upper_times = np.zeros(len(n_bin_list))

for x, nb in enumerate(n_bin_list):
    xedges = np.linspace(-5.0-1e-6,5.0+1e-6,nb+1)
    yedges = np.linspace(-5.0-1e-6,5.0+1e-6,nb+1)
    sz = (nb)*(nb)

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
    
    # mainList = [[] for x in range(n_steps)]
    # for row in range(len(data)):
    #     k = n_steps - 1
    #     while k >= 0 and stepsz[row] <= step_list[k]+1e-8:
    #         mainList[k].append(row)
    #         k -= 1
    #         if k < 0:
    #             break
    index = 0
    indexList = []
    for ix in range(nb):
        for iy in range(nb):
            indexList.append([xedges[ix], yedges[iy], xedges[ix+1], yedges[iy], index])
            indexList.append([xedges[ix], yedges[iy], xedges[ix], yedges[iy+1], index])

            # Run pixel test for whether or not it's an obstacle
            if imageMean(im_base[47:1007,48:1008], [int(x_edge_px[ix]), int(x_edge_px[ix+1])], [int(y_edge_px[iy]), int(y_edge_px[iy+1])]) >= 0.75:
                track_zeros[index] = 1.0
                ax.plot((int(x_edge_px[ix]), int(x_edge_px[ix])), (int(y_edge_px[iy]), int(y_edge_px[iy+1])), 'r')
                ax.plot((int(x_edge_px[ix+1]), int(x_edge_px[ix+1])), (int(y_edge_px[iy]), int(y_edge_px[iy+1])), 'r')
                ax.plot((int(x_edge_px[ix]), int(x_edge_px[ix+1])), (int(y_edge_px[iy]), int(y_edge_px[iy])), 'r')
                ax.plot((int(x_edge_px[ix]), int(x_edge_px[ix+1])), (int(y_edge_px[iy+1]), int(y_edge_px[iy+1])), 'r')

            index += 1
  
    fig.savefig('AltData/Room'+room_number_str+'/img_reduced_bins'+str(nb)+'.jpg')
    # breakpoint()

    print(nb)

    badList = []
    for k in range(sz):
        if track_zeros[k] == 1.0:
            badList.append([indexList[2*k], k])
            badList.append([indexList[2*k+1], k])  
    
    if len(badList) > 0:
        print('Length of bad list: ', len(badList))
        badArray = np.zeros((int(len(badList)/2), 5))
        for k in range(int(len(badList)/2)):
            badArray[k, 0] = badList[2*k][0][0]     # x0
            badArray[k, 1] = badList[2*k][0][1]     # y0
            badArray[k, 2] = badList[2*k][0][2]     # x1
            badArray[k, 3] = badList[2*k+1][0][3]   # y1
            badArray[k, 4] = badList[2*k][0][4]     # index
        
        np.savetxt('AltData/Room'+room_number_str+'/badIdx_bins'+str(nb)+'_copy.csv', badArray, delimiter=',')

    
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
