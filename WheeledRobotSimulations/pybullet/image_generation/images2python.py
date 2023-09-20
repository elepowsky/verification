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

def main_loop(seed_integer, room_type=0):
    np.random.seed(seed_integer)

    # 96 pixels per inch
    ppi = 96

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

    if room_type == 0:
        # Add in random walls -- width of 1/6 ppi
        wall_width = int(ppi/6)
        n_walls = 4

        wall_dirs = np.zeros(n_walls).astype(int) # 0 = horizontal
        wall_dirs[:int(np.floor(n_walls/2))] = int(1) # 1 = vertical

        k_scaling = 4
        wall_lengths = np.random.randint(int(3*k_scaling), high=int(k_scaling*(im_dim[0]-1)/2), size=n_walls)*(int(ppi/k_scaling))
        wall_positions = np.random.randint(int(k_scaling*1.5), high=int(k_scaling*(im_dim[0]-1.5)), size=(2, n_walls))*(int(ppi/k_scaling))

        for i in range(xmax):
            for j in range(ymax):
                for k in range(n_walls):
                    if wall_dirs[k] == 0: # Horizontal
                        if (i >= wall_positions[0,k] and i <= wall_positions[0,k] + wall_lengths[k]) and (j >= wall_positions[1,k] and j <= wall_positions[1,k] + wall_width):
                            im_base[i, j] = int(0)
                    elif wall_dirs[k] == 1: # Vertical
                        if (i >= wall_positions[0,k] and i <= wall_positions[0,k] + wall_width) and (j >= wall_positions[1,k] and j <= wall_positions[1,k] + wall_lengths[k]):
                            im_base[i, j] = int(0)
                    else:
                        raise ValueError('wall_dirs[k] must be either 0 or 1')

    elif room_type == 1:
        # Add in random boxes of side length 2*ppi
        square_width_px = int(2*ppi)
        n_squares = 5

        # Positions go at 1/2-inch intervals --> 
        k_scaling = 1
        corner_interval = int(ppi/k_scaling)

        # Generate corner positions
        # x, y ranges [0.5, 8.5]
        val_range = int(8)
        x_corners_0 = np.random.randint(0, high=val_range*k_scaling+1, size=n_squares)*corner_interval + int(1*ppi/2)    # Pixel space
        y_corners_0 = np.random.randint(0, high=val_range*k_scaling+1, size=n_squares)*corner_interval + int(1*ppi/2)    # Pixel space

        for i in range(xmax):
            for j in range(ymax):
                for k in range(n_squares):
                    if i >= x_corners_0[k] and i < x_corners_0[k] + square_width_px and j >= y_corners_0[k] and j < y_corners_0[k] + square_width_px:
                        im_base[i, j] = int(0)

    # cv2.imshow('blank_room', im_base)
    # cv2.imwrite('../Rooms/Room'+str(seed_integer)+'.jpg', im_base)
    # cv2.imwrite('../Rooms/Room'+str(seed_integer)+'.pbm', im_base)

    return

def special_image(dumbbellMap=False, lBeamMap=False, lBeamMapAdv=True, cBeamMap=False, fifthMap=False):

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

    if dumbbellMap:
        im_dumbbell = np.copy(im_base)
        centerWidth = ppi
        for i in range(xmax):
            for j in range(ymax):
                if j > ppi*3 and j < ppi*8:
                    if np.abs(i-(xmax/2)) > centerWidth/2:
                        im_dumbbell[i, j] = int(0)

        # cv2.imwrite('../Rooms/Room'+str(1)+'.jpg', im_dumbbell)
        # cv2.imwrite('../Rooms/Room'+str(1)+'.pbm', im_dumbbell)

    if lBeamMap:
        im_lbeam = np.copy(im_base)
        for i in range(xmax):
            for j in range(ymax):
                if j <= ppi*8 and i >= ppi*3:
                    if not ((j >= ppi*7.5) and (i >= ppi*10)):
                        im_lbeam[i, j] = int(0)
        
        # cv2.imwrite('../Rooms/Room'+str(2)+'.jpg', im_lbeam)
        # cv2.imwrite('../Rooms/Room'+str(2)+'.pbm', im_lbeam)
    
    if lBeamMapAdv:
        im_lbeam_adv = np.copy(im_base)
        for i in range(xmax):
            for j in range(ymax):
                if j <= ppi*8 and i >= ppi*3:
                    if (not ((j >= ppi*6.5) and (i >= ppi*9.5))) and (not ((j >= ppi*6.5) and (j <= ppi*7.5) and (i >= ppi*8.5))):
                        im_lbeam_adv[i, j] = int(0)
        
        # cv2.imwrite('../Rooms/Room'+str(3)+'.jpg', im_lbeam_adv)
        # cv2.imwrite('../Rooms/Room'+str(3)+'.pbm', im_lbeam_adv)
    
    if cBeamMap:
        im_cbeam = np.copy(im_base)
        for i in range(xmax):
            for j in range(ymax):
                if j <= ppi*9 and i >= ppi*2.5 and i <=ppi*8.5:
                        im_cbeam[i, j] = int(0)
        
        # cv2.imwrite('../Rooms/Room'+str(4)+'.jpg', im_cbeam)
        # cv2.imwrite('../Rooms/Room'+str(4)+'.pbm', im_cbeam)
    
    if fifthMap:
        im_fifth = np.copy(im_base)
        centerEmpty = 4*ppi
        centerWidth = 1*ppi
        for i in range(xmax):
            for j in range(ymax):
                if np.abs(i-(xmax/2)) > centerEmpty/2 or np.abs(j-(ymax/2)) > centerEmpty/2:
                    if np.abs(i-(xmax/2)) > centerWidth/2 and np.abs(j-(ymax/2)) > centerWidth/2:
                        # if ((i <= 9.5*ppi or i >= 10.5*ppi) or (j <= xmax/2 or j >= xmax/2 + centerWidth/2 + ppi/2) or ((i <= 0.5*ppi or i >= 1.5*ppi) or (j <= xmax/2 or j >= xmax/2 + centerWidth/2 + ppi/2))):
                        if (i <= 9.5*ppi or i >= 10.5*ppi or j <= xmax/2 + centerWidth/2 or j >= xmax/2 + centerWidth/2 + ppi) and (i <= 0.5*ppi or i >= 1.5*ppi or j <= xmax/2 + centerWidth/2 or j >= xmax/2 + centerWidth/2 + ppi):
                            if (j <= 9.5*ppi or j >= 10.5*ppi or i <= xmax/2 + centerWidth/2 or i >= xmax/2 + centerWidth/2 + ppi) and (j <= 0.5*ppi or j >= 1.5*ppi or i <= xmax/2 + centerWidth/2 or i >= xmax/2 + centerWidth/2 + ppi):
                                im_fifth[i, j] = int(0)
        
        # cv2.imwrite('../Rooms/Room'+str(5)+'.jpg', im_fifth)
        # cv2.imwrite('../Rooms/Room'+str(5)+'.pbm', im_fifth)
    
    # cv2.imwrite('../Rooms/Room'+str(6)+'.jpg', im_base)
    # cv2.imwrite('../Rooms/Room'+str(6)+'.pbm', im_base)

    return 


if __name__ == "__main__":
    
    # Make 5 special rooms + 1 empty room
    special_image()
    
    # Make wall rooms
    for k in range(7, 17):
        print('Beginning loop: ', k)
        main_loop(k, room_type=0)
        print()

    # Make box rooms
    for k in range(17, 41):
        print('Beginning loop: ', k)
        main_loop(k, room_type=1)
        print()
    