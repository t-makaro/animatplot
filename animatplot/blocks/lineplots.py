from .base import Block
from animatplot.util import parametric_line
import numpy as np


class Line(Block):
    """Animates lines

    Parameters
    ----------
    x : list of 1D numpy arrays or a 2D numpy array
        The x data to be animated.
    y : list of 1D numpy arrays or a 2D numpy array
        The y data to be animated.
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to attach the block to.
        Defaults to matplotlib.pyplot.gca()
    t_axis : int, optional
        The axis of the numpy array that represents time.
        Defaults to 0. No effect if x, y are lists of numpy arrays.

        The default is chosen to be consistent with:
            X, T = numpy.meshgrid(x, t)

    Attributes
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axes that the block is attached to.

    Notes
    -----
    This block accepts additional keyword arguments to be passed to
    :meth:`matplotlib.axes.Axes.plot`
    """
    def __init__(self, x, y, ax=None, t_axis=0, **kwargs):
        self.x = np.asanyarray(x)
        self.y = np.asanyarray(y)
        if self.x.shape != self.y.shape:
            raise ValueError("x, y must have the same shape"
                             "or be lists of the same length")
        super().__init__(ax, t_axis)

        self._is_list = (self.x.dtype == 'object')
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
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to attach the block to.

    Attributes
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axes that the animation is attached to.

    Notes
    -----
    This block accepts additional keyword arguments to be passed to
    :meth:`matplotlib.axes.Axes.plot`
    """
    def __init__(self, x, y, *args, **kwargs):
        X, Y = parametric_line(x, y)
        super().__init__(X, Y, *args, *kwargs)


class Scatter(Block):
    """Animates scatter plots

    Parameters
    ----------
    x : list of 1D numpy arrays or a 2D numpy array
        The x data to be animated.
    y : list of 1D numpy arrays or a 2D numpy array
        The y data to be animated.
    s : scalar, or array_like of the same form as x/y, optional
        The size of the data points to be animated.
    c : color, optional
        The color of the data points. Cannot [yet] be animated.
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to attach the block to.
        Defaults to matplotlib.pyplot.gca()
    t_axis : int, optional
        The axis of the numpy array that represents time.
        Defaults to 0. No effect if x, y are lists of numpy arrays.

        The default is chosen to be consistent with:
            X, T = numpy.meshgrid(x, t)

    Attributes
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axes that the block is attached to.

    Notes
    -----
    This block accepts additional keyword arguments to be passed to
    :meth:`matplotlib.axes.Axes.scatter`
    """
    def __init__(self, x, y, s=None, c=None, ax=None, t_axis=0, **kwargs):
        self.x = np.asanyarray(x)
        self.y = np.asanyarray(y)
        if self.x.shape != self.y.shape:
            raise ValueError("x, y must have the same shape"
                             "or be lists of the same length")

        self.c = c
        self.s = self._parse_s(s)
        super().__init__(ax, t_axis)

        self._is_list = (self.x.dtype == 'object')
        Slice = self._make_slice(0, 2)
        s_Slice = self._make_s_slice(0, 2)
        self.scat = self.ax.scatter(self.x[Slice], self.y[Slice],
                                    self.s[s_Slice], self.c, **kwargs)

    def _parse_s(self, s):
        s = np.asanyarray(s)
        self._s_like_x = (s.shape == self.x.shape)
        if not self._s_like_x:
            if len(s.shape) == 0:
                s = s[None]
            else:
                raise ValueError("s is not a scalar, or like x/y.")
        return s

    def _make_s_slice(self, i, dim):
        if self._s_like_x:
            return self._make_slice(i, dim)
        return 0

    def _update(self, i):
        Slice = self._make_slice(i, 2)
        s_slice = self._make_s_slice(i, 2)

        x, y = self.x[Slice], self.y[Slice]
        data = np.vstack((x, y)).T

        self.scat.set_offsets(data)  # x, y
        if self._s_like_x:
            self.scat._sizes = self.s[s_slice]
        # self.scat.set_array(x_vector, y_vector) # color
        return self.scat

    def __len__(self):
        if self._is_list:
            return self.x.shape[0]
        return self.x.shape[self.t_axis]
