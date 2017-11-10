from __future__ import print_function, division

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate2d

# import thinkplot
# from thinkstats2 import Cdf
# from thinkstats2 import RandomSeed

from Cell2D import Cell2D, Cell2DViewer

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
        """
        self.dist = dist
        self.k1 = k1
        self.k2 = k1 if k2 is None else k2
        self.kl = kl
        self.a1 = self.k1 / (2 * self.k1 + 2 * self.k2 + self.kl)
        self.a2 = self.k2 / (2 * self.k1 + 2 * self.k2 + self.kl)
        self.fth = fth

        m = n if m is None else m

        d = self.dist * np.random.random((n,m)) - self.dist / 2

        kernel = np.array(
            [[0,        -self.k2,                          0],
            [-self.k1, (2*self.k1 + 2*self.k2 + self.kl), -self.k1],
            [0,        -self.k2,                          0]]
        )

        # array is a 2-dimensional array of size n*m of forces offsets
        self.array = correlate2d(d, kernel, mode='same', boundary='fill', fillvalue=0)

    # def forces(self):
    #     """Returns array of forces in the model"""
    #     a = self.array
    #     return f

    def step(self):
        a = self.array
        # TODO: redistribute forces above fth
        # get blocks greater than fth
        s = np.where(a >= self.fth, a, 0)
        # print(s)
        # calculate redistributed forces
        kernel = np.array([[0, self.a2, 0],
                           [self.a1, 0, self.a1],
                           [0, self.a2, 0]])
        redistribution = correlate2d(s, kernel, mode='same', boundary='fill', fillvalue=0)
        # print(redistribution)
        a += redistribution  # add redistributed forces
        # print(a)
        a = np.where(s, 0, a)  # set shifted blocks to 0
        # print(a)
        self.array = a

        # TODO: if earthquake is evolved bump up forces


if __name__ == "__main__":
    steve = Earthquake(3)
    print(steve.array)
    for i in range(3):
        print('step {}'.format(i))
        print(steve.array)
        steve.step()
