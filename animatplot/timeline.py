import numpy as np
from animatplot.util import demeshgrid


class Timeline:
    """An object to contain and control all of the time

    Parameters
    ----------
    t : array_like
        Gets converted into a numpy array representing
        the time at each frame of the animation.
    units : str, optional
        The units in which the time is measured.
    fps : float, optional
        Indicates the number of frames per second of the animation.
        Defaults to 10.
    log : bool, optional
        Displays the time scale logarithmically (base 10). Defaults to False.
    """
    def __init__(self, t, units='', fps=10, log=False):
        t = np.asanyarray(t)
        if len(t.shape) > 1:
            self.t = demeshgrid(t)
            if self.t is None:
                raise ValueError("Unable to interpret time values."
                                 "Please try passing a 1D array instead.")
        else:
            self.t = t

        self.fps = fps
        self.units = units
        self.log = log

        if self.log:
            self.t = np.log10(self.t)
        self.index = 0

        self._len = len(self.t)

    def __getitem__(self, i):
        return self.t.__getitem__(i)

    def __repr__(self):
        time = repr(self.t)
        units = repr(self.units)
        return "animatplot.animation.Timeline(t={}, units={}, fps={})"\
            .format(time, units, self.fps)

    def __len__(self):
        return self._len

    def _update(self):
        """Increments the current time."""
        self.index = (self.index + 1) % self._len
