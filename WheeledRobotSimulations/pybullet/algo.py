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
from PIL import Image
import matplotlib.pyplot as plt


class SimEnv():
    """
    This is the main class that runs the PyBullet simulation according to the arguments.
    """

    def __init__(self):
        self._data = []
        self._N = 100
        self._iterations = args.iterations
        self._env = gym.make(args.env+str('-v0'))
        if args.env[-2].isnumeric():
            self.room_number_str = args.env[-2:]
        else:
            self.room_number_str = args.env[-1]
        self._strength = args.strength
        self._background = args.background
        self._max_step = args.maxstep
        self._k_thresh = args.k
        self._velocity = args.velocity
        self._dist_tooClose = 0.4
        self._sleep_time = args.sleep_time
        self._verbose = args.verbose
        self._i = 0
        self._liste_position = []
        
        self._env.reset()
        self._obs, self._rew, self._done, self._info = self._env.step([0, 0])
        self._goal_position = self._env._scenario.world._config.goal_config.goal_position
        
        # initialize controllers
        self._controller = CustomController(self._env, self._velocity, verbose=False)
        
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
        
        print('dx and dy: [', self.DX, ', ', self.DY,']')
                
        p.resetDebugVisualizerCamera(cameraDistance=6, cameraYaw=0, cameraPitch=-89.999, cameraTargetPosition=[0.2,-0.2,0]) #[-self.DX,-self.DY,0]
        
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = f'{base_path}/Anims/Room'+self.room_number_str+'_source'+str(int(self._strength))+'_step'+str(int(self._max_step))+'_run'
        i = 1
        if os.path.exists(path+str(i)+".csv"):
            while os.path.exists(path+str(i)+".csv"):
                i += 1
        self._path = path+str(i)

    def _save_image(self, i=None):
        cam_width, cam_height = 2400, 2400
        cam_target_pos = [0.235,-0.22,0] #[-self.DX,-self.DY,0]
        cam_distance = 9.0
        cam_yaw, cam_pitch, cam_roll = 0, -89.999, 0
        cam_up, cam_up_axis_idx, cam_near_plane, cam_far_plane, cam_fov = [0, 0, 1], 2, 0.01, 100, 60
        cam_view_matrix = p.computeViewMatrixFromYawPitchRoll(cam_target_pos, cam_distance, cam_yaw, cam_pitch, cam_roll, cam_up_axis_idx)
        cam_projection_matrix = p.computeProjectionMatrixFOV(cam_fov, cam_width*1./cam_height, cam_near_plane, cam_far_plane)
        image = p.getCameraImage(cam_width, cam_height, cam_view_matrix, cam_projection_matrix)[2][:, :, :3]

        if i is None:
            i = 1
            if os.path.exists(self._path+'_it'+str(i)+".png"):
                while os.path.exists(self._path+'_it'+str(i)+".png"):
                    i += 1
        
        #with open(path+str(i)+".csv", 'w', newline='') as file:
        #    writer = csv.writer(file)
        #    writer.writerows(image)
        #    print("\ndata saved in:", file.name)
        
        result = Image.fromarray(image)
        result.save(self._path+'_it'+str(i)+".png", dpi=(480, 480))

    def _movement(self, action, nbr=1):
        obs, rew, done, info = self._env.step(action)
        print(self._i, end='\r')
        self._i += 1
        if args.save_res:
            x, y, z, roll, pitch, yaw = info['pose']
            self._liste_position.append(
                [self._i, x, y, z, roll, pitch, yaw, info["dist_obj"], obs])
        # if done: break

        time.sleep(self._sleep_time)

        return obs, rew, done, info
        
    def _measure(self):
        info = self._env.get_state()
        distance_to_source = info["dist_obj"]
        r = distance_to_source*100
        if r < 31:
            source_nom = self._strength
        else:
            f = 0.452425578/r + 1245.16411/r**2 - 10134.7807/r**3
            source_nom = self._strength * f
        background_nom = self._background
        mu = source_nom + background_nom
        # check for attenuation by obstacles
        results = p.rayTest(self._env.get_state()['pose'][0:3], self._goal_position)
        hit_fractions = np.array(results, dtype=np.object)[:, 2].astype(dtype=np.float)
        ranges = distance_to_source * hit_fractions
        scan = np.clip(ranges, a_min=0,a_max=distance_to_source)
        if scan < distance_to_source:
            #print('Attenuated signal')
            return np.random.poisson(lam=background_nom)
        else:
            print('Direct view to source', distance_to_source)
            return np.random.poisson(lam=mu)
        
    def _orien(self):
        info = self._env.get_state()
        x, y, z, roll, pitch, yaw = info['pose']
        return yaw
        
    def _algorithm(self, counts, B):
        if counts > B + self._k_thresh*np.sqrt(B):
            step = np.random.uniform(low=0, high=0.1*self._max_step)
        else:
            step = np.random.uniform(low=0, high=self._max_step)
        return step
        
    def _rotate(self):
        # choose random direction
        start_yaw = self._orien() + np.pi
        end_yaw = np.random.rand(1)*2*np.pi
        # print(start_yaw, end_yaw)
        if start_yaw < end_yaw:
            while (self._orien() + np.pi) < end_yaw:
                #print(self._orien())
                command = [self._velocity*0.4, -self._velocity*0.4]
                self._obs, self._rew, self._done, self._info = self._movement(command)
        else:
            while (self._orien() + np.pi) > end_yaw:
                #print(self._orien())
                command = [-self._velocity*0.4, self._velocity*0.4]
                self._obs, self._rew, self._done, self._info = self._movement(command)

    def start(self):
        """Forward the simulation until its complete."""
        i = 0
        dT = 1/60
        while i < self._iterations:
            # acquire radiation measurement
            counts = self._measure()
            # implement algorithm for step size (duration)
            step_set = self._algorithm(counts, self._background)
            T_set = step_set / self._velocity
            #change direction
            self._rotate()
            # begin walk
            info = self._env.get_state()
            x, y, z, roll, pitch, yaw = info['pose']
            self._data.append([i, x+self.DX, y+self.DY, step_set, counts])
            if i <= 100:
                self._save_image(i)
            elif i <= 1000 and i % 10 == 0:
                self._save_image(i)
            elif i % 100 == 0:
                self._save_image(i)
            elif counts > 20:
                self._save_image(i)
            
            print(i, x, y, step_set, counts)
            try:
                T = 0
                while T < T_set: # continue walk until duration reached
                    command = self._controller.get_command()
                    if command is None:
                        self._rotate()
                        self._controller.reset()
                    else:
                        self._obs, self._rew, self._done, self._info = self._movement(command)
                        self._controller.reset()
                        T += dT
            except KeyboardInterrupt:
                print(' The simulation was forcibly stopped.')
                self.save_res()
                break
            if i % self._N == 0: # perform KS test (done offline)
                pass
            i += 1

        print("Number of steps:", self._i)
        print("Simulation time:", self._info['time'], "s\n")
        self._env.close()

    def save_result(self):
        """Save the simulation data in a csv file in the folder
        corresponding to the controller and name it accordingly.
        """
        with open(self._path+".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["iteration", "x", "y", "step_size", "counts"])
            writer.writerows(self._data)
            print("\ndata saved in:", file.name)


def main():
    sim_env = SimEnv()
#    sim_env._save_image()
    sim_env.start()
    if args.save_res:
        sim_env.save_result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Launch pybullet simulation run.')
    parser.add_argument('--env', type=str, default="Room51",
                        help='environnement: kitchen, maze_hard, race_track')
    parser.add_argument('--strength', type=float, default=100,
                        help='source strength cps')
    parser.add_argument('--background', type=float, default=10,
                        help='background strength cps')
    parser.add_argument('--k', type=float, default=2.33,
                        help='number of standard deviations')
    parser.add_argument('--maxstep', type=float, default=4,
                        help='maximum step size')
    parser.add_argument('--velocity', type=float, default=1,
                        help='nominal robot speed')
    parser.add_argument('--sleep_time', type=float, default=0.000000001,
                        help='sleeping time between each step')
    parser.add_argument('--verbose', type=bool, default=True,
                        help='verbose for controller: True or False')
    parser.add_argument('--save_res', type=bool, default=True,
                        help='save the result in a csv file: True or False')
    parser.add_argument('--iterations', type=int, default=5000,
                        help='save the result in a csv file: True or False')
    args = parser.parse_args()
    main()
