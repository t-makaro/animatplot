from warnings import warn
import numpy as np

from .base import Block
from animatplot.util import parametric_line


class Line(Block):
    """
    Animates a single line.

    Accepts additional keyword arguments to be passed to
    :meth:`matplotlib.axes.Axes.plot`.

    Parameters
    ----------
    x : 1D numpy array, list of 1D numpy arrays or a 2D numpy array, optional
        The x data to be animated. If 1D then will be constant over animation.
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
    **kwargs
        Passed on to `matplotlib.axes.Axes.plot`.

    Attributes
    ----------
    line: matplotlib.lines.Line2D

    ax : matplotlib.axes.Axes
        The matplotlib axes that the block is attached to.

    Notes
    -----
    This block animates a single line - to animate multiple lines you must call
    this once for each line, and then animate all of the blocks returned by
    passing a list of those blocks to `animatplot.animation.Animation`.
    """

    def __init__(self, *args, ax=None, t_axis=0, **kwargs):
        axis = kwargs.pop('axis', None)
        if axis is not None:
            warn('axis has been replaced in favour of "ax", '
                 'and will be removed in 0.4.0.')
            ax = axis

        super().__init__(ax, t_axis)

        # TODO handle lists by instead just converting straight to ndarrays?
        # TODO option for x being specified as an unvarying 1D array?

        if len(args) == 1:
            y = args[0]
            x = None
        elif len(args) == 2:
            [x, y] = args
        else:
            raise ValueError("Invalid data arguments to Line block")

        if y is None:
            raise ValueError("Must supply y data to plot")
        self.y = np.asanyarray(y)
        if y.ndim != 2:
            raise ValueError("y data must be 2-dimensional")

        # x is optional
        if x is None:
            x = np.arange(y.shape[t_axis])
        else:
            x = np.asanyarray(x)

        # x might be constant over time
        if x.ndim == 1:
            # TODO better way to specify "not time dimension"
            if x.shape[0] == y.shape[t_axis-1]:
                # Broadcast x to match y
                x = np.repeat(x[..., np.newaxis], repeats=y.shape[t_axis],
                              axis=t_axis)

        print(x.shape)
        print(y.shape)
        if x.shape != y.shape:
            # TODO more informative error message
            raise ValueError("x, y must have the same shape"
                             "or be lists of the same length")

        self.x = x
        self.y = y

        self._is_list = isinstance(self.x, list)
        frame_slice = self._make_slice(0, 2)

        x_first_frame_data = self.x[frame_slice]
        y_first_frame_data = self.y[frame_slice]

        self.line, = self.ax.plot(x_first_frame_data,
                                  y_first_frame_data, **kwargs)

    def _update(self, frame):
        frame_slice = self._make_slice(frame, dim=2)
        x_vector = self.x[frame_slice]
        y_vector = self.y[frame_slice]
        self.line.set_data(x_vector, y_vector)

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
        x_grid, y_grid = parametric_line(x, y)
        super().__init__(x_grid, y_grid, *args, *kwargs)


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
