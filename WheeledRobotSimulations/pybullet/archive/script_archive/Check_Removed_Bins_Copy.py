import numpy as np
# import cv2
# import csv
import sys
from matplotlib import pyplot as plt


def viz_main(room_number, nbins):
    
    room_number_str = str(room_number)

    data_path = 'PData/Room'+room_number_str+'/badIdx_bins'+str(nbins)+'_copy.csv'

    img_path = 'Rooms/Room'+room_number_str+'.jpg'
    ppi = 96
    im_base = plt.imread(img_path)
    fig, ax = plt.subplots()
    im_base = ax.imshow(255-im_base, cmap='Greys', extent=[0, 1056, 0, 1056])

    try:
        badArray = np.genfromtxt(data_path, delimiter=',')
        X0 = []
        X1 = []
        Y0 = []
        Y1 = []
        for k in range(badArray.shape[0]):
            X0.append(badArray[k,0])
            Y0.append(badArray[k,1])
            X1.append(badArray[k,2])
            Y1.append(badArray[k,3])
        
        for k in range(len(X0)):
            x0 = (X0[k]+5.5)*ppi
            y0 = (Y0[k]+5.5)*ppi
            x1 = (X1[k]+5.5)*ppi
            y1 = (Y1[k]+5.5)*ppi
            ax.plot((x0, x1), (y0, y0), 'r')
            ax.plot((x0, x1), (y1, y1), 'r')
            ax.plot((x0, x0), (y0, y1), 'r')
            ax.plot((x1, x1), (y0, y1), 'r')

    except:
        # print('Nbins = ', nbins)
        # print('Room number = ', room_number)
        # raise ValueError('Could not find data path. Please check room number and nbins arguments')
        print('Did not find any bad list; just showing the image (unreduced)')
    
    fig.savefig('Rooms/Room'+room_number_str+'reduced_bins'+str(nbins)+'_copy.jpg')

    return 


if __name__ == "__main__":
    # sample command: python3 binning_stats.py room_number 
    if len(sys.argv) <= 2:
        raise ValueError("Must include room_number AND nbins as arguments, e.g.: 'python3 Check_Removed_Bins.py 7 10' where '7' is the room_number")
    elif len(sys.argv) == 3:
        room_number = int(sys.argv[1])
        nbins = int(sys.argv[2])

    else:
        raise ValueError('Only supports layout_number and nbins arguments; there are too many arguments in the attempted command')
    
    viz_main(room_number, nbins)