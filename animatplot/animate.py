from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider


class Animate():
    def __init__(self, func, xlim, ylim, time, fps=30, res=1000,
                 pre_calc=False):
        """
        Animates a function f: [a,b]x[t0,tf] -> [c,d]

        func : callable
        Takes a numpy array for the x domain and a scalar for the time domain

        xlim : a sequence of floats ex. [a,b] or (a,b)
        ylim : a sequence of floats ex. [c,d] or (c,d)
        time : a sequence of floats ex. [t0,tf] or (t0,tf) (represents seconds)

        fps : float, optional
            indicates how many frames per second to display
        res : integer, optional
            indicates the number of subdivisions of xlim
        pre_calc : bool, optional
            if true, calculates func for all time before plotting
            if false, calculates func as needed
        """
        self._t_0 = time[0]
        self._t_f = time[1]
        self._dt = 1/fps
        self._t_i = self._t_0

        self.func = func
        self.x = np.linspace(xlim[0], xlim[1], res)
        self.t = np.linspace(time[0], time[1], (time[1]-time[0])*fps)

        self._pre_calc = pre_calc
        self._pause = False
        self._has_slider = False
        self._len = len(self.t)

        self.fig = plt.gcf()
        self.ax = plt.axes(xlim=xlim, ylim=ylim)
        self.line, = self.ax.plot(self.x, func(self.x, time[0]))

        if pre_calc:
            self.data = []
            self._i = 0
            for t in self.t:
                self.data.append(func(self.x, t))

        def animate(i):
            if self._has_slider:
                self.slider.set_val(self._t_i)
            if pre_calc:
                self.line.set_data(self.x, self.data[self._i])
                self._i = (self._i + 1) % self._len
                self._t_i = self.t[self._i]
            else:
                self.line.set_data(self.x, func(self.x, self._t_i))
                self._t_i += self._dt
                if self._t_i > self._t_f:
                    self._t_i = self._t_0
            return self.line,

        self.anim = FuncAnimation(
            self.fig, animate, frames=self._len, interval=1000/fps)

    def toggle(self, rect=[.78, .03, .1, .07], adjust_plot={'bottom': .2}):
        """Creates a play/pause button to start/stop the animation"""
        plt.subplots_adjust(**adjust_plot)
        self.button_ax = plt.axes(rect)
        self.button = Button(self.button_ax, "Pause")
        self.button.label2 = self.button_ax.text(
            0.5, 0.5, 'Play', verticalalignment='center',
            horizontalalignment='center', transform=self.button_ax.transAxes)
        self.button.label2.set_visible(False)

        def pause(event):
            if self._pause:
                self.anim.event_source.start()
                self.button.label.set_visible(True)
                self.button.label2.set_visible(False)
            else:
                self.anim.event_source.stop()
                self.button.label.set_visible(False)
                self.button.label2.set_visible(True)
            self.fig.canvas.draw()
            self._pause ^= True
        self.button.on_clicked(pause)

    def timeline(self, rect=[.18, .05, .5, .03], adjust_plot={'bottom': .2}):
        """Create a timeline slider."""
        plt.subplots_adjust(**adjust_plot)
        self.slider_ax = plt.axes(rect)
        self.slider = Slider(
            self.slider_ax, "Time", self.t[0], self.t[-1], valinit=self.t[0])
        self._has_slider = True

        def set_time(t):
            self._t_i = self.slider.val
            if self._pre_calc:
                self._i = np.where(abs(self.t-self._t_i) <= self._dt)[0][0]
            if self._pause:
                self.line.set_data(self.x, self.func(self.x, self._t_i))
                self.fig.canvas.draw()
        self.slider.on_changed(set_time)
