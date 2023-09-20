import subprocess
import numpy as np

trials = 50

for room in [65]:
    for trial in range(trials):
        for step in [2,4,6,8,10]:
            print('')
            print('Room '+str(room)+', Step '+str(step)+', Trial '+str(trial+1))
            print('')
            cmd = 'python ../algo_ray.py --env Room'+str(room)+' --maxstep '+str(step)+' --strength '+str(0)
            subprocess.call(cmd)
