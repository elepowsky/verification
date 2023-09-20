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


class SimEnv():
    """This is the main class that runs the PyBullet simulation according to the arguments.

    Attributes:
        _env: The actual environnment.
        _sleep_time: float, representing the sleep time between each step.
        _ctr: string, the name of the controller.
        _verbose: bool, activate verbose or not.
        _i: int, iterator for steps.
        _liste_position: list of tuples, values to save in the csv file.
    """

    def __init__(self):
        self._data = []
        self._N = 100
        self._env = gym.make(args.env+str('-v0'))
        self._strength = args.strength
        self._background = args.background
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
        source_nom = self._strength/distance_to_source**2
        background_nom = self._background
        mu = source_nom + background_nom
        # check for attenuation by obstacles
        results = p.rayTest(self._env.get_state()['pose'][0:3], self._goal_position)
        hit_fractions = np.array(results, dtype=np.object)[:, 2].astype(dtype=np.float)
        ranges = self._env.get_state()["dist_obj"] * hit_fractions
        scan = np.clip(ranges, a_min=0,a_max=self._env.get_state()["dist_obj"])
        if scan < self._env.get_state()["dist_obj"]:
            print('Attenuated signal')
            return np.random.poisson(lam=background_nom)
        else:
            print('Direct view to source', distance_to_source)
            return np.random.poisson(lam=mu)
        
    def _orien(self):
        info = self._env.get_state()
        x, y, z, roll, pitch, yaw = info['pose']
        return yaw
        
    def _algorithm(self, counts, k_thresh, B, high_step=4.0):
        if counts > B + k_thresh*np.sqrt(B):
            step = np.random.uniform(low=0, high=0.1*high_step)
        else:
            step = np.random.uniform(low=0, high=high_step)
        return step
        
    def _rotate(self):
        # choose random direction
        start_yaw = self._orien() + np.pi
        end_yaw = np.random.rand(1)*2*np.pi
        # Add in margin to account for discrete time
        eps_angle = 0.002
        if start_yaw < end_yaw-eps_angle:
            while (self._orien() + np.pi) < end_yaw-eps_angle:
                #print(self._orien())
                command = [self._velocity*0.4, -self._velocity*0.4]
                self._obs, self._rew, self._done, self._info = self._movement(command)
        elif start_yaw > end_yaw+eps_angle:
            while (self._orien() + np.pi) > end_yaw+eps_angle:
                #print(self._orien())
                command = [-self._velocity*0.4, self._velocity*0.4]
                self._obs, self._rew, self._done, self._info = self._movement(command)
        else:
            command = [-self._velocity*0.0, self._velocity*0.0]
            self._obs, self._rew, self._done, self._info = self._movement(command)

    def start(self):
        """Forward the simulation until its complete."""
        i = 0
        dT = 1/60
        while not self._done:
            # acquire radiation measurement
            counts = self._measure()
            # implement algorithm for step size (duration)
            T_set = self._algorithm(counts, 2, self._background) / self._velocity
            #change direction
            self._rotate()
            # begin walk
            info = self._env.get_state()
            x, y, z, roll, pitch, yaw = info['pose']
            self._data.append([i, x, y, counts, T_set])
            print(i, x, y, counts, T_set)
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
                break
            if i % self._N == 0: # perform KS test
                pass
            i += 1

        print("Number of steps:", self._i)
        print("Simulation time:", self._info['time'], "s\n")
        self._env.close()

#    def save_result(self):
#        """Save the simulation data in a csv file in the folder
#        corresponding to the controller and name it accordingly.
#        """
#        base_path = os.path.dirname(os.path.abspath(__file__))
#        path = f'{base_path}/../results/{args.env}/bullet_{args.ctr}_'
#        i = 1
#        if os.path.exists(path+str(i)+".csv"):
#            while os.path.exists(path+str(i)+".csv"):
#                i += 1
#        with open(path+str(i)+".csv", 'w', newline='') as file:
#            writer = csv.writer(file)
#            writer.writerow(["steps", "x", "y", "z", "roll", "pitch", "yaw",
#                             "distance_to_obj", "laser"])
#            writer.writerows(self._liste_position)
#            print("\ndata saved in:", file.name)


def main():
    sim_env = SimEnv()
    # print(p.getDebugVisualizerCamera())
    # breakpoint()
    p.resetDebugVisualizerCamera(cameraDistance=7.5, cameraYaw=0, cameraPitch=-89.99, cameraTargetPosition=[0.0,0.0,0])
    sim_env.start()
#    if args.save_res:
#        sim_env.save_result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Launch pybullet simulation run.')
    parser.add_argument('--env', type=str, default="Room6",
                        help='environnement: kitchen, maze_hard, race_track, Room0, ...,6')
    parser.add_argument('--strength', type=float, default=20,
                        help='source strength cps')
    parser.add_argument('--background', type=float, default=10,
                        help='background strength cps')
    parser.add_argument('--velocity', type=float, default=1,
                        help='nominal robot speed')
    parser.add_argument('--sleep_time', type=float, default=0.001,
                        help='sleeping time between each step')
    parser.add_argument('--verbose', type=bool, default=True,
                        help='verbose for controller: True or False')
    parser.add_argument('--save_res', type=bool, default=False,
                        help='save the result in a csv file: True or False')
    args = parser.parse_args()
    main()
#    parser.add_argument('--file_name', type=str,
#                        default='NoveltyFitness/9/maze_nsfit9-gen38-p0', help='file name of the invidual to load if ctr=novelty')
