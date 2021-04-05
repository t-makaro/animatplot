from .base import Block
import matplotlib.pyplot as plt
import numpy as np


class Surface(Block):
    """Animates a surface (wrapping :meth:`mpl_toolkits.mplot3d.axes3d.plot_surface`)

    Parameters
    ----------
    X : 1D or 2D np.ndarray, optional
    Y : 1D or 2D np.ndarray, optional
    C : list of 2D np.ndarray or a 3D np.ndarray
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to attach the block to.
        Must be created with 'projection="3d"'.
        Defaults to matplotlib.pyplot.gca()
    t_axis : int, optional
        The axis of the array that represents time. Defaults to 0.
        No effect if C is a list.
    fixed_vscale: bool, default True
        By default, set the vertical scale using the overall minimum and maximum of the
        array. If set to False, scale is calculated independently for each time slice.

    Attributes
    ----------
    ax : matplotlib axis
        The matplotlib axes that the block is attached to.

    Notes
    -----
    All other keyword arguments get passed to ``ax.plot_surface``
    see :meth:`mpl_toolkits.mplot3d.axes3d.plot_surface` for details.
    """
    def __init__(self, *args, ax=None, t_axis=0, fixed_vscale=True, **kwargs):
        self.kwargs = kwargs

        if len(args) == 1:
            self.C = args[0]
            x1d = np.arange(self.C[0].shape[0])
            y1d = np.arange(self.C[0].shape[1])
            self.Y, self.X = np.meshgrid(y1d, x1d)
        elif len(args) == 3:
            self.X, self.Y, self.C = args
            if len(self.X.shape) not in [1, 2]:
                raise TypeError('X must be a 1D or 2D arrays')
            if len(self.Y.shape) not in [1, 2]:
                raise TypeError('Y must be a 1D or 2D arrays')
        else:
            raise TypeError(
                'Illegal arguments to Surface; see help(ax.plot_surface)')

        if self.kwargs.get("color") is None and self.kwargs.get("cmap") is None:
            # No user-specified colors for plot. Need to set to a fixed value to avoid
            # cycling during the animation
            self.kwargs["color"] = "C0"

        super().__init__(ax, t_axis)

        self._is_list = isinstance(self.C, list)
        self.C = np.asanyarray(self.C)

        if fixed_vscale:
            self.ax.set_zlim([self.C.min(), self.C.max()])

        Slice = self._make_slice(0, 3)

        self.poly = self.ax.plot_surface(self.X, self.Y, self.C[Slice], **self.kwargs)

    def _update(self, i):
        Slice = self._make_slice(i, 3)
        self.ax.collections.clear()
        self.poly = self.ax.plot_surface(self.X, self.Y, self.C[Slice], **self.kwargs)
        return self.poly

    def __len__(self):
        if self._is_list:
            return self.C.shape[0]
        return self.C.shape[self.t_axis]
