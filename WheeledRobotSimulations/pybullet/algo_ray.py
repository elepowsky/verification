import os
import sys
import time
import csv
import argparse
import gym
import numpy as np
from iRobot_gym.envs import SimpleNavEnv
import pybullet as p


class SimEnv():

    def __init__(self):
        self._data = []
        self._env = gym.make(args.env+str('-v0'))
        if args.env[-2].isnumeric():
            self.room_number_str = args.env[-2:]
        else:
            self.room_number_str = args.env[-1]
        self.room_number = int(self.room_number_str)
        self._iterations = args.iterations
        self._strength = args.strength
        self._background = args.background
        self._max_step = args.maxstep
        self._k_thresh = args.k
        self._verbose = args.verbose
        self._i = 0
        self._env.reset()
        # Determine room boundaries
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
        self.DX = -(xMax-xMin)/2.0 - xMin
        self.DY = -(yMax-yMin)/2.0 - yMin
        
        # initialize source and robot position
        valid_source = False
        while valid_source is not True:
            source = np.random.random(2)*9.9 - 4.95
            source[0] -= self.DX
            source[1] -= self.DY
            temp_cast = p.rayTest(np.append(source,[0]), np.append(source,[10]))
            hit_fractions = np.array(temp_cast, dtype=np.object)[:, 2].astype(dtype=np.float)
            if hit_fractions < 1:
                pass
            else:
                valid_source = True
        self._source = np.append(source,[0])
        valid_robot = False
        while valid_robot is not True:
            robot = np.random.random(2)*9.9 - 4.95
            robot[0] -= self.DX
            robot[1] -= self.DY
            temp_cast = p.rayTest(np.append(robot,[0]), np.append(robot,[10]))
            hit_fractions = np.array(temp_cast, dtype=np.object)[:, 2].astype(dtype=np.float)
            if hit_fractions < 1:
                pass
            else:
                valid_robot = True
        self._robot = np.append(robot,[0])

    def _measure(self):
        distance_to_source = np.linalg.norm(self._source - self._robot)
        r = distance_to_source*100
        if r < 31:
            source_nom = self._strength
        else:
            f = 0.452425578/r + 1245.16411/r**2 - 10134.7807/r**3
            source_nom = self._strength * f
        background_nom = self._background
        mu = source_nom + background_nom
        # check for attenuation by obstacles
        results = p.rayTest(self._robot, self._source)
        hit_fractions = np.array(results, dtype=np.object)[:, 2].astype(dtype=np.float)
        ranges = distance_to_source * hit_fractions
        scan = np.clip(ranges, a_min=0,a_max=distance_to_source)
        if scan < distance_to_source:
            #print('Attenuated signal')
            return np.random.poisson(lam=background_nom)
        else:
            #print('Direct view to source', distance_to_source)
            return np.random.poisson(lam=mu)
        
    def _algorithm(self, counts, B):
        if counts > B + self._k_thresh*np.sqrt(B):
            step = np.random.uniform(low=0, high=0.1*self._max_step)
        else:
            step = np.random.uniform(low=0, high=self._max_step)
        return step

    def start(self):
        for i in range(self._iterations):
            try:
                # acquire radiation measurement
                counts = self._measure()
                # implement algorithm for step size (duration)
                distance = self._algorithm(counts, self._background)
                angle = np.random.rand(1)*2*np.pi
                # begin walk
                x = self._robot[0]
                y = self._robot[1]
                self._data.append([i, x+self.DX, y+self.DY, distance, counts])
                if i % 10000 == 0:
                    print(i)
                
                reached = False
                angle_set = angle
                dist_remaining = distance
                xstart, ystart = x, y
                while reached is not True:
                    xend = xstart + dist_remaining*np.cos(angle_set)
                    yend = ystart + dist_remaining*np.sin(angle_set)
                    raycast = p.rayTest([xstart,ystart,0.0001], [xend,yend,0.0001])
                    hit_fractions = np.array(raycast, dtype=np.object)[:, 2].astype(dtype=np.float)
                    ranges = dist_remaining*hit_fractions
                    scan = np.clip(ranges, a_min=0,a_max=dist_remaining)
                    if True:
                        if (scan >= dist_remaining):
                            reached = True
                        else:
                            if scan > 0.01:
                                xstart += (scan - 0.01)*np.cos(angle_set)
                                ystart += (scan - 0.01)*np.sin(angle_set)
                                dist_remaining -= (scan - 0.01)
                            angle_set = np.random.rand(1)*2*np.pi
                            
                self._robot[0] = xend
                self._robot[1] = yend
            
            except KeyboardInterrupt:
                print(' The simulation was forcibly stopped.')
                break

        self._env.close()

    def save_result(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = f'{base_path}/Sims/Empirical/New/Room'+self.room_number_str+'/step'+str(int(self._max_step))+'_run'
        i = 1
        if os.path.exists(path+str(i)+".csv"):
            while os.path.exists(path+str(i)+".csv"):
                i += 1
        with open(path+str(i)+".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["iteration", "x", "y", "step_size", "counts"])
            writer.writerows(self._data)
            print("\ndata saved in:", file.name)
        #np.savetxt(path+str(i)+'_source.csv',[self._source[0:2]],delimiter=',')
            

def main():
    sim_env = SimEnv()
    sim_env.start()
    if args.save_res:
        sim_env.save_result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Launch pybullet simulation run.')
    parser.add_argument('--env', type=str, default="kitchen",
                        help='environnement: kitchen, maze_hard, race_track')
    parser.add_argument('--iterations', type=int, default=50000,
                        help='number of iterations/measurements')
    parser.add_argument('--strength', type=float, default=0,
                        help='source strength cps')
    parser.add_argument('--background', type=float, default=10,
                        help='background strength cps')
    parser.add_argument('--k', type=float, default=2.33,
                        help='number of standard deviations')
    parser.add_argument('--maxstep', type=float, default=10,
                        help='maximum step size')
    parser.add_argument('--verbose', type=bool, default=True,
                        help='verbose for controller: True or False')
    parser.add_argument('--save_res', type=bool, default=True,
                        help='save the result in a csv file: True or False')
    args = parser.parse_args()
    main()
