import numpy as np
import csv
# import matplotlib.pyplot as plt
from scipy.stats import kstest

step_num = 5
trials = 10
times = int(50000/100)

if 'ref' in locals():
    pass
else:
    rows = []
    with open('ref_dist.csv', 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    ref = np.array(rows).astype('float')

folders = ['Sims/Trials-Source100'] #'Sims/Trials-Source100'

for folder in folders:

    ks_trials = np.zeros((times, trials*30*5))   
    row_num = 0
    
    times_max  = np.zeros((times,0))
    times_min  = np.zeros((times,0))
    times_mean = np.zeros((times,0))
    times_std  = np.zeros((times,0))
    times_med  = np.zeros((times,0))

    for room_num in np.arange(21,51):
        
        for step_size in [2,4,6,8,10]:
            
            for trial in np.arange(1,trials+1):
        
                rows = []
                with open(folder+'/Room'+str(room_num)+'/step'+str(step_size)+'_run'+str(trial)+'.csv', 'r') as file:
                    csvreader = csv.reader(file)
                    header = next(csvreader)
                    for row in csvreader:
                        rows.append(row)
                
                data = np.array(rows).astype(float)
                iteration = data[:,0]
                steps     = data[:,3] / step_size
                                    
                print('Processing: ', room_num, step_size, trial)
                
                for i_t, t in enumerate(np.arange(100,len(iteration)+1,100)):
                    
                    if ks_trials[i_t,row_num] != -5:
                        
                        result_ks = kstest(steps[:t].reshape((-1,1)).squeeze(),ref.squeeze())
                        pvalue = result_ks.pvalue
                        if pvalue == 0:
                            print('Error: ', room_num, step_size, t)
                            logsig = 0
                        else:
                            logsig = np.log10(pvalue)
                        ks_trials[i_t,row_num] = logsig
                        
                        if logsig < -5:
                            ks_trials[i_t:,row_num] = -5
                        
                row_num += 1
                    
    times_max  = np.max(ks_trials,axis=1)
    times_min  = np.min(ks_trials,axis=1)
    times_mean = np.mean(ks_trials,axis=1)
    times_std  = np.std(ks_trials,axis=1)
    times_med  = np.median(ks_trials,axis=1)
    
    np.savetxt(folder+'/KS/Full_Data.csv',
               ks_trials, delimiter=',')
    
    np.savetxt(folder+'/KS/KS_Tmax.csv',
               times_max, delimiter=',')
        
    np.savetxt(folder+'/KS/KS_Tmin.csv',
               times_min, delimiter=',')
    
    np.savetxt(folder+'/KS/KS_Tmean.csv',
               times_mean, delimiter=',')
        
    np.savetxt(folder+'/KS/KS_Tstd.csv',
               times_std, delimiter=',')
        
    np.savetxt(folder+'/KS/KS_Tmed.csv',
               times_med, delimiter=',')
