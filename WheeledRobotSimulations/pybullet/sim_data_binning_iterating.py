import numpy as np
import csv
#import matplotlib.pyplot as plt

bins = 3
step_num = 5
trials = 50

folder = 'Sims/Empirical'

for room_num in np.arange(1,11):
    
    times_max  = np.zeros((bins, step_num))
    times_min  = np.zeros((bins, step_num))
    times_mean = np.zeros((bins, step_num))
    times_std  = np.zeros((bins, step_num))
    times_med  = np.zeros((bins, step_num))
    
    for i_s, step_size in enumerate([2,4,6,8,10]):
        
        coverage_trials = np.zeros((bins, trials))
        
        for trial in np.arange(1,trials+1):
    
            rows = []
            if room_num in [5,7,8,9,10]:
                with open(folder+'/Room'+str(room_num+60)+'/step'+str(step_size)+'_run'+str(trial)+'.csv', 'r') as file:
                    csvreader = csv.reader(file)
                    header = next(csvreader)
                    for row in csvreader:
                        rows.append(row)
            else:
                with open(folder+'/Room'+str(room_num)+'/step'+str(step_size)+'_run'+str(trial)+'.csv', 'r') as file:
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
            
            # fig, ax = plt.subplots()
            # ax.plot(x,y,color='black')
            # ax.set_aspect('equal', 'box')
            # plt.title('Room '+str(room_num))
            # fig.tight_layout()
            # plt.show()
            
            for i_n, nb in enumerate([5,10,20]):
                
                xedges = np.linspace(-4.95,4.95,nb+1)
                yedges = np.linspace(-4.95,4.95,nb+1)
                
                max_guess = len(iteration)
                min_guess = 0
                
                found = False
                covered_it = int(0.5*(max_guess - min_guess) + min_guess)
                
                while not found:
                
                    H, __, __ = np.histogram2d(x[:covered_it], y[:covered_it], bins=(xedges, yedges))
                    
                    try:
                        rows = []
                        if room_num in [5,7,8,9,10]:
                            with open('BadBins/Room'+str(room_num+60)+'/badIdx_bins'+str(nb)+'_copy.csv', 'r') as file:
                                csvreader = csv.reader(file)
                                for row in csvreader:
                                    rows.append(row)
                            badIdx = np.array(rows)[:,-1].astype('float').astype('int')
                            bad_bins = len(badIdx)
                        else:
                            with open('BadBins/Room'+str(room_num)+'/badIdx_bins'+str(nb)+'_copy.csv', 'r') as file:
                                csvreader = csv.reader(file)
                                for row in csvreader:
                                    rows.append(row)
                            badIdx = np.array(rows)[:,-1].astype('float').astype('int')
                            bad_bins = len(badIdx)
                        
                        H_temp = H.ravel()
                        H_temp[badIdx] = 0
                        H = H_temp.reshape(np.shape(H))
                    except:
                        bad_bins = 0
                    
                    covered = np.zeros(np.shape(H))
                    covered[H > 0] = 1
                    
                    coverage = sum(sum(covered))/(nb*nb - bad_bins)
                    
                    if coverage < 1:
                        min_guess = covered_it
                    else:
                        max_guess = covered_it
                    covered_it = int(0.5*(max_guess - min_guess) + min_guess)
                    
                    if (max_guess - min_guess) < 2:
                        found = True
                        covered_it = max_guess
                
                coverage_trials[i_n,trial-1] = covered_it
                
                # print('Room '+str(room_num)+', Bins '+str(nb)+' Fraction covered: '+str(coverage))
                
                # fig, ax = plt.subplots()
                # im = ax.pcolormesh(covered.T, cmap=plt.colormaps['binary'], vmin=0, vmax=1)
                # ax.set_aspect('equal', 'box')
                # fig.tight_layout()
                # plt.show()
        
        times_max[:,i_s]  = np.max(coverage_trials,axis=1)
        times_min[:,i_s]  = np.min(coverage_trials,axis=1)
        times_mean[:,i_s] = np.mean(coverage_trials,axis=1)
        times_std[:,i_s]  = np.std(coverage_trials,axis=1)
        times_med[:,i_s]  = np.median(coverage_trials,axis=1)
        
    with open(folder+'/Times/Room'+str(room_num)+'_Tmax.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(times_max)
        print("\n Data saved:", file.name)
        
    with open(folder+'/Times/Room'+str(room_num)+'_Tmin.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(times_min)
        print("\n Data saved:", file.name)
    
    with open(folder+'/Times/Room'+str(room_num)+'_Tmean.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(times_mean)
        print("\n Data saved:", file.name)
        
    with open(folder+'/Times/Room'+str(room_num)+'_Tstd.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(times_std)
        print("\n Data saved:", file.name)
        
    with open(folder+'/Times/Room'+str(room_num)+'_Tmed.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(times_med)
        print("\n Data saved:", file.name)
