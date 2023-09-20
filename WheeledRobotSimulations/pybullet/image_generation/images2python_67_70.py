import cv2
import numpy as np

# # Testing
# im = cv2.imread('../Rooms/Room_Blank.bmp', cv2.IMREAD_GRAYSCALE)
#	
# print(im.shape)

### NOTES ###
# 255 is white
# 0 is black
#
# Need to be in (base) conda environment to use opencv!
#

def special_image():

    # 96 pixels per inch
    ppi = 96

    # Dimension in inches
    im_dim = (11, 11)
    xmax, ymax = [ppi*im_dim[0], ppi*im_dim[1]]

    # Add in a border (1/2 inch) -- subtract 1 from each dimension to get open space within 
    im_base = (255 - np.zeros((ppi*im_dim[0], ppi*im_dim[1]))).astype(int)
    print(im_base.shape)
    print(np.mean(im_base))

    outer_width = int(ppi/2)

    for i in range(xmax):
        for j in range(ymax):
            if i < outer_width or i >= xmax-outer_width-1 or j < outer_width or j >= ymax-outer_width-1:
                im_base[i, j] = int(0)

    # Maps 67-70 -- thin walls, replace numbers 7-10
    im_67 = np.copy(im_base)
    im_68 = np.copy(im_base)
    im_69 = np.copy(im_base)
    im_70 = np.copy(im_base)

    centerWidth = ppi
    for i in range(xmax):
        for j in range(ymax):

            if (np.abs(i - 2.5*ppi) <= 3 and j >= 2.5*ppi and j < 6.5*ppi) or (np.abs(j - 2.5*ppi) <= 3 and i >= 2.5*ppi and i <= 6.5*ppi):
                im_67[i,j] = int(0)

            if (np.abs(i - 5.5*ppi) <= 3 and j > 2.5*ppi and j <= 8.5*ppi) or (np.abs(j - 5.5*ppi) <= 3 and i > 2.5*ppi and i <= 8.5*ppi):
                im_68[i,j] = int(0)
            
            if (np.abs(j - 8.5*ppi) <= 3 or np.abs(j-2.5*ppi) <=3) and (i > 2.5*ppi and i <= 6.5*ppi):
                im_69[i, j] = int(0)
                im_70[i, j] = int(0)
            elif (np.abs(i - 6.5*ppi) <= 3 and j >= 2.5*ppi and j < 8.5*ppi):
                im_69[i,j] = int(0)
                im_70[i, j] = int(0)
            elif (np.abs(j - 8.5*ppi) <= 3 or np.abs(j-2.5*ppi) <=3) and (i >= 6.5*ppi and i < 9.5*ppi):
                im_70[i, j] = int(0)

    # cv2.imwrite('../Rooms/Room'+str(67)+'.jpg', im_67)
    # cv2.imwrite('../Rooms/Room'+str(67)+'.pbm', im_67)

    # cv2.imwrite('../Rooms/Room'+str(68)+'.jpg', im_68)
    # cv2.imwrite('../Rooms/Room'+str(68)+'.pbm', im_68)

    # cv2.imwrite('../Rooms/Room'+str(69)+'.jpg', im_69)
    # cv2.imwrite('../Rooms/Room'+str(69)+'.pbm', im_69)

    # cv2.imwrite('../Rooms/Room'+str(70)+'.jpg', im_70)
    # cv2.imwrite('../Rooms/Room'+str(70)+'.pbm', im_70)

    im_65 = np.copy(im_base)
    centerEmpty = 2*ppi
    centerWidth = 2*ppi
    for i in range(xmax):
        for j in range(ymax):
            if np.abs(i-(xmax/2)) > centerEmpty/2 or np.abs(j-(ymax/2)) > centerEmpty/2:
                if np.abs(i-(xmax/2)) > centerWidth/2 and np.abs(j-(ymax/2)) > centerWidth/2:
                    # if ((i <= 9.5*ppi or i >= 10.5*ppi) or (j <= xmax/2 or j >= xmax/2 + centerWidth/2 + ppi/2) or ((i <= 0.5*ppi or i >= 1.5*ppi) or (j <= xmax/2 or j >= xmax/2 + centerWidth/2 + ppi/2))):
                    if (i < 8.5*ppi or i > 10.5*ppi or j <= xmax/2 + centerWidth/2 or j >= xmax/2 + centerWidth/2 + 0) and (i <= 0.5*ppi or i >= 2.5*ppi or j <= xmax/2 + centerWidth/2 or j >= xmax/2 + centerWidth/2 + 0):
                        if (j <= 8.5*ppi or j >= 10.5*ppi or i <= xmax/2 + centerWidth/2 or i >= xmax/2 + centerWidth/2 + 2*ppi-2) and (j <= 0.5*ppi or j >= 2.5*ppi or i <= xmax/2 + centerWidth/2 or i >= xmax/2 + centerWidth/2 + 2*ppi-2):
                            im_65[i, j] = int(0)
    
    # cv2.imwrite('../Rooms/Room'+str(65)+'.jpg', im_65)
    # cv2.imwrite('../Rooms/Room'+str(65)+'.pbm', im_65)
    
    return 


if __name__ == "__main__":
    
    # Make Rooms 65, 67-70 (modified)
    special_image()
    