from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import collections
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider


class Animation:
    """
    Provides a base class that controls timing and interactive elements
    """

    def __init__(self, time, fps=30, pre_calc=False):
        self._t_0 = time[0]
        self._t_f = time[1]
        self._dt = 1/fps
        self._t_i = self._t_0

        self.t = np.linspace(time[0], time[1], (time[1]-time[0])*fps)

        self._pre_calc = pre_calc
        self._pause = False
        self._has_slider = False
        self._len_t = len(self.t)

        self.fig = plt.gcf()

        def animate(i):
            pass

        self.anim = FuncAnimation(
            self.fig, animate, frames=self._len_t, interval=1000/fps)

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

    def timeline(self, rect=[.18, .05, .5, .03], adjust_plot={'bottom': .2},
                 t_scale=(1, '')):
        """Create a timeline slider."""
        plt.subplots_adjust(**adjust_plot)
        self.slider_ax = plt.axes(rect)
        self.slider = Slider(
            self.slider_ax, "Time", self.t[0], self.t[-1],
            valinit=self.t[0], valfmt=('%1.2f'+t_scale[1]))
        self._has_slider = True

        def set_time(t):
            self._t_i = self.slider.val
            self.slider.valtext.set_text(
                self.slider.valfmt % (self.slider.val*t_scale[0]))
            if self._pre_calc:
                self._i = np.where(abs(self.t-self._t_i) <= self._dt)[0][0]
            if self._pause:
                self._update_state()
                self.fig.canvas.draw()
        self.slider.on_changed(set_time)

    def _update_state(self):
        pass

    def _update_time(self):
        if self._has_slider:
            self.slider.set_val(self._t_i)
        if self._pre_calc:
            self._i = (self._i + 1) % self._len_t
            self._t_i = self.t[self._i]
        else:
            self._t_i += self._dt
            if self._t_i > self._t_f:
                self._t_i = self._t_0

class Animate(Animation):
    def __init__(self, func, xlim, ylim, time, fps=30, res=1000,
                 pre_calc=False):
        """
        Animates a function f: [a,b]x[t0,tf] -> [c,d]

        func : callable or iterable of callables
        Takes a numpy array for the x domain and a scalar for the time domain
        Returns a numpy array for the y domain

        xlim : a sequence of floats ex. [a,b] or (a,b)
        ylim : a sequence of floats ex. [c,d] or (c,d)
        time : a sequence of floats ex. [t0,tf] or (t0,tf) (in seconds)

        fps : float, optional
            indicates how many frames per second to display
        res : integer, optional
            indicates the number of subdivisions of xlim
        pre_calc : bool, optional
            if true, calculates func for all time before plotting
            if false, calculates func as needed
        """

        if isinstance(func, collections.Iterable):
            self.funcs = list(func)
        else:
            self.funcs = [func]

        Animation.__init__(self, time, fps, pre_calc)

        self.lines = []
        self._len_l = len(self.funcs)
        self.x = np.linspace(xlim[0], xlim[1], res)

        self.ax = plt.axes(xlim=xlim, ylim=ylim)
        for func in self.funcs:
            line, = self.ax.plot(self.x, func(self.x, time[0]))
            self.lines.append(line)

        if pre_calc:
            self.data = []
            self._i = 0
            for func in self.funcs:
                datum = []
                for t in self.t:
                    datum.append(func(self.x, t))
                self.data.append(datum)

        def animate(i):
            self._update_state()
            self._update_time()
            return self.lines

        self.anim = FuncAnimation(
            self.fig, animate, frames=self._len_t, interval=1000/fps)

    def _update_state(self):
        if self._pre_calc:
            for i in range(self._len_l):
                self.lines[i].set_data(self.x, self.data[i][self._i])
        else:
            for i in range(self._len_l):
                self.lines[i].set_data(self.x,
                                       self.funcs[i](self.x, self._t_i))

class AnimateParametric(Animation):
    def __init__(self, func, xlim, ylim, time, fps=30,
                 pre_calc=False):
        """
        Animates a function f: [t0,tf] -> [a,b]x[c,d]

        func : callable or iterable of callables
        Takes a numpy array for the time domain
        Returns a list of x coordinates and a list of y coordinates

        xlim : a sequence of floats ex. [a,b] or (a,b)
        ylim : a sequence of floats ex. [c,d] or (c,d)
        time : a sequence of floats ex. [t0,tf] or (t0,tf) (in seconds)

        fps : float, optional
            indicates how many frames per second to display
        pre_calc : bool, optional
            if true, calculates func for all time before plotting
            if false, calculates func as needed
        """

        if isinstance(func, collections.Iterable):
            self.funcs = list(func)
        else:
            self.funcs = [func]

        Animation.__init__(self, time, fps, pre_calc)

        self.lines = []
        self._len_l = len(self.funcs)

        self.ax = plt.axes(xlim=xlim, ylim=ylim)
        for func in self.funcs:
            x, y = func(time[0])
            line, = self.ax.plot(x, y)
            self.lines.append(line)

        if pre_calc:
            self.x_data = []
            self.y_data = []
            self._i = 0
            for func in self.funcs:
                x, y = func(self.t)
                self.x_data.append(x)
                self.y_data.append(y)

        def animate(i):
            self._update_state()
            self._update_time()
            return self.lines

        self.anim = FuncAnimation(
            self.fig, animate, frames=self._len_t, interval=1000/fps)

    def _update_state(self):
        if self._pre_calc:
            for i in range(self._len_l):
                self.lines[i].set_data(self.x_data[i][:self._i+1],
                                       self.y_data[i][:self._i+1])
        else:
            t = np.arange(self._t_0, self._t_i+self._dt, self._dt)
            for i in range(self._len_l):
                x, y = self.funcs[i](t)
                self.lines[i].set_data(x, y)
