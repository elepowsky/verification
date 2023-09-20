import numpy as np
import csv
#import matplotlib.pyplot as plt

bins = 3
step_num = 5
trials = 10
times = 5000

folders = ['Sims/Empirical'] #['Sims/Trials-NoSource', 'Sims/Trials-Source100']

for folder in folders:

    for room_num in np.arange(1,11):
        
        times_max  = np.zeros((bins, times))
        times_min  = np.zeros((bins, times))
        times_mean = np.zeros((bins, times))
        times_std  = np.zeros((bins, times))
        times_med  = np.zeros((bins, times))
        
        for i_s, step_size in enumerate([2,4,6,8,10]):
            
            coverage_trials = np.zeros((bins, times, trials))
            
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
                
                for i_n, nb in enumerate([5,10,20]):
                    
                    for i_t, t in enumerate(np.arange(0,len(iteration),10)):
                        
                        if coverage_trials[i_n,i_t,trial-1] != 1:
                            
                            xedges = np.linspace(-4.95,4.95,nb+1)
                            yedges = np.linspace(-4.95,4.95,nb+1)
            
                            H, __, __ = np.histogram2d(x[:t], y[:t], bins=(xedges, yedges))
                            
                            try:
                                rows = []
                                if room_num in [5,7,8,9,10]:
                                    with open('BadBins/Room'+str(room_num+60)+'/badIdx_bins'+str(nb)+'_copy.csv', 'r') as file:
                                        csvreader = csv.reader(file)
                                        for row in csvreader:
                                            rows.append(row)
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
                            
                            coverage_trials[i_n,i_t,trial-1] = coverage
                            if coverage > 0.999:
                                coverage_trials[i_n,i_t:,trial-1] = 1
                    
            times_max  = np.max(coverage_trials,axis=2)
            times_min  = np.min(coverage_trials,axis=2)
            times_mean = np.mean(coverage_trials,axis=2)
            times_std  = np.std(coverage_trials,axis=2)
            times_med  = np.median(coverage_trials,axis=2)
            
            with open(folder+'/Coverage/Room'+str(room_num)+'_steps'+str(step_size)+'_Tmax.csv','w',newline='') as file:
                writer = csv.writer(file)
                writer.writerows(times_max)
                print("\n Data saved:", file.name)
                
            with open(folder+'/Coverage/Room'+str(room_num)+'_steps'+str(step_size)+'_Tmin.csv','w',newline='') as file:
                writer = csv.writer(file)
                writer.writerows(times_min)
                print("\n Data saved:", file.name)
            
            with open(folder+'/Coverage/Room'+str(room_num)+'_steps'+str(step_size)+'_Tmean.csv','w',newline='') as file:
                writer = csv.writer(file)
                writer.writerows(times_mean)
                print("\n Data saved:", file.name)
                
            with open(folder+'/Coverage/Room'+str(room_num)+'_steps'+str(step_size)+'_Tstd.csv','w',newline='') as file:
                writer = csv.writer(file)
                writer.writerows(times_std)
                print("\n Data saved:", file.name)
                
            with open(folder+'/Coverage/Room'+str(room_num)+'_steps'+str(step_size)+'_Tmed.csv','w',newline='') as file:
                writer = csv.writer(file)
                writer.writerows(times_med)
                print("\n Data saved:", file.name)
