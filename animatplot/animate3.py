from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import collections
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .animate import Animation

class AnimateImage(Animation):
    def __init__(self, func, xlim, ylim, time, fps=30,
                 pre_calc=False, res=(200,200), image_args={}):
        """
        Animates a function f: [a,b]x[c,d]x[t0,tf] -> [e,f]

        func : callable
        Takes a numpy array for the time domain
        Returns a list of x coordinates and a list of y coordinates

        xlim : a sequence of floats ex. [a,b] or (a,b)
        ylim : a sequence of floats ex. [c,d] or (c,d)
        time : a sequence of floats ex. [t0,tf] or (t0,tf) (in seconds)

        fps : float, optional
            indicates how many frames per second to display
        res : sequence of 2 ints, optional
            indicates the number of subdivisions of xlim and ylim
        pre_calc : bool, optional
            if true, calculates func for all time before plotting
            if false, calculates func as needed
        """

        self.func = func
        x = np.linspace(xlim[0], xlim[1], res[0])
        y = np.linspace(ylim[0], ylim[1], res[1])
        self.x, self.y = np.meshgrid(x, y)
        
        extent = image_args.get('extent', [xlim[0], xlim[1], ylim[0], ylim[1]])
        image_args['extent'] = extent

        Animation.__init__(self, time, fps, pre_calc)

        z_0 = func(self.x, self.y, time[0])
        self.im = plt.imshow(z_0, animated=True, **image_args)
        self.ax = plt.axes()

        if pre_calc:
            self.data = []
            self._i = 0
            for t in self.t:
                self.data.append(func(self.x, self.y, t))

        def animate(i):
            self._update_state()
            self._update_time()
            return self.im,

        self.anim = FuncAnimation(
            self.fig, animate, frames=self._len_t, interval=1000/fps)

    def _update_state(self):
        if self._pre_calc:
            self.im.set_array(self.data[self._i])
        else:
            self.im.set_array(self.func(self.x, self.y, self._t_i))
