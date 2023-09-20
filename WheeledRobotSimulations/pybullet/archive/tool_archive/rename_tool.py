import numpy as np
import shutil 


for i in [1, 2, 3, 4, 5, 10]:
    for j in [5, 10, 15, 20]:
        origin_path_E = 'PData_Room6/E_room6_bins'+str(j)+'_maxstep'+str(i)+'.csv'
        origin_path_P = 'PData_Room6/P_room6_bins'+str(j)+'_maxstep'+str(i)+'.csv'
        origin_path_TK = 'PData_Room6/TK_room6_bins'+str(j)+'_maxstep'+str(i)+'.csv'
        dest_E = 'PData/Room6/E_bins'+str(j)+'_maxstep'+str(i)+'.csv'
        dest_P = 'PData/Room6/P_bins'+str(j)+'_maxstep'+str(i)+'.csv'
        dest_TK = 'PData/Room6/TK_bins'+str(j)+'_maxstep'+str(i)+'.csv'

        shutil.copyfile(origin_path_E, dest_E)
        shutil.copyfile(origin_path_P, dest_P)
        shutil.copyfile(origin_path_TK, dest_TK)
        