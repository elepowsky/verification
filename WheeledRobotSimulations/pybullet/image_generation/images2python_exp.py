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

    # Maps 101-106 -- experimental setups
    im_101 = np.copy(im_base)
    im_102 = np.copy(im_base)

    for i in range(xmax):
        for j in range(ymax):
            if i <= 4*ppi or i > 8*ppi:
                im_101[i,j] = int(0)

            elif j <= 3*ppi or j > 8*ppi:
                im_101[i,j] = int(0)
    
    for i in range(xmax):
        for j in range(ymax):
            if i <= 2*ppi or i > 9*ppi:
                im_102[i,j] = int(0)

            elif j <= 3.5*ppi or j > 7.5*ppi:
                im_102[i,j] = int(0)
            
            elif i <= 5*ppi and j > 5.5*ppi:
                im_102[i,j] = int(0)

    # cv2.imwrite('../Rooms/Room'+str(101)+'.jpg', im_101)
    # cv2.imwrite('../Rooms/Room'+str(101)+'.pbm', im_101)

    # cv2.imwrite('../Rooms/Room'+str(102)+'.jpg', im_102)
    # cv2.imwrite('../Rooms/Room'+str(102)+'.pbm', im_102)

    im_103 = np.copy(im_base)
    im_104 = np.copy(im_base)
    im_105 = np.copy(im_base)
    im_106 = np.copy(im_base)

    for i in range(xmax):
        for j in range(ymax):
            if i <= 4*ppi or i > 8*ppi:
                im_103[i,j] = int(0)
                im_104[i,j] = int(0)
                im_105[i,j] = int(0)
                im_106[i,j] = int(0)

            elif j <= 4*ppi or j > 8*ppi:
                im_103[i,j] = int(0)
                im_104[i,j] = int(0)
                im_105[i,j] = int(0)
                im_106[i,j] = int(0)

            elif j < 6*ppi and i <= 5*ppi:
                im_103[i,j] = int(0)
                im_104[i,j] = int(0)
            
            elif j < 6*ppi and i > 7*ppi:
                im_104[i,j] = int(0)
            
            if j > 6*ppi and i > 6*ppi:
                if np.abs(i - 7.5*ppi) > ppi/2 or np.abs(j-6.5*ppi) > ppi/2:
                    im_106[i,j] = int(0)
            
            if i > 6*ppi-4 and i < 6*ppi+4 and j <= 6*ppi:
                im_105[i,j] = int(0)

    # cv2.imwrite('../Rooms/Room'+str(103)+'.jpg', im_103)
    # cv2.imwrite('../Rooms/Room'+str(103)+'.pbm', im_103)

    # cv2.imwrite('../Rooms/Room'+str(104)+'.jpg', im_104)
    # cv2.imwrite('../Rooms/Room'+str(104)+'.pbm', im_104)

    # cv2.imwrite('../Rooms/Room'+str(105)+'.jpg', im_105)
    # cv2.imwrite('../Rooms/Room'+str(105)+'.pbm', im_105)

    # cv2.imwrite('../Rooms/Room'+str(106)+'.jpg', im_106)
    # cv2.imwrite('../Rooms/Room'+str(106)+'.pbm', im_106)


    return 


if __name__ == "__main__":
    
    # Make six experimental setups
    special_image()
    