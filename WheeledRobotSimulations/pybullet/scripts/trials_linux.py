import subprocess
import numpy as np

trials = 10

for room in np.arange(1,51):
    for trial in range(trials):
        for step in [2,4,6,8,10]:
            print('')
            print('Room '+str(room)+', Step '+str(step)+', Trial '+str(trial+1))
            print('')
            cmd = 'python3 ../algo_ray.py --env Room'+str(room)+' --maxstep '+str(step)+' --strength '+str(100)
            subprocess.call(cmd, shell=True)
