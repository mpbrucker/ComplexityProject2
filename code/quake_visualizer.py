import matplotlib
# matplotlib.rcParams['backend'] = "TkAgg"
from Cell2D import Cell2D, Cell2DViewer
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
rc('animation', html='html5')


class Cell3DViewer(Cell2DViewer):
    cmap = matplotlib.cm.get_cmap('RdYlBu')
    def __init__(self, viewee, z_limit=[0,3]):
        Cell2DViewer.__init__(self, viewee)
        self.fig = plt.figure()
        self.fig.set_size_inches(10,10, True)
        self.ax1 = self.fig.add_subplot(111, projection='3d')
        self.ax1.axis('off')
        self.z_limit = z_limit
        self.ax1.set_zlim(*self.z_limit)

    def draw_array(self, array=None, cmap=None, **kwds):
        self.get_bars()
#         self.fig.canvas.draw()

    def get_bars(self):
        top = np.abs(self.viewee.array.flatten())
        n,m = self.viewee.array.shape
        bottom = np.zeros(n*m)
        width = depth = 1
        _xx, _yy = np.meshgrid(np.arange(n), np.arange(m))
        x, y = _xx.ravel(), _yy.ravel()
#         norm = matplotlib.colors.Normalize(vmin=0,vmax=10)
        colors = [self.cmap(val/self.z_limit[1]) for val in top]
        self.bars = self.ax1.bar3d(x, y, bottom, width, depth, top, color=colors)

    def animate(self, frames=20, interval=200, grid=False):
        """Creates an animation.

        frames: number of frames to draw

        interval: time between frames in ms
        """
        self.draw(grid)
        anim = animation.FuncAnimation(self.fig, self.animate_func,
                                       init_func=self.init_func,
                                       frames=frames, interval=interval)
        return anim

    def live_animate(self):
        plt.show(block=False)
        for i in range(100):
            self.step()
            self.get_bars()
            self.fig.canvas.draw()
            time.sleep(0.01)
            self.bars.remove()


    def animate_func(self, i):
#         print(i)
        self.bars.remove()
        if i>0:
            self.step()
        self.get_bars()
        return (self.bars,)
