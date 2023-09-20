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
        self.xx = np.ones(101)*4.0
        self.yy = np.linspace(5.5, 7., 76)
        self._obs, self._rew, self._done, self._info = self._env.step([0, 0])
        self._goal_position = self._env._scenario.world._config.goal_config.goal_position
        # initialize controllers
        self._controller = CustomController(self._env, self._velocity, verbose=False)
        
    def _measure_is_clear(self, x_des):
        # info = self._env.get_state()
        #distance_to_source = info["dist_obj"]
        #source_nom = self._strength/distance_to_source**2
        #background_nom = self._background
        # mu = source_nom + background_nom
        # check for attenuation by obstacles
        x0 = x_des
        x0[2] += 10.0
        results = p.rayTest(x0, x_des)
        hit_fractions = np.array(results, dtype=np.object)[:, 2].astype(dtype=np.float)
        if hit_fractions < 0.95:
            return False
        else:
            return True

    def start(self):
        """Forward the simulation until its complete."""
        i = 0
        dT = 1/60
        while not self._done:
            # acquire clear / not clear measurement
            is_clear = self._measure_is_clear(x_des=[self.xx[i], self.yy[i], 0.0])

            if is_clear:
                print('The position (',self.xx[i],',',self.yy[i],') is clear')
            else:
                print('The position (',self.xx[i],',',self.yy[i],') is NOT clear')
            try:
                time.sleep(1)

            except KeyboardInterrupt:
                print(' The simulation was forcibly stopped.')
                break

            i += 1
            if i == 100:
                self._done = True

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
    sim_env.start()
#    if args.save_res:
#        sim_env.save_result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Launch pybullet simulation run.')
    parser.add_argument('--env', type=str, default="kitchen",
                        help='environnement: kitchen, maze_hard, race_track, Room0, ..., Room5')
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
