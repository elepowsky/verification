import subprocess
import numpy as np

for room in np.arange(1,11):
    print('')
    print('Room '+str(room))
    print('')
    cmd = 'python pairs.py --env Room'+str(room)
    subprocess.call(cmd)
