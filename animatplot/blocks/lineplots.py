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
    passing a list of those blocks to `animatplot.Animation`.
    """
    def __init__(self, *args, ax=None, t_axis=0, **kwargs):

        super().__init__(ax, t_axis)

        if len(args) == 1:
            y = args[0]
            x = None
        elif len(args) == 2:
            [x, y] = args
        else:
            raise ValueError("Invalid data arguments to Line block")

        if y is None:
            raise ValueError("Must supply y data to plot")
        y = np.asanyarray(y)
        if str(y.dtype) == 'object':
            self.t_axis = 0

            # ragged array
            if x is None:
                raise ValueError("Must specify x data explicitly when passing"
                                 "a ragged array for y data")

            x = np.asanyarray(x)

            if not all(len(xline) == len(yline) for xline, yline in zip(x, y)):
                raise ValueError("Length of x & y data must match one another "
                                 "for every frame")

            self._is_list = True

        else:
            # Rectangular data
            if y.ndim != 2:
                raise ValueError("y data must be 2-dimensional")

            # x is optional
            shape = list(y.shape)
            shape.remove(y.shape[t_axis])
            data_length, = shape
            if x is None:
                x = np.arange(data_length)
            else:
                x = np.asanyarray(x)

            shape_mismatch = "The dimensions of x must be compatible with " \
                             "those of y, but the shape of x is {} and the " \
                             "shape of y is {}".format(x.shape, y.shape)
            if x.ndim == 1:
                # x is constant over time
                if len(x) == data_length:
                    # Broadcast x to match y
                    x = np.expand_dims(x, axis=t_axis)
                    x = np.repeat(x, repeats=y.shape[t_axis], axis=t_axis)
                else:
                    raise ValueError(shape_mismatch)
            elif x.ndim == 2:
                if x.shape != y.shape:
                    raise ValueError(shape_mismatch)
            else:
                raise ValueError("x, must be either 1- or 2-dimensional")

        self.x = x
        self.y = y

        frame_slice = self._make_slice(i=0, dim=2)

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
        return self.y.shape[self.t_axis]


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
