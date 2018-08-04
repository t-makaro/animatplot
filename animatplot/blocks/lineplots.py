from .base import Block
from animatplot.util import parametric_line
import numpy as np


class Line(Block):
    """Animates lines

    Parameters
    ----------
    x, y : list of 1D numpy arrays or a 2D numpy array
        The data to be animated.
    axis : matplotlib.axes.Axes, optional
        The axis to attach the block to. Defaults to
        matplotlib.pyplot.gca()
    t_axis : int, optional
        The axis of the numpy array that represents time.
        Defaults to 0. No effect if x, y are lists of numpy arrays.

        The default is chosen to be consistent with:
            X, T = numpy.meshgrid(x, t)
    Notes
    -----
    This block accepts additional keyword arguments to be passed to
    :meth:`matplotlib.axes.Axes.plot`
    """
    def __init__(self, x, y, axis=None, t_axis=0, **kwargs):
        self.x = np.asanyarray(x)
        self.y = np.asanyarray(y)
        super().__init__(axis, t_axis)

        self._is_list = (self.x.dtype == 'object')  # TODO: make this better
        Slice = self._make_slice(0, 2)
        self.line, = self.ax.plot(self.x[Slice], self.y[Slice], **kwargs)

    def _update(self, i):
        Slice = self._make_slice(i, 2)
        x_vector = self.x[Slice]
        y_vector = self.y[Slice]

        self.line.set_data(x_vector, y_vector)
        return self.line

    def __len__(self):
        if self._is_list:
            return self.x.shape[0]
        return self.x.shape[self.t_axis]


class ParametricLine(Line):
    """Animates lines

    Parameters
    ----------
    x, y : 1D numpy array
        The data to be animated.
    axis : matplotlib.axes.Axes
        The axis to attach the block to.
    """
    def __init__(self, x, y, *args, **kwargs):
        X, Y = parametric_line(x, y)
        super().__init__(X, Y, *args, *kwargs)
