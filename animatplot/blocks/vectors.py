from .base import Block
import numpy as np
from warnings import warn


class Quiver(Block):
    """
    A block for animated quiver plots

    Parameters
    ----------
    X : 1D or 2D numpy array
        The x positions of the arrows. Cannot be animated.
    Y : 1D or 2D numpy array
        The y positions of the arrows. Cannot be animated.
    U : 2D or 3D numpy array
        The U displacement of the arrows. 1 dimension
        higher than the X, Y arrays.
    V : 2D or 3D numpy array
        The V displcement of the arrows. 1 dimension
        higher than the X, Y arrays.
    ax : matplotlib.axes.Axes, optional
        The matplotlib axes to the block to.
        Defaults to matplotlib.pyplot.gca()
    t_axis : int, optional
        The axis of the array that represents time. Defaults to 0.
        No effect if U, V are lists.

    Attributes
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axes that the block is attached to.

    Notes
    -----
    This block accepts additional keyword arguments to be passed to
    :meth:`matplotlib.axes.Axes.quiver`
    """
    def __init__(self, X, Y, U, V, ax=None, t_axis=0, **kwargs):
        axis = kwargs.pop('axis', None)
        if axis is not None:
            warn('axis has been replaced in favour of "ax", '
                 'and will be removed in 0.4.0')
            ax = axis

        self.X = X
        self.Y = Y
        self.U = np.asanyarray(U)
        self.V = np.asanyarray(V)
        if X.shape != Y.shape:
            raise ValueError("X, Y must have the same shape")
        if self.U.shape != self.V.shape:
            raise ValueError("U, V must have the same shape")

        super().__init__(ax, t_axis)

        self._dim = len(self.U.shape)
        self._is_list = isinstance(U, list)

        Slice = self._make_slice(0, self._dim)
        self.Q = self.ax.quiver(self.X, self.Y,
                                self.U[Slice], self.V[Slice],
                                **kwargs)

    def _update(self, i):
        Slice = self._make_slice(i, self._dim)
        self.Q.set_UVC(self.U[Slice], self.V[Slice])
        return self.Q

    def __len__(self):
        if self._is_list:
            return self.U.shape[0]
        return self.U.shape[self.t_axis]
