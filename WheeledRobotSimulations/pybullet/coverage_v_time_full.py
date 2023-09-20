import numpy as np
import csv
#import matplotlib.pyplot as plt

bins = 3
step_num = 5
trials = 10
times = 5000

folders = ['Sims/Trials-NoSource'] #, 'Sims/Trials-Source100']

for folder in folders:
    
    coverage_trials = np.zeros((times, trials*30*5, bins))
    row_num = 0

    for room_num in np.arange(21,51):
        
        for i_s, step_size in enumerate([2,4,6,8,10]):
            
            print(room_num, step_size)
                        
            for trial in np.arange(1,trials+1):
        
                rows = []
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
                        
                        if coverage_trials[i_t,row_num,i_n] != 1:
                            
                            xedges = np.linspace(-4.95,4.95,nb+1)
                            yedges = np.linspace(-4.95,4.95,nb+1)
            
                            H, __, __ = np.histogram2d(x[:t], y[:t], bins=(xedges, yedges))
                            
                            try:
                                rows = []
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
                            
                            coverage_trials[i_t,row_num,i_n] = coverage
                            if coverage > 0.999:
                                coverage_trials[i_t:,row_num,i_n] = 1
                                
                row_num += 1
                
    times_max5  = np.max(coverage_trials[:,:,0],axis=1)
    times_min5  = np.min(coverage_trials[:,:,0],axis=1)
    times_mean5 = np.mean(coverage_trials[:,:,0],axis=1)
    times_std5  = np.std(coverage_trials[:,:,0],axis=1)
    times_med5  = np.median(coverage_trials[:,:,0],axis=1)
    
    np.savetxt(folder+'/Coverage/Full_Data_bins5.csv',
               coverage_trials[:,:,0], delimiter=',')
    
    np.savetxt(folder+'/Coverage/KS_Tmax_bins5.csv',
               times_max5, delimiter=',')
        
    np.savetxt(folder+'/Coverage/KS_Tmin_bins5.csv',
               times_min5, delimiter=',')
    
    np.savetxt(folder+'/Coverage/KS_Tmean_bins5.csv',
               times_mean5, delimiter=',')
        
    np.savetxt(folder+'/Coverage/KS_Tstd_bins5.csv',
               times_std5, delimiter=',')
        
    np.savetxt(folder+'/Coverage/KS_Tmed_bins5.csv',
               times_med5, delimiter=',')
    
    times_max10  = np.max(coverage_trials[:,:,1],axis=1)
    times_min10  = np.min(coverage_trials[:,:,1],axis=1)
    times_mean10 = np.mean(coverage_trials[:,:,1],axis=1)
    times_std10  = np.std(coverage_trials[:,:,1],axis=1)
    times_med10  = np.median(coverage_trials[:,:,1],axis=1)
    
    np.savetxt(folder+'/Coverage/Full_Data_bins10.csv',
               coverage_trials[:,:,1], delimiter=',')
    
    np.savetxt(folder+'/Coverage/KS_Tmax_bins10.csv',
               times_max10, delimiter=',')
        
    np.savetxt(folder+'/Coverage/KS_Tmin_bins10.csv',
               times_min10, delimiter=',')
    
    np.savetxt(folder+'/Coverage/KS_Tmean_bins10.csv',
               times_mean10, delimiter=',')
        
    np.savetxt(folder+'/Coverage/KS_Tstd_bins10.csv',
               times_std10, delimiter=',')
        
    np.savetxt(folder+'/Coverage/KS_Tmed_bins10.csv',
               times_med10, delimiter=',')
    
    times_max20  = np.max(coverage_trials[:,:,2],axis=1)
    times_min20  = np.min(coverage_trials[:,:,2],axis=1)
    times_mean20 = np.mean(coverage_trials[:,:,2],axis=1)
    times_std20  = np.std(coverage_trials[:,:,2],axis=1)
    times_med20  = np.median(coverage_trials[:,:,2],axis=1)
    
    np.savetxt(folder+'/Coverage/Full_Data_bins20.csv',
               coverage_trials[:,:,2], delimiter=',')
    
    np.savetxt(folder+'/Coverage/KS_Tmax_bins20.csv',
               times_max20, delimiter=',')
        
    np.savetxt(folder+'/Coverage/KS_Tmin_bins20.csv',
               times_min20, delimiter=',')
    
    np.savetxt(folder+'/Coverage/KS_Tmean_bins20.csv',
               times_mean20, delimiter=',')
        
    np.savetxt(folder+'/Coverage/KS_Tstd_bins20.csv',
               times_std20, delimiter=',')
        
    np.savetxt(folder+'/Coverage/KS_Tmed_bins20.csv',
               times_med20, delimiter=',')
