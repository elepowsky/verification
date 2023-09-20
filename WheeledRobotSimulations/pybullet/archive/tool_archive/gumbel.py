import numpy as np
import sys
import csv

#%%

def gumbel_percentile(x=0.57721566490153286,a=0,b=1):
    cdf = np.exp(-np.exp(-(x-a)/b))
    return cdf

# print(gumbel_percentile(x=-np.log(np.log(2))))

def inverse_gumbel(cdf):
    x = -np.log(-np.log(cdf))
    return x

# print(inverse_gumbel(0.99))

#%% UPDATE FROM DAVID

def InverseTau(chi: float, Tk: np.ndarray, epsilon: float) -> int:
    max_tau = np.max(Tk)
    min_tau = 0.5*np.max(Tk)
    while(-np.log(np.sum(np.exp(-max_tau/Tk))) <= chi):
        min_tau = max_tau
        max_tau = 2*max_tau

    tau_0 = 0.5*(max_tau-min_tau) + min_tau
    done_opt = False
    chi_0 = -np.log(np.sum(np.exp(-tau_0/Tk)))
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
        chi_0 = -np.log(np.sum(np.exp(-tau_0/Tk)))
        
#%%

if len(sys.argv) == 1:
    raise ValueError("Must include room_number as an argument, e.g.: 'python3 gumbel.py 7' where '7' is the room_number")
elif len(sys.argv) == 2:
    room_number = int(sys.argv[1])
    room_number_str = str(room_number)
else:
    raise ValueError('Only supports layout_number argument; there are too many arguments in the attempted command')

#%%

expected_times = np.zeros((4,6))
upper_times = np.zeros((4,6))

for x, nb in enumerate([5,10,15,20]):
    for y, max_step in enumerate([1,2,3,4,5,10]):
        
        Tk = []
        with open('PData/Room'+room_number_str+'/TK_bins'+str(nb)+'_maxstep'+str(max_step)+'.csv', 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                Tk.append(row)
        
        euler_gamma = 0.57721566490153286
        upper_confidence_99 = inverse_gumbel(0.99)
        
        traversal_time_mean  = InverseTau(euler_gamma, Tk, 1e-7)
        print('Expected traversal time: ', traversal_time_mean, ' steps')
        np.savetxt('PData/Room'+room_number_str+'/E_bins'+str(nb)+'_maxstep'+str(max_step)+'.csv',[traversal_time_mean],delimiter=',')
        
        traversal_time_upper = InverseTau(upper_confidence_99, Tk, 1e-7)
        print('Upper traversal time: ', traversal_time_upper, ' steps')
        np.savetxt('PData/Room'+room_number_str+'/U_bins'+str(nb)+'_maxstep'+str(max_step)+'.csv',[traversal_time_upper],delimiter=',')
        
        expected_times[x,y] = traversal_time_mean
        upper_times[x,y] = traversal_time_upper
        
with open('PData/Room'+room_number_str+'/ET.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(expected_times)
    print("\nData saved:", file.name)
    
with open('PData/Room'+room_number_str+'/UT.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(upper_times)
    print("\nData saved:", file.name)
