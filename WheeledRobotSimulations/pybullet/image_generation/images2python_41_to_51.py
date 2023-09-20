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

    # Maps 41-44 -- 80-20, 60-40, 40-60, 20-80
    
    im_41 = np.copy(im_base)
    im_42 = np.copy(im_base)
    im_43 = np.copy(im_base)
    im_44 = np.copy(im_base)
    centerWidth = ppi
    for i in range(xmax):
        for j in range(ymax):
            if j < ppi*2.5:
                im_41[i, j] = int(0)
            
            if j < ppi*4.5:
                im_42[i, j] = int(0)
            
            if j < ppi*6.5:
                im_43[i, j] = int(0)

            if j < ppi*8.5:
                im_44[i, j] = int(0)

    # cv2.imwrite('../Rooms/Room'+str(41)+'.jpg', im_41)
    # cv2.imwrite('../Rooms/Room'+str(41)+'.pbm', im_41)

    # cv2.imwrite('../Rooms/Room'+str(42)+'.jpg', im_42)
    # cv2.imwrite('../Rooms/Room'+str(42)+'.pbm', im_42)

    # cv2.imwrite('../Rooms/Room'+str(43)+'.jpg', im_43)
    # cv2.imwrite('../Rooms/Room'+str(43)+'.pbm', im_43)

    # cv2.imwrite('../Rooms/Room'+str(44)+'.jpg', im_44)
    # cv2.imwrite('../Rooms/Room'+str(44)+'.pbm', im_44)

    # Maps 45-47 -- Aisles
    im_45 = np.copy(im_base)
    im_46 = np.copy(im_base)
    im_47 = np.copy(im_base)
    for i in range(xmax):
        for j in range(ymax):
            # IM_45 is 3 columns
            if (j >= 2*ppi and j < 3*ppi) or (j >= 4.5*ppi and j < 5.5*ppi) or (j >= 7*ppi and j < 8*ppi):
                if (i >= 2.5*ppi and i < 8.5*ppi):
                    im_45[i,j] = int(0)
            
            # IM_46 is 4 columns
            if (j >= 2*ppi and j < 3*ppi) or (j >= 4*ppi and j < 5*ppi) or (j >= 6*ppi and j < 7*ppi) or (j >= 8*ppi and j < 9*ppi):
                if (i >= 2.5*ppi and i < 8.5*ppi):
                    im_46[i,j] = int(0)
            
            # IM_47 is 2 columns
            if (j >= 2.5*ppi and j < 3.5*ppi) or (j >= 7.5*ppi and j < 8.5*ppi):
                if (i >= 1.5*ppi and i < 9.5*ppi):
                    im_47[i,j] = int(0)

    # cv2.imwrite('../Rooms/Room'+str(45)+'.jpg', im_45)
    # cv2.imwrite('../Rooms/Room'+str(45)+'.pbm', im_45)

    # cv2.imwrite('../Rooms/Room'+str(46)+'.jpg', im_46)
    # cv2.imwrite('../Rooms/Room'+str(46)+'.pbm', im_46)

    # cv2.imwrite('../Rooms/Room'+str(47)+'.jpg', im_47)
    # cv2.imwrite('../Rooms/Room'+str(47)+'.pbm', im_47)

    # Maps 48-50 -- Partitions
    im_48 = np.copy(im_base)
    im_49 = np.copy(im_base)
    im_50 = np.copy(im_base)
    for i in range(xmax):
        for j in range(ymax):
            # IM_48 is 2 rooms
            if (j >= 5*ppi and j < 6*ppi):
                if (i >= 6*ppi or i < 5*ppi):
                    im_48[i,j] = int(0)
            
            # IM_49 is 4 rooms
            if ((j >= 5*ppi and j < 6*ppi) and (i >= 1.5*ppi and i < 9.5*ppi)) or ((i >= 5*ppi and i < 6*ppi) and (j >= 1.5*ppi and j < 9.5*ppi)):
                im_49[i,j] = int(0)
            
            # IM_50 is IM_50 as a line, not a cycle (remove one door)
            if ((j >= 5*ppi and j < 6*ppi) and (i >= 1.5*ppi and i < 9.5*ppi)) or ((i >= 5*ppi and i < 6*ppi) and (j >= 1.5*ppi)):
                im_50[i,j] = int(0)
    
    # cv2.imwrite('../Rooms/Room'+str(48)+'.jpg', im_48)
    # cv2.imwrite('../Rooms/Room'+str(48)+'.pbm', im_48)

    # cv2.imwrite('../Rooms/Room'+str(49)+'.jpg', im_49)
    # cv2.imwrite('../Rooms/Room'+str(49)+'.pbm', im_49)

    # cv2.imwrite('../Rooms/Room'+str(50)+'.jpg', im_50)
    # cv2.imwrite('../Rooms/Room'+str(50)+'.pbm', im_50)

    im_51 = np.copy(im_base)
    for i in range(xmax):
        for j in range(ymax):
            # IM_51 is 3 boxes 
            if (i >= 2.5*ppi and i < 4.5*ppi and j >= 2.5*ppi and j < 4.5*ppi) or (i >= 6.5*ppi and i < 8.5*ppi and j >= 2.5*ppi and j < 4.5*ppi) or (i >= 2.5*ppi and i < 4.5*ppi and j >= 6.5*ppi and j < 8.5*ppi):
                im_51[i,j] = int(0)

    # cv2.imwrite('../Rooms/Room'+str(51)+'.jpg', im_51)
    # cv2.imwrite('../Rooms/Room'+str(51)+'.pbm', im_51)

    return 


if __name__ == "__main__":
    
    # Special ending maps
    # -- open map at 80-20, 60-40, 40-60, 20-80 fill ratio (4) 
    # -- Aisles (Ed Sheeran album cover) (2-3)
    # -- Partitions (multiple sub-rooms) (3-4)

    # Make 10 special ending maps + MP
    special_image()
