import os
import sys
import time
import csv
import argparse
import gym
import numpy as np
from iRobot_gym.envs import SimpleNavEnv
from controllers.custom import CustomController
import pybullet as p
from matplotlib import pyplot as plt


class SimEnv():

    def __init__(self):
        self._data = []
        self._start_points = []
        self._end_points = []
        self._env = gym.make(args.env+str('-v0'))
        if args.env[-2].isnumeric():
            self.room_number_str = args.env[-2:]
        else:
            self.room_number_str = args.env[-1]
        self.room_number = int(self.room_number_str)
        self._verbose = args.verbose
        self._env.reset()
        
    def start(self):
        ### DEFINE THESE PARAMETERS ### 
        temp_cast = p.rayTest([0.0, 10.0, 0.0001], [0.0, 0.0, 0.0001])
        hit_fractions = np.array(temp_cast, dtype=np.object)[:, 2].astype(np.float)
        yMax = 10.0*(1.0-hit_fractions[0])

        temp_cast = p.rayTest([0.0, -10.0, 0.0001], [0.0, 0.0, 0.0001])
        hit_fractions = np.array(temp_cast, dtype=np.object)[:, 2].astype(np.float)
        yMin = -10.0*(1.0-hit_fractions[0])

        temp_cast = p.rayTest([10.0, 0.0, 0.0001], [0.0, 0.0, 0.0001])
        hit_fractions = np.array(temp_cast, dtype=np.object)[:, 2].astype(np.float)
        xMax = 10.0*(1.0-hit_fractions[0])

        temp_cast = p.rayTest([-10.0, 0.0, 0.0001], [0.0, 0.0, 0.0001])
        hit_fractions = np.array(temp_cast, dtype=np.object)[:, 2].astype(np.float)
        xMin = -10.0*(1.0-hit_fractions[0])
        print('xmin and xmax: [', xMin, ', ', xMax,']')
        print('ymin and ymax: [', yMin, ', ', yMax,']')
        print('xrange and yrange (outer): ', xMax-xMin, ' and ', yMax-yMin)
        
        # Define CX, CY as function of the data to center everything
        DX = -(xMax-xMin)/2.0 - xMin
        DY = -(yMax-yMin)/2.0 - yMin

        # IF DX, DY < 0, then the object is shifted RIGHT / UP
        # ELSE DX, DY > 0, then the object is shifted LEFT / DOWN 
        print('Corrected X: [', xMin + DX, ', ', xMax+DX,']')
        print('Corrected Y: [', yMin + DY, ', ', yMax+DY,']')
        print('DX: ', DX)
        print('DY: ', DY)
        # breakpoint()

        n_linspace = 60
        xs, ys = np.linspace(-4.95, 4.95, n_linspace), np.linspace(-4.95, 4.95, n_linspace)
        #xs, ys = [0], [0]
        N_a = 36
        N_d = 50
        max_step = 10
        num_pts = n_linspace*n_linspace
        ### DEFINE THESE PARAMETERS ###
        it = 0
        for x in xs:
            for y in ys:
                it += 1
                # print(it/num_pts, x, y)
                temp_cast = p.rayTest([x-DX,y-DY,10.], [x-DX,y-DY,0.])
                hit_fractions = np.array(temp_cast, dtype=np.object)[:, 2].astype(dtype=np.float)
                if hit_fractions < 1:
                    pass
                else:
                    print(it/num_pts, x, y)
                    for angle in np.linspace(0,2*np.pi,N_a+1)[:-1]:
                        for dist in np.linspace(0,max_step,N_d+1):
                            reached = False
                            angle_set = angle
                            dist_remaining = dist
                            xstart, ystart = x-DX, y-DY
                            while reached is not True:
                                xend = xstart + dist_remaining*np.cos(angle_set)
                                yend = ystart + dist_remaining*np.sin(angle_set)
                                raycast = p.rayTest([xstart,ystart,0.0001], [xend,yend,0.0001])
                                hit_fractions = np.array(raycast, dtype=np.object)[:, 2].astype(dtype=np.float)
                                ranges = dist_remaining*hit_fractions
                                scan = np.clip(ranges, a_min=0,a_max=dist_remaining)
                                
                                #xend = xstart + scan*np.cos(angle_set)
                                #yend = ystart + scan*np.sin(angle_set)
                                #self._data.append([x,y,float(xend),float(yend),angle,dist])
                                #reached = True
                                
                                if True:
                                    if (scan >= dist_remaining):
                                        #temp_cast = p.rayTest([xend,yend,0], [xend,yend,10])
                                        #hit_fractions = np.array(temp_cast, dtype=np.object)[:, 2].astype(dtype=np.float)
                                        #if hit_fractions < 1:
                                        #    angle_set = np.random.rand(1)*2*np.pi
                                        #else:
                                        reached = True
                                        self._start_points.append([x,y])
                                        self._end_points.append([xend+DX,yend+DY])
                                        self._data.append([float(x),float(y),float(xend+DX),float(yend+DY),angle,dist])
                                    else:
                                        #xstart += 0.9*scan*np.cos(angle_set)
                                        #ystart += 0.9*scan*np.sin(angle_set)
                                        #dist_remaining -= 0.9*scan
                                        #angle_set = np.random.rand(1)*2*np.pi
                                        if scan > 0.01:
                                            xstart += (scan - 0.01)*np.cos(angle_set)
                                            ystart += (scan - 0.01)*np.sin(angle_set)
                                            dist_remaining -= (scan - 0.01)
                                        angle_set = np.random.rand(1)*2*np.pi
        self._env.close()


    def save_result(self):
        file_name = 'pairs_room'+self.room_number_str+'_large.csv'
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["x_start", "y_start", "x_end", "y_end", "angle", "distance"])
            writer.writerows(self._data)
            print("\ndata saved in:", file.name)


def main():
    sim_env = SimEnv()
    sim_env.start()
    if args.save_res:
        sim_env.save_result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Launch pybullet simulation run.')
    parser.add_argument('--env', type=str, default="Room6",
                        help='environnement: kitchen, maze_hard, race_track')
    parser.add_argument('--verbose', type=bool, default=True,
                        help='verbose for controller: True or False')
    parser.add_argument('--save_res', type=bool, default=True,
                        help='save the result in a csv file: True or False')
    parser.add_argument('--file_name', type=str,
                        default='random-walk-pairs-room6-large-new', help='file name of the invidual to load if ctr=novelty')
    args = parser.parse_args()
    main()
