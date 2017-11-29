from __future__ import print_function, division
from Cell2D import Cell2D, Cell2DViewer

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d

import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

# import thinkplot
# from thinkstats2 import Cdf
# from thinkstats2 import RandomSeed


class Earthquake(Cell2D):

    def __init__(self, n, m=None, dist=1, k1=2, k2=None, kl=2, fth=3):
        """Initializes the attributes.

        n: number of rows
        m: number of columns
        dist: distance between blocks (meters)
        k1: spring constant between blocks horizontally (N/m)
        k2: spring constant between blocks vertically (N/m)
        kl: spring constant between blocks and moving plate (N/m)
        fth: threshold force
        global_perturbation: perturb globally
        """
        self.dist = dist
        self.k1 = k1
        self.k2 = k1 if k2 is None else k2
        self.kl = kl
        self.a1 = self.k1 / (2 * self.k1 + 2 * self.k2 + self.kl)
        logging.info("Elasticity coefficient: " + str(self.a1))
        self.a2 = self.k2 / (2 * self.k1 + 2 * self.k2 + self.kl)
        self.fth = fth

        m = n if m is None else m

        d = self.dist * np.random.random((n,m)) - self.dist / 2

        kernel_offsets = np.array(
            [[0,        -self.k2,                          0],
            [-self.k1, (2*self.k1 + 2*self.k2 + self.kl), -self.k1],
            [0,        -self.k2,                          0]]
        )

        # array is a 2-dimensional array of size n*m of forces offsets
        self.array = correlate2d(d, kernel_offsets, mode='same', boundary='fill', fillvalue=0)

    # def forces(self):
    #     """Returns array of forces in the model"""
    #     a = self.array
    #     return f

    def step(self, perturbation=True):
        a = self.array
        logging.debug("INITIAL\n" + str(a))
        # If no blocks slide, add global perturbation
        if (np.absolute(a) < self.fth).all() and perturbation:
            logging.debug("TILT")
            fmax = np.amax(a)
            a += self.fth - fmax
        # get blocks greater than fth
        s = np.where(np.absolute(a) >= self.fth, a, 0)
        logging.debug("SHIFTING\n" + str(s))
        # calculate redistributed forces
        kernel = np.array([[0, self.a2, 0],
                           [self.a1, 0, self.a1],
                           [0, self.a2, 0]])
        redistribution = correlate2d(s, kernel, mode='same', boundary='fill', fillvalue=0)
        logging.debug("REDISTRIBUTION\n" + str(redistribution))
        # a += redistrubiton # Add redistrubited forces. Might be a sign issue here.
        a += np.abs(redistribution)*np.sign(a)  # add redistributed forces
        # TODO: Figure out whether the sign of the forces causes issues with things.
        a = np.where(s, 0, a)  # set shifted blocks to 0
        logging.debug("FINAL\n" + str(a))
        self.array = a
        return np.sum(s>0)

    def run_quake(self):
        num_slide = 1
        total_slide = 0
        while num_slide > 0:
            num_slide = self.step(perturbation=False)
            logging.debug("Number of sliding blocks:" + str(num_slide))
            total_slide += num_slide
        logging.debug("GLOBAL PERTURBATION")
        fmax = np.amax(self.array)
        self.array += self.fth - fmax
        return total_slide

    def run(self, iters):
        all_vals = []
        for _ in range(iters):
            num_slide = self.run_quake()
            if num_slide > 0:
                all_vals.append(num_slide)
        return all_vals


    def get_max_force(self):
        return np.max(self.array)


if __name__ == "__main__":
    steve = Earthquake(3)
    # print(steve.array)
    # steve.run_quake()
    steve.run(100)
