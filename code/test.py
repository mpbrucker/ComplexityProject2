

from Cell2D import Cell2D, Cell2DViewer
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import correlate2d


class Cell3DViewer(Cell2DViewer):
    def __init__(self, viewee):
        Cell2DViewer.__init__(self,viewee)
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(111, projection='3d')
        self.fig.canvas.draw()
        plt.show(block=False)

    def draw(self):
        top = self.viewee.array
        n,m = top.shape
#         print(n,m)
        bottom = np.zeros(n*m)
        width = depth = 1
        _xx, _yy = np.meshgrid(np.arange(n), np.arange(m))
        x, y = _xx.ravel(), _yy.ravel()
#         print(x)
#         print(y)
#         print(top)
#         print(bottom)
        bars = self.ax1.bar3d(x, y, bottom, width, depth, top.flatten())
        self.fig.canvas.draw()
        time.sleep(0.01)
        bars.remove()

    def animate(self):
        for i in range(100):
            self.step()
            self.draw()

class Diffusion(Cell2D):
    """Diffusion Cellular Automaton."""

    kernel = np.array([[0, 1, 0],
                       [1,-4, 1],
                       [0, 1, 0]])

    def __init__(self, n, m=None, r=0.1):
        """Initializes the attributes.

        n: number of rows
        m: number of columns
        r: diffusion rate constant
        """
        self.r = r
        m = n if m is None else m
        self.array = np.zeros((n, m), np.float)

    def step(self):
        """Executes one time step."""
        c = correlate2d(self.array, self.kernel, mode='same')
        self.array += self.r * c

if __name__ == '__main__':
    diff = Diffusion(n=6, r=0.1)
    diff.add_cells(3, 3, '111', '111', '111')
    viewer = Cell3DViewer(diff)
    viewer.animate()
